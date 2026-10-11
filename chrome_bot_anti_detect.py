#!/usr/bin/env python3
"""
Chrome automation bot with mouse/keyboard simulation and anti-detection.
Uses Selenium with ChromeDriver anti-detection + pyautogui for human-like mouse input.
Works on both Windows and Linux.
"""

import time
import random
import sys
import subprocess
from typing import List

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pyautogui

# ===== ANTI-DETECTION SETTINGS =====
# These options help hide the bot from Chrome's detection systems

# Website links to visit
WEBSITE_LINKS: List[str] = [
    "https://www.google.com",
    "https://www.wikipedia.org",
    "https://www.github.com",
    "https://www.stackoverflow.com",
    "https://www.python.org",
]

# Random human-like delays
HUMAN_MIN_DELAY = 0.5
HUMAN_MAX_DELAY = 2.0

# ===== ANTI-DETECTION HELPER =====
def anti_detect(driver):
    """Apply anti-detection scripts to hide bot automation."""
    try:
        # Execute script to remove webdriver property
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            """
        })
        print("Anti-detection scripts applied")
    except Exception as e:
        print(f"Note: Could not apply all anti-detection: {e}")


def random_delay():
    """Pause for a human-like random amount of time."""
    time.sleep(random.uniform(HUMAN_MIN_DELAY, HUMAN_MAX_DELAY))


def move_mouse_smooth(x, y, duration=None):
    """Move mouse to position with smooth, human-like motion."""
    if duration is None:
        duration = random.uniform(0.5, 2.0)
    pyautogui.moveTo(x, y, duration=duration)


def human_click(x=None, y=None, clicks=1):
    """Human-like mouse click with movement and delay."""
    if x is not None and y is not None:
        move_mouse_smooth(x, y)
    random_delay()
    pyautogui.click(clicks=clicks)


def human_type(text, interval=None):
    """Type text with human-like delays between keystrokes."""
    if interval is None:
        interval = random.uniform(0.05, 0.2)
    pyautogui.write(text, interval=interval)


# ===== BROWSER SETUP =====
def setup_chrome_driver():
    """Set up Chrome WebDriver with anti-detection options."""
    chrome_options = Options()
    
    # Anti-detection arguments
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # User agent randomization (basic)
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Exclude automated control
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    # Set preferences to reduce automation flags
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2,
        "profile.managed_default_content_settings.images": 2,
    })
    
    # Install and set up chromedriver automatically
    service = Service(ChromeDriverManager().install())
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Apply additional anti-detection JS
    anti_detect(driver)
    
    return driver


# ===== WEB ACTIONS =====
def visit_website(driver, url):
    """Navigate to a website with human-like behavior."""
    print(f"Visiting: {url}")
    try:
        driver.get(url)
        random_delay()
        print(f"  Loaded: {url}")
        return True
    except Exception as e:
        print(f"  Error visiting {url}: {e}")
        return False


def scroll_page_mouse(driver):
    """Scroll page using mouse wheel with human-like patterns."""
    print("  Scrolling with mouse...")
    try:
        # Get current position
        driver.execute_script("window.scrollTo(0, 0);")
        random_delay()
        
        # Scroll down in chunks
        for _ in range(3):
            pyautogui.scroll(-200)
            random_delay()
        
        # Scroll up
        for _ in range(3):
            pyautogui.scroll(200)
            random_delay()
        
        print("  Mouse scrolling complete")
        return True
    except Exception as e:
        print(f"  Error scrolling: {e}")
        return False


def click_close_button_mouse():
    """Close tab by clicking the close button with mouse."""
    try:
        screen_w, screen_h = pyautogui.size()
        
        # Move to top-right area where close button typically is
        # Adjust these coordinates based on your screen setup
        human_click(x=screen_w - 40, y=40, clicks=1)
        random_delay()
        print("  Mouse click on close button")
        return True
    except Exception as e:
        print(f"  Error clicking close button: {e}")
        return False


def open_new_tab_mouse():
    """Open new tab using mouse (clicking + button or Ctrl+T)."""
    try:
        # Method: Keyboard shortcut Ctrl+T (more reliable)
        human_keyboard_shortcut('ctrl', 't')
        random_delay()
        print("  New tab opened")
        return True
    except Exception as e:
        print(f"  Error opening new tab: {e}")
        return False


def human_keyboard_shortcut(*keys):
    """Press a keyboard shortcut with human-like timing."""
    pyautogui.hotkey(*keys)


# ===== MAIN CYCLE =====
def find_and_focus_chrome():
    """Try to find and focus Chrome browser."""
    print("Finding and focusing Chrome...")
    random_delay()
    
    # Click at center to try to focus
    screen_w, screen_h = pyautogui.size()
    human_click(x=screen_w // 2, y=screen_h // 2, clicks=1)
    random_delay()
    
    # Type Ctrl+L to focus address bar (Linux/Windows)
    human_keyboard_shortcut('ctrl', 'l')
    random_delay()
    
    return True


def main_cycle():
    """Main automation cycle."""
    print("=" * 60)
    print("Chrome Automation Bot - Anti-Detection + Mouse/Keyboard")
    print("=" * 60)
    print(f"Platform: {sys.platform}")
    print(f"Website links: {len(WEBSITE_LINKS)}")
    print("Move mouse to corner to trigger fail-safe and exit!")
    print()
    
    # Open Chrome browser
    print("Opening Chrome...")
    chrome_cmd = "google-chrome-stable" if sys.platform != "win32" else "chrome.exe"
    try:
        subprocess.Popen([chrome_cmd])
        print(f"  Started: {chrome_cmd}")
    except Exception as e:
        print(f"  Could not start Chrome directly: {e}")
    
    random_delay()
    random_delay()
    
    # Try to focus Chrome
    find_and_focus_chrome()
    
    driver = setup_chrome_driver()
    cycle_count = 0
    
    try:
        while True:
            cycle_count += 1
            print(f"\n{'='*60}")
            print(f"CYCLE {cycle_count}")
            print(f"{'='*60}")
            
            # Visit each website link
            for i, link in enumerate(WEBSITE_LINKS):
                # Check fail-safe manually - check if mouse is at (0,0)
                try:
                    mouse_x, mouse_y = pyautogui.position()
                    if mouse_x == 0 and mouse_y == 0:
                        print("  Fail-safe triggered! Mouse at corner.")
                        return
                except Exception:
                    pass
                
                print(f"\n  --- Link {i+1}/{len(WEBSITE_LINKS)}: {link} ---")
                
                # Human-like mouse movement before action
                screen_w, screen_h = pyautogui.size()
                move_mouse_smooth(screen_w // 2, screen_h // 2, duration=random.uniform(0.5, 1.5))
                random_delay()
                
                # Visit website
                success = visit_website(driver, link)
                if not success:
                    print(f"  Skipping {link}")
                    continue
                
                # Scroll with mouse
                scroll_page_mouse(driver)
                
                # Open new tab with mouse
                open_new_tab_mouse()
                
                # Random wait between visits
                wait_time = random.uniform(2, 5)
                print(f"  Waiting {wait_time:.1f}s before next...")
                random_delay()
                time.sleep(wait_time)
            
            # Close extra tabs with mouse
            print(f"\n  Cycle {cycle_count} complete. Cleaning up tabs...")
            try:
                for _ in range(len(WEBSITE_LINKS) - 1):
                    click_close_button_mouse()
                    random_delay()
            except Exception as e:
                print(f"  Tab cleanup note: {e}")
            
            # Longer pause before next cycle
            cycle_pause = random.uniform(3, 8)
            print(f"  Pausing for {cycle_pause:.1f} seconds...")
            random_delay()
            time.sleep(cycle_pause)
            
    except KeyboardInterrupt:
        print("\n\nBot stopped by user. Goodbye!")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Closing browser...")
        try:
            driver.quit()
        except:
            pass
        print("Bot session ended.")


if __name__ == "__main__":
    main_cycle()