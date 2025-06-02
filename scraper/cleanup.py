import os
import json
from datetime import datetime, timedelta
import logging
import shutil

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cleanup.log'),
        logging.StreamHandler()
    ]
)

def cleanup_old_files(days_to_keep=7):
    """Clean up old job files and logs."""
    try:
        # Get current date
        today = datetime.now()
        
        # Get all job files
        job_files = [f for f in os.listdir('.') if f.startswith('scraped_jobs_') and f.endswith('.json')]
        
        # Get all log files
        log_files = [f for f in os.listdir('.') if f.endswith('.log')]
        
        deleted_files = []
        
        # Clean up job files
        for file in job_files:
            try:
                # Extract date from filename
                date_str = file.split('_')[2].split('.')[0]
                file_date = datetime.strptime(date_str, '%Y-%m-%d')
                
                # Check if file is older than days_to_keep
                if (today - file_date).days > days_to_keep:
                    os.remove(file)
                    deleted_files.append(file)
                    logging.info(f"Deleted old job file: {file}")
            except Exception as e:
                logging.error(f"Error processing file {file}: {str(e)}")
        
        # Clean up log files (keep last 30 days)
        for file in log_files:
            try:
                file_date = datetime.fromtimestamp(os.path.getmtime(file))
                if (today - file_date).days > 30:
                    os.remove(file)
                    deleted_files.append(file)
                    logging.info(f"Deleted old log file: {file}")
            except Exception as e:
                logging.error(f"Error processing log file {file}: {str(e)}")
        
        return deleted_files
        
    except Exception as e:
        logging.error(f"Error during cleanup: {str(e)}")
        return []

if __name__ == "__main__":
    logging.info("Starting cleanup process")
    deleted_files = cleanup_old_files()
    logging.info(f"Cleanup completed. Deleted {len(deleted_files)} files.") 