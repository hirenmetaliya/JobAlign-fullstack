from playwright.sync_api import sync_playwright
import json
import time

def scrape_designrush_from_links(category_urls):
    all_companies = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        
        for base_url in category_urls:
            context = browser.new_context()
            page = context.new_page()
            page_number = 1
            first_page_links = None
            print(f"\n🔍 Starting category: {base_url}")
            
            while True:
                full_url = f"{base_url}?page={page_number}"
                print(f"Scraping page {page_number}: {full_url}")
                page.goto(full_url, timeout=60000)
                time.sleep(2)  # Give the page a moment to load
                
                try:
                    page.wait_for_selector("a.js--agency-website-link", timeout=15000)
                except:
                    print(f"No companies found on page {page_number}. Stopping this category.")
                    break

                links = page.query_selector_all("a.js--agency-website-link")
                if not links:
                    print(f"No company links on page {page_number}. Stopping this category.")
                    break

                # Extract current page links (using the href attribute)
                current_links = [link.get_attribute("href").strip() for link in links]

                # If this is not the first page and the list matches that of page 1, break out
                if page_number == 1:
                    first_page_links = current_links
                else:
                    if current_links == first_page_links:
                        print("Detected repeated page. Ending category scrape.")
                        break

                # Loop through and extract company data
                for link in links:
                    company_name = link.inner_text().strip()
                    website_url = link.get_attribute("href").strip()
                    all_companies.append({
                        "company_name": company_name,
                        "website": website_url,
                        "source_category": base_url
                    })

                page_number += 1
                time.sleep(1)  # Delay between pages

            context.close()
        
        browser.close()

    # Save output to JSON
    with open("all_companies.json", "w", encoding="utf-8") as f:
        json.dump(all_companies, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Scraping complete. {len(all_companies)} companies saved to all_companies.json")

if __name__ == "__main__":
    category_links = [
        "https://www.designrush.com/agency/web-development-companies/in/ahmedabad",
        "https://www.designrush.com/agency/software-development/in/ahmedabad",
        "https://www.designrush.com/agency/graphic-design/in/ahmedabad",
        "https://www.designrush.com/agency/digital-marketing/in/ahmedabad",
        "https://www.designrush.com/agency/ui-ux-design/in/ahmedabad",
        "https://www.designrush.com/agency/search-engine-optimization/in/ahmedabad",
        # add more links if needed
    ]
    scrape_designrush_from_links(category_links)
