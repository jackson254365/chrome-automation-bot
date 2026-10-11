#!/usr/bin/env python3
"""
Chrome automation bot that:
1. Opens Chrome browser
2. Clicks on Chrome icon/location
3. Types website links from a predefined list
4. Scrolls through websites
5. Opens new tabs
6. Repeats the cycle
"""

import pyautogui
import time
import subprocess
import os
import sys
from typing import List

# Safety settings - fail-safe will move mouse to corner if you move it to (0,0)
pyautogui.FAIL_SAFE = True
# Set pause between pyautogui actions
pyautogui.PAUSE = 0.5

# Website links to visit
WEBSITE_LINKS: List[str] = [
    "https://www.google.com",
    "https://www.wikipedia.org",
    "https://www.github.com",
    "https://www.stackoverflow.com",
    "https://www.python.org",
]

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()


def open_chrome():
    """Open Google Chrome browser."""
    print("Opening Chrome...")
    try:
        # Try to open Chrome
        subprocess.Popen(["google-chrome-stable"])
        time.sleep(3)
        print("Chrome opened successfully")
        return True
    except Exception as e:
        print(f"Error opening Chrome: {e}")
        return False


def click_chrome_icon():
    """Click on Chrome icon to focus it."""
    print("Clicking Chrome icon...")
    # Try to locate Chrome icon - use screen coordinates or image recognition
    # Move to a reasonable position and click
    try:
        # Click at center screen or try to find Chrome icon
        # Here we'll just click at a position that typically has Chrome
        # You may need to adjust these coordinates based on your setup
        chrome_button_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pyautogui.click(chrome_button_pos[0], chrome_button_pos[1])
        time.sleep(2)
        print("Clicked Chrome icon position")
        return True
    except Exception as e:
        print(f"Error clicking Chrome icon: {e}")
        return False


def search_and_visit(link: str):
    """Search for a website link and visit it."""
    print(f"Visiting: {link}")
    try:
        # Focus on address bar (Cmd+L on Mac, Ctrl+L on Linux/Windows)
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(0.5)
        
        # Select all and type new URL
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.3)
        
        # Type the website link
        pyautogui.write(link, interval=0.1)
        time.sleep(0.5)
        
        # Press Enter to go
        pyautogui.press('enter')
        time.sleep(3)
        print(f"Visited: {link}")
        return True
    except Exception as e:
        print(f"Error visiting {link}: {e}")
        return False


def scroll_website():
    """Scroll through the current website."""
    print("Scrolling through website...")
    try:
        # Scroll down multiple times
        for i in range(5):
            pyautogui.scroll(-200)  # Negative = down
            time.sleep(1)
        
        # Scroll back up
        for i in range(5):
            pyautogui.scroll(200)   # Positive = up
            time.sleep(1)
            
        print("Website scrolling complete")
        return True
    except Exception as e:
        print(f"Error scrolling: {e}")
        return False


def open_new_tab():
    """Open a new browser tab."""
    print("Opening new tab...")
    try:
        pyautogui.hotkey('ctrl', 't')
        time.sleep(1)
        print("New tab opened")
        return True
    except Exception as e:
        print(f"Error opening new tab: {e}")
        return False


def close_current_tab():
    """Close the current browser tab."""
    print("Closing current tab...")
    try:
        pyautogui.hotkey('ctrl', 'w')
        time.sleep(1)
        print("Tab closed")
        return True
    except Exception as e:
        print(f"Error closing tab: {e}")
        return False


def wait_random():
    """Wait a random amount of time between cycles."""
    import random
    wait_time = random.uniform(3, 8)
    print(f"Waiting {wait_time:.1f} seconds before next cycle...")
    time.sleep(wait_time)


def main_cycle():
    """Main cycle: open Chrome, visit websites, scroll, repeat."""
    print("=" * 50)
    print("Starting Chrome Automation Bot")
    print("=" * 50)
    
    # Open Chrome
    if not open_chrome():
        print("Failed to open Chrome, retrying...")
        if not open_chrome():
            print("Could not open Chrome, exiting.")
            return
    
    # Click to focus Chrome
    click_chrome_icon()
    
    cycle_count = 0
    
    try:
        while True:
            cycle_count += 1
            print(f"\n--- Cycle {cycle_count} ---")
            
            # Visit each website link
            for link in WEBSITE_LINKS:
                # Check fail-safe
                if pyautogui.onScreenFailure():
                    print("Fail-safe triggered, exiting.")
                    return
                
                if not search_and_visit(link):
                    print(f"Skipping {link} due to error")
                    continue
                
                # Scroll through the website
                scroll_website()
                
                # Open a new tab after visiting
                open_new_tab()
                
                # Small delay between visits
                wait_random()
            
            # Close extra tabs (keep only one)
            # Count open tabs and close extras
            print(f"Cycle {cycle_count} complete. Restarting...")
            
            # Wait before starting next full cycle
            wait_random()
            
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main_cycle()