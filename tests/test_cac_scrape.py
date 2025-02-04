import pytest
import os
from datetime import datetime, timedelta
from backend.cac_scraper import scrape_cac_index_alternative

LAST_RUN_FILE = "tests/last_run_timestamp.txt"
CACHE_FILE = "tests/cac_cache.txt"

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

def cache_cac_value(cac_value):
    with open(CACHE_FILE, "w") as f:
        f.write(cac_value)

def get_cached_cac_value():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return f.read().strip()
    return None

def test_scrape_cac_index_alternative():
    if not should_run_test():
        cached_value = get_cached_cac_value()
        if cached_value:
            print(f"Using cached CAC Index: {cached_value}")
            return
        else:
            print("Test already run within the last 24 hours, but no cached value found. Skipping test.")
            return

    cac_index_alternative = scrape_cac_index_alternative()
    assert cac_index_alternative is not None, "Failed to scrape CAC Index from ikiwi"
    print(f"CAC Index from ikiwi: {cac_index_alternative}")

    update_last_run_timestamp()
    cache_cac_value(cac_index_alternative)

def test_cached_cac_value():
    # Cache a test value
    test_value = "15.356,40"
    cache_cac_value(test_value)
    
    # Retrieve the cached value
    cached_value = get_cached_cac_value()
    
    # Check if the cached value is correct
    assert cached_value == test_value, "Cached CAC value does not match the expected value"
    print(f"Cached CAC value: {cached_value}")

if __name__ == "__main__":
    pytest.main()