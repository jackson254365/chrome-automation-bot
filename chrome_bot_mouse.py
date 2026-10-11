#!/usr/bin/env python3
"""
Chrome automation bot with mouse pointer interactions.
This bot simulates human-like mouse and keyboard input using pyautogui.
Works on both Windows and Linux.

Features:
- Opens Chrome browser
- Clicks Chrome icon using mouse
- Types website links using keyboard
- Clicks close button on tabs using mouse
- Scrolls with mouse
- Opens new tabs with mouse
- Human-like mouse movements and delays
"""

import pyautogui
import subprocess
import time
import random
import os
import sys
from typing import List

# Safety settings - fail-safe will move mouse to corner if you move it to (0,0)
pyautogui.FAIL_SAFE = True
# Set pause between pyautogui actions
pyautogui.PAUSE = 0.1

# Website links to visit
WEBSITE_LINKS: List[str] = [
    "https://www.google.com",
    "https://www.wikipedia.org",
    "https://www.github.com",
    "https://www.stackoverflow.com",
    "https://www.python.org",
]

# Platform-specific Chrome paths
CHROME_PATHS = {
    "linux": ["google-chrome-stable", "google-chrome", "chromium-browser", "chromium"],
    "windows": ["chrome.exe"],
    "darwin": ["google-chrome", "Google Chrome"],
}


def detect_platform():
    """Detect the operating system."""
    return sys.platform


def get_chrome_command():
    """Get the command to open Chrome based on platform."""
    platform = detect_platform()
    chrome_paths = CHROME_PATHS.get(platform, CHROME_PATHS["linux"])
    
    for path in chrome_paths:
        if subprocess.run(["which", path], capture_output=True).returncode == 0:
            return path
    
    # Fallback: just try "google-chrome"
    return "google-chrome-stable"


def human_move_to(x, y, duration=None):
    """Move mouse to position with human-like movement."""
    if duration is None:
        # Random duration between 0.5-2.5 seconds
        duration = random.uniform(0.5, 2.5)
    pyautogui.moveTo(x, y, duration=duration)


def human_click(x=None, y=None, clicks=1, interval=0.1):
    """Human-like mouse click."""
    if x is not None and y is not None:
        human_move_to(x, y)
    time.sleep(random.uniform(0.1, 0.5))
    pyautogui.click(x=x, y=y, clicks=clicks, interval=interval)


def human_type(text, interval=None):
    """Human-like typing with random delays."""
    if interval is None:
        interval = random.uniform(0.05, 0.2)
    pyautogui.write(text, interval=interval)


def get_screen_size():
    """Get screen dimensions."""
    return pyautogui.size()


def find_chrome_window():
    """Try to locate and focus Chrome window."""
    screen_w, screen_h = get_screen_size()
    
    # Try clicking at various Chrome-related positions
    # These are approximate - users may need to adjust
    
    # Option 1: Click near center of screen
    human_click(x=screen_w // 2, y=screen_h // 2, duration=1.0)
    
    # Option 2: Try clicking at typical taskbar/dock area
    # Bottom center (Windows taskbar) or bottom left (Linux dock)
    human_click(x=screen_w // 4, y=screen_h - 50, duration=0.8)
    time.sleep(1)
    
    human_click(x=screen_w // 2, y=screen_h - 50, duration=0.8)
    time.sleep(1)


def click_chrome_icon_mouse():
    """Click Chrome icon using mouse pointer."""
    print("Clicking Chrome icon with mouse...")
    screen_w, screen_h = get_screen_size()
    
    # Try multiple positions to find Chrome
    positions = [
        # Center of screen
        (screen_w // 2, screen_h // 2),
        # Top left
        (50, 50),
        # Top right
        (screen_w - 50, 50),
        # Bottom left
        (50, screen_h - 50),
        # Bottom right
        (screen_w - 50, screen_h - 50),
        # Taskbar area (bottom center)
        (screen_w // 2, screen_h - 30),
    ]
    
    for i, (x, y) in enumerate(positions):
        print(f"  Trying position {i+1}: ({x}, {y})")
        human_move_to(x, y, duration=0.8)
        time.sleep(0.5)
        human_click(x=x, y=y, clicks=1)
        time.sleep(3)  # Wait for response
        
        # Check if Chrome seems to be opening (we can't easily detect this,
        # so we just try and hope)
        print(f"  Position {i+1} clicked, waiting...")
    
    # Final attempt at center
    human_click(x=screen_w // 2, y=screen_h // 2, duration=1.0)
    time.sleep(3)
    print("Chrome icon click attempt complete")


def visit_website_with_keyboard(url):
    """Visit a website by typing the URL with keyboard."""
    print(f"Visiting: {url} (using keyboard)")
    try:
        # Focus address bar - Ctrl+L on Linux/Windows, Cmd+L on Mac
        if detect_platform() == "darwin":
            pyautogui.hotkey('command', 'l')
        else:
            pyautogui.hotkey('ctrl', 'l')
        time.sleep(0.5)
        
        # Select all address
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.3)
        
        # Type the URL with human-like delays
        human_type(url, interval=0.1)
        time.sleep(0.5)
        
        # Press Enter
        pyautogui.press('enter')
        time.sleep(3)
        print(f"Successfully visited: {url}")
        return True
    except Exception as e:
        print(f"Error visiting {url}: {e}")
        return False


def scroll_with_mouse():
    """Scroll through webpage using mouse wheel."""
    print("Scrolling with mouse...")
    try:
        screen_w, screen_h = get_screen_size()
        
        # Move mouse to a position and scroll
        human_move_to(screen_w // 2, screen_h // 2, duration=0.8)
        
        # Scroll down multiple times with human-like intervals
        for i in range(4):
            pyautogui.scroll(-150)  # Negative = down
            time.sleep(random.uniform(0.5, 1.5))
        
        # Scroll back up
        for i in range(4):
            pyautogui.scroll(150)   # Positive = up
            time.sleep(random.uniform(0.5, 1.5))
        
        print("Mouse scrolling complete")
        return True
    except Exception as e:
        print(f"Error scrolling: {e}")
        return False


def open_tab_with_mouse():
    """Open new tab using mouse (Ctrl+T or clicking plus button)."""
    print("Opening new tab with mouse...")
    try:
        # Method 1: Keyboard shortcut Ctrl+T
        pyautogui.hotkey('ctrl', 't')
        time.sleep(1)
        print("Tab opened via keyboard shortcut")
        return True
    except Exception as e:
        print(f"Error opening tab: {e}")
        return False


def close_tab_with_mouse():
    """Close current tab using mouse to click close button."""
    print("Closing tab with mouse...")
    try:
        screen_w, screen_h = get_screen_size()
        
        # Move mouse to close button area (top right of tab)
        # Close button is typically in the tab area or top right corner
        
        # Option 1: Click top right corner of browser
        human_click(x=screen_w - 30, y=40, clicks=1)
        time.sleep(1)
        
        # Option 2: Try clicking on the tab close area
        human_click(x=screen_w - 50, y=80, clicks=1)
        time.sleep(1)
        
        print("Tab close attempt complete")
        return True
    except Exception as e:
        print(f"Error closing tab with mouse: {e}")
        return False


def main_cycle():
    """Main cycle: visit websites with human-like mouse/keyboard input."""
    print("=" * 60)
    print("Chrome Automation Bot - Mouse & Keyboard Simulation")
    print("=" * 60)
    print(f"Platform: {detect_platform()}")
    print(f"Website links to visit: {len(WEBSITE_LINKS)}")
    print("Move your mouse to any corner to trigger fail-safe and exit!")
    print()
    
    # Open Chrome
    print("Opening Chrome browser...")
    chrome_cmd = get_chrome_command()
    print(f"Using command: {chrome_cmd}")
    
    try:
        subprocess.Popen([chrome_cmd])
        time.sleep(3)
    except Exception as e:
        print(f"Attempting to open Chrome anyway... Error: {e}")
    
    time.sleep(2)
    
    # Try to find/focus Chrome
    find_chrome_window()
    
    cycle_count = 0
    
    try:
        while True:
            cycle_count += 1
            print(f"\n{'='*60}")
            print(f"CYCLE {cycle_count}")
            print(f"{'='*60}")
            
            # Visit each website link
            for i, link in enumerate(WEBSITE_LINKS):
                if pyautogui.onFailSafe():
                    print("Fail-safe triggered! Mouse moved to corner.")
                    return
                
                print(f"\n--- Visiting link {i+1}/{len(WEBSITE_LINKS)}: {link} ---")
                
                # Human-like mouse movement before visiting
                screen_w, screen_h = get_screen_size()
                human_move_to(screen_w // 2, screen_h // 2, duration=random.uniform(0.5, 1.5))
                time.sleep(random.uniform(0.5, 1.0))
                
                # Visit website using keyboard input
                success = visit_website_with_keyboard(link)
                
                if not success:
                    print(f"Failed to visit {link}, continuing...")
                    continue
                
                # Scroll with mouse
                scroll_with_mouse()
                
                # Open new tab with mouse
                open_tab_with_mouse()
                
                # Random wait between visits
                wait_time = random.uniform(2, 5)
                print(f"Waiting {wait_time:.1f} seconds before next...")
                time.sleep(wait_time)
            
            # Close extra tabs with mouse
            print(f"\nCycle {cycle_count} complete. Closing extra tabs...")
            try:
                # Move mouse to close area and click
                screen_w, screen_h = get_screen_size()
                for _ in range(len(WEBSITE_LINKS) - 1):
                    close_tab_with_mouse()
                    time.sleep(0.5)
            except:
                pass
            
            # Longer pause before next cycle
            cycle_pause = random.uniform(3, 8)
            print(f"Pausing for {cycle_pause:.1f} seconds...")
            time.sleep(cycle_pause)
            
    except KeyboardInterrupt:
        print("\n\nBot stopped by user. Goodbye!")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Bot session ended.")


if __name__ == "__main__":
    main_cycle()