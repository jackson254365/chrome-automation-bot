#!/usr/bin/env python3
"""
Chrome automation bot using Selenium with webdriver-manager.
This bot:
1. Opens Chrome browser
2. Navigates through website links
3. Scrolls through websites
4. Opens new tabs
5. Repeats the cycle
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
from typing import List

# Website links to visit
WEBSITE_LINKS: List[str] = [
    "https://www.google.com",
    "https://www.wikipedia.org",
    "https://www.github.com",
    "https://www.stackoverflow.com",
    "https://www.python.org",
]

def setup_chrome_driver():
    """Set up Chrome WebDriver with options and webdriver-manager."""
    chrome_options = Options()
    # Uncomment the following line to run headless
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Use webdriver-manager to automatically manage chromedriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def visit_website(driver, link: str):
    """Navigate to a website link."""
    print(f"Visiting: {link}")
    try:
        driver.get(link)
        time.sleep(3)  # Wait for page to load
        print(f"Successfully visited: {link}")
        return True
    except Exception as e:
        print(f"Error visiting {link}: {e}")
        return False

def scroll_page(driver):
    """Scroll through the current webpage."""
    print("Scrolling through webpage...")
    try:
        # Get page height
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        # Scroll down multiple times
        for i in range(5):
            driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
            time.sleep(1)
        
        # Scroll back to top
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        print(f"Scrolling complete. Page height: {last_height} -> {new_height}")
        return True
    except Exception as e:
        print(f"Error scrolling: {e}")
        return False

def open_new_tab(driver):
    """Open a new browser tab."""
    print("Opening new tab...")
    try:
        driver.execute_script("window.open('');")
        # Switch to the new tab
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(1)
        print("New tab opened")
        return True
    except Exception as e:
        print(f"Error opening new tab: {e}")
        return False

def close_current_tab(driver):
    """Close the current browser tab."""
    print("Closing current tab...")
    try:
        if len(driver.window_handles) > 1:
            driver.close()
            # Switch back to main tab
            driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)
        print("Tab closed")
        return True
    except Exception as e:
        print(f"Error closing tab: {e}")
        return False

def main_cycle():
    """Main cycle: visit websites, scroll, open tabs, repeat."""
    print("=" * 50)
    print("Chrome Automation Bot (Selenium with webdriver-manager)")
    print("=" * 50)
    
    driver = setup_chrome_driver()
    
    try:
        # Open Chrome and navigate to first website
        print("Starting bot cycle...")
        
        # Visit each website link
        cycle_count = 0
        
        while True:
            cycle_count += 1
            print(f"\n--- Cycle {cycle_count} ---")
            
            # Visit each website link
            for link in WEBSITE_LINKS:
                if not visit_website(driver, link):
                    continue
                
                # Scroll through the website
                scroll_page(driver)
                
                # Open new tab after visiting
                open_new_tab(driver)
                
                # Random wait between visits
                wait_time = random.uniform(2, 5)
                print(f"Waiting {wait_time:.1f} seconds...")
                time.sleep(wait_time)
            
            # Clean up: close extra tabs, keep main one
            print(f"Cycle {cycle_count} complete. Resetting tabs...")
            
            # Keep only the first tab, close rest
            # But first make sure we have handles to work with
            try:
                handles = driver.window_handles
                print(f"Number of open tabs: {len(handles)}")
                # Close extra tabs (keep the first/main one)
                while len(handles) > 1:
                    driver.switch_to.window(handles[-1])
                    driver.close()
                    handles = driver.window_handles
                # Switch back to main tab
                if driver.window_handles:
                    driver.switch_to.window(driver.window_handles[0])
            except Exception as e:
                print(f"Error during tab cleanup: {e}")
            
            # Wait before starting next full cycle
            cycle_wait = random.uniform(3, 8)
            print(f"Cycle pause for {cycle_wait:.1f} seconds...")
            time.sleep(cycle_wait)
            
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up
        print("Closing browser...")
        try:
            driver.quit()
        except:
            pass
        print("Bot finished.")

if __name__ == "__main__":
    main_cycle()