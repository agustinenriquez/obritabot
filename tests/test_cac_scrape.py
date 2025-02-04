import pytest
import os
import time
from datetime import datetime, timedelta
from backend.cac_scraper import scrape_cac_index, scrape_cac_index_alternative

LAST_RUN_FILE = "tests/last_run_timestamp.txt"

def should_run_test():
    if os.path.exists(LAST_RUN_FILE):
        with open(LAST_RUN_FILE, "r") as f:
            last_run_timestamp = f.read().strip()
            last_run_time = datetime.strptime(last_run_timestamp, "%Y-%m-%d %H:%M:%S")
            if datetime.now() - last_run_time < timedelta(days=1):
                return False
    return True

def update_last_run_timestamp():
    with open(LAST_RUN_FILE, "w") as f:
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def test_scrape_cac_index_alternative():
    if not should_run_test():
        print("Test already run within the last 24 hours. Skipping test.")
        return

    cac_index_alternative = scrape_cac_index_alternative()
    assert cac_index_alternative is not None, "Failed to scrape CAC Index from ikiwi"
    print(f"CAC Index from ikiwi: {cac_index_alternative}")

    update_last_run_timestamp()

if __name__ == "__main__":
    pytest.main()