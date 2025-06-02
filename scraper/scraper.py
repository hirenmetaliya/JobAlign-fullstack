# scraper.py

import asyncio
from playwright.async_api import async_playwright
from urllib.parse import urlparse
import google.generativeai as genai
import re
import json
import csv
import time
from datetime import datetime
from typing import List, Dict, Optional
import logging
from concurrent.futures import ThreadPoolExecutor
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import socket
from progress import ProgressBar, clear_line

# ----------------------------
# Setup: Logging and Config
# ----------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)

# Configuration
CSV_FILE = "company_websites.csv"
GEMINI_API_KEY = "AIzaSyAeDl5kbNgkXEPZf9QGr81ie3ikn-QroSc"
MAX_CONCURRENT_REQUESTS = 20  # Increased for faster processing
MAX_RETRIES = 3
TIMEOUT = 30000
MAX_WEBSITES_TO_SCRAPE = 50

# Email Configuration
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'your-email@gmail.com',  # Replace with your email
    'sender_password': 'your-app-password',  # Replace with your app password
    'recipient_email': 'recipient@example.com'  # Replace with recipient email
}

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# ----------------------------
# Utility Functions
# ----------------------------
def clean_json_output(text: str) -> Optional[str]:
    """Clean and extract JSON from Gemini's response."""
    try:
        text = text.strip().replace("```json", "").replace("```", "").strip()
        match = re.search(r'\[\s*{.*?}\s*\]', text, re.DOTALL)
        return match.group(0) if match else None
    except Exception as e:
        logging.error(f"Error cleaning JSON output: {e}")
        return None

async def scrape_links(base_url: str, page) -> List[str]:
    """Scrape relevant career/job links from a company website."""
    for attempt in range(MAX_RETRIES):
        try:
            await page.goto(base_url, timeout=TIMEOUT)
            await page.wait_for_load_state("networkidle")
            
            links = await page.locator("a").all()
            hrefs = []
            for link in links:
                try:
                    href = await link.get_attribute("href")
                    if href:
                        hrefs.append(href)
                except:
                    continue

            relevant_keywords = ["careers", "career", "job opening", "job openings", "open positions"]
            filtered_links = [
                link for link in hrefs 
                if link and any(keyword in link.lower() for keyword in relevant_keywords)
            ]
            
            # Convert relative URLs to absolute
            base_domain = urlparse(base_url).netloc
            absolute_links = []
            for link in filtered_links:
                if link.startswith('http'):
                    absolute_links.append(link)
                else:
                    absolute_links.append(f"https://{base_domain}{link}")
            
            return list(set(absolute_links))
            
        except Exception as e:
            logging.warning(f"Attempt {attempt + 1} failed for {base_url}: {str(e)}")
            if attempt == MAX_RETRIES - 1:
                logging.error(f"Failed to scrape links from {base_url} after {MAX_RETRIES} attempts")
                return []
            await asyncio.sleep(2 ** attempt)  # Exponential backoff

async def process_company(base_url: str, browser, progress_bar) -> List[Dict]:
    """Process a single company website and extract job information."""
    try:
        page = await browser.new_page()
        
        # Scrape career links
        career_links = await scrape_links(base_url, page)
        if not career_links:
            progress_bar.update(progress_bar.current + 1)
            await page.close()
            return []

        # Process each career page
        results = []
        for url in career_links:
            try:
                await page.goto(url, timeout=TIMEOUT)
                await page.wait_for_load_state("networkidle")
                content = await page.content()
                
                # Extract job information using Gemini
                response = model.generate_content(f"""
                Extract job information from this HTML content. Return only valid JSON:
                ```json
                [
                  {{
                    "Job Position": "<position>",
                    "Apply Link": "<apply_url>"
                  }}
                ]
                ```
                If no jobs found, return: `[]`
                
                HTML:
                {content}
                """)

                json_output = clean_json_output(response.text)
                if json_output:
                    parsed_data = json.loads(json_output)
                    for job in parsed_data:
                        job["Company"] = urlparse(base_url).netloc
                        job["Source URL"] = url
                    results.extend(parsed_data)
                
                await asyncio.sleep(1)  # Reduced delay between requests
                
            except Exception as e:
                logging.error(f"Error processing {url}: {str(e)}")
                continue

        progress_bar.update(progress_bar.current + 1)
        return results

    except Exception as e:
        logging.error(f"Error processing company {base_url}: {str(e)}")
        progress_bar.update(progress_bar.current + 1)
        return []
    finally:
        await page.close()

async def process_batch(urls: List[str], browser, json_filename: str, progress_bar) -> List[Dict]:
    """Process a batch of company websites concurrently."""
    tasks = [process_company(url, browser, progress_bar) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Filter out exceptions and flatten results
    valid_results = []
    for result in results:
        if isinstance(result, list):
            valid_results.extend(result)
    
    # Save results incrementally
    if valid_results:
        try:
            existing_results = []
            if os.path.exists(json_filename):
                with open(json_filename, 'r') as f:
                    existing_results = json.load(f)
            
            all_results = existing_results + valid_results
            
            with open(json_filename, 'w') as f:
                json.dump(all_results, f, indent=2)
            
            logging.info(f"Saved {len(valid_results)} new jobs. Total jobs: {len(all_results)}")
        except Exception as e:
            logging.error(f"Error saving incremental results: {e}")
    
    return valid_results

def send_email(subject: str, body: str, is_error: bool = False):
    """Send email notification about scraper status."""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG['sender_email']
        msg['To'] = EMAIL_CONFIG['recipient_email']
        msg['Subject'] = f"{'[ERROR] ' if is_error else ''}Job Scraper - {subject}"
        
        # Add hostname to body
        hostname = socket.gethostname()
        body = f"Host: {hostname}\n\n{body}"
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        server.starttls()
        server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
        server.send_message(msg)
        server.quit()
        
        logging.info("Email notification sent successfully")
    except Exception as e:
        logging.error(f"Failed to send email: {str(e)}")

def get_last_run_info():
    """Get information about the last successful run."""
    try:
        if os.path.exists('scraper.log'):
            with open('scraper.log', 'r') as f:
                lines = f.readlines()
                for line in reversed(lines):
                    if 'Scraping completed' in line:
                        return line.strip()
        return "No previous run information found"
    except Exception as e:
        logging.error(f"Error reading last run info: {str(e)}")
        return "Error reading last run information"

def should_run_today():
    """Check if we need to run the scraper today."""
    today = datetime.now().strftime("%Y-%m-%d")
    json_filename = f"scraped_jobs_{today}.json"
    
    # If today's file exists and is not empty, we've already run
    if os.path.exists(json_filename):
        try:
            with open(json_filename, 'r') as f:
                data = json.load(f)
                if data:  # If file exists and has data
                    last_run = get_last_run_info()
                    logging.info(f"Today's scraping has already been completed. Last run: {last_run}")
                    return False
        except:
            pass
    
    return True

async def main():
    """Main function to orchestrate the scraping process."""
    if not should_run_today():
        return

    start_time = datetime.now()
    logging.info("Starting job scraping process")
    
    try:
        # Read company websites
        base_urls = []
        with open(CSV_FILE, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            base_urls = [row['Company URL'].strip() for row in reader if row.get('Company URL') and row['Company URL'].strip() and not row['Company URL'].startswith('javascript:')]
        
        base_urls = base_urls[:MAX_WEBSITES_TO_SCRAPE]
        total_urls = len(base_urls)
        
        # Create output filename
        today = datetime.now().strftime("%Y-%m-%d")
        json_filename = f"scraped_jobs_{today}.json"
        
        # Initialize progress bar
        progress_bar = ProgressBar(total=total_urls, description="Scraping websites")
        progress_bar.start()
        
        # Initialize empty JSON file
        with open(json_filename, 'w') as f:
            json.dump([], f)

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            
            # Process websites in batches
            all_results = []
            for i in range(0, total_urls, MAX_CONCURRENT_REQUESTS):
                batch = base_urls[i:i + MAX_CONCURRENT_REQUESTS]
                batch_results = await process_batch(batch, browser, json_filename, progress_bar)
                all_results.extend(batch_results)
                await asyncio.sleep(2)  # Brief pause between batches

            await browser.close()
            progress_bar.stop()

        duration = datetime.now() - start_time
        success_message = f"Scraping completed in {duration}. Found {len(all_results)} jobs."
        logging.info(success_message)
        send_email("Scraping Completed Successfully", success_message)
        
    except Exception as e:
        error_message = f"Scraping failed: {str(e)}"
        logging.error(error_message)
        send_email("Scraping Failed", error_message, is_error=True)
        raise

if __name__ == "__main__":
    asyncio.run(main())
