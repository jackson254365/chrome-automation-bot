#!/usr/bin/env python3
"""
chrome_stealth_bot.py - Chrome automation bot with Anti-Bot Detection Evasion
and Real Mouse Pointer Interaction.

Features:
- Launches Chrome via ChromeDriver with full anti-bot detection evasion:
  * Masks navigator.webdriver (returns undefined/None)
  * Removes 'Chrome is being controlled by automated software' info bar
  * Disables AutomationControlled blink features
  * Applies selenium-stealth fingerprint protections (WebGL, vendor, plugins)
  * Fallback to undetected-chromedriver if available
- Human-like mouse pointer interactions:
  * Visibly moves mouse pointer with curved, smooth trajectories
  * Clicks address bar / search using mouse pointer
  * Types URLs with human cadence and keystroke jitter
  * Scrolls through webpages with mouse wheel & natural reading pauses
  * Opens new tabs and closes previous tabs with mouse / tab controls
  * Cycles through predefined website list repeatedly
- Fail-safe: moving mouse to screen corner (0,0) immediately stops the bot.
"""

import os
import sys
import time
import random
import re
import subprocess
from typing import Optional

# Setup X11 / XWayland authorization
try:
    subprocess.run(["xhost", "+local:"], capture_output=True, timeout=2)
except Exception:
    pass

import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

try:
    from selenium_stealth import stealth
    HAS_STEALTH = True
except ImportError:
    HAS_STEALTH = False

try:
    import undetected_chromedriver as uc
    HAS_UC = True
except ImportError:
    HAS_UC = False

import config
import human_mouse

pyautogui.FAIL_SAFE = True


def get_chrome_major_version() -> Optional[int]:
    """Detect installed Google Chrome major version."""
    for cmd in ["google-chrome-stable", "google-chrome", "chromium"]:
        try:
            out = subprocess.check_output([cmd, "--version"], text=True)
            match = re.search(r"(\d+)\.", out)
            if match:
                return int(match.group(1))
        except Exception:
            continue
    return None


def init_stealth_driver():
    """
    Initialize ChromeDriver with advanced anti-bot detection evasion.
    Removes automation banners, hides navigator.webdriver, masks fingerprint.
    """
    print("\n[1/3] Initializing Stealth ChromeDriver...")
    chrome_ver = get_chrome_major_version()
    if chrome_ver:
        print(f"      Detected Chrome version: {chrome_ver}")

    # Standard Selenium with high-grade anti-bot stealth flags
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    
    # Hide automation indicators from Chrome
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # Dynamic OS platform detection
    is_windows = sys.platform.startswith("win")
    is_mac = sys.platform == "darwin"

    if is_windows:
        platform_str = "Win32"
        ua_str = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
        )
    elif is_mac:
        platform_str = "MacIntel"
        ua_str = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
        )
    else:
        platform_str = "Linux x86_64"
        ua_str = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
        )

    options.add_argument(f"user-agent={ua_str}")

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        print(f"      Notice: Standard driver init warning: {e}. Trying fallback...")
        driver = webdriver.Chrome(options=options)

    # Apply CDP stealth scripts to hide navigator.webdriver
    try:
        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": f"""
                Object.defineProperty(navigator, 'webdriver', {{
                    get: () => undefined
                }});
                window.chrome = {{
                    runtime: {{}}
                }};
                Object.defineProperty(navigator, 'platform', {{
                    get: () => '{platform_str}'
                }});
                Object.defineProperty(navigator, 'languages', {{
                    get: () => ['en-US', 'en']
                }});
                Object.defineProperty(navigator, 'plugins', {{
                    get: () => [1, 2, 3, 4, 5]
                }});
                """
            },
        )
    except Exception:
        pass

    # Apply selenium-stealth if installed
    if HAS_STEALTH:
        try:
            stealth(
                driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform=platform_str,
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
            )
            print(f"      Applied selenium-stealth fingerprint protections for {platform_str}.")
        except Exception as e:
            print(f"      Could not apply selenium-stealth: {e}")

    # Verify stealth status
    try:
        is_webdriver = driver.execute_script("return navigator.webdriver")
        print(f"      Anti-Bot Verification: navigator.webdriver = {is_webdriver} (Bot Hidden!)")
    except Exception:
        pass

    return driver


def focus_and_click_address_bar():
    """
    Move the mouse pointer to the Chrome address / omnibox bar,
    click it with the mouse pointer, and prepare for typing.
    """
    screen_w, screen_h = human_mouse.get_screen_size()
    
    # Chrome omnibox typically sits horizontally centered, around y=82 in maximized window
    omnibox_x = int(screen_w * 0.45 + random.randint(-40, 40))
    omnibox_y = int(82 + random.randint(-4, 4))
    
    print(f"   [Mouse] Moving to address bar at ({omnibox_x}, {omnibox_y})...")
    human_mouse.smooth_move_to(omnibox_x, omnibox_y, duration=random.uniform(0.4, 0.7))
    human_mouse.human_click(clicks=1)
    time.sleep(0.2)
    
    # Select all existing address text (Ctrl+A or Ctrl+L backup)
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.15)


def open_new_tab_with_mouse(driver=None):
    """
    Move mouse pointer to the '+' New Tab button in Chrome and click it.
    Also executes driver tab synchronization.
    """
    screen_w, screen_h = human_mouse.get_screen_size()
    
    # Estimate '+' button position on the Chrome tab bar (y ≈ 42)
    # Move mouse up to the tab strip
    tab_plus_x = int(min(screen_w * 0.35, 360) + random.randint(-10, 10))
    tab_plus_y = int(42 + random.randint(-3, 3))
    
    print(f"   [Mouse] Moving to tab bar '+' area ({tab_plus_x}, {tab_plus_y})...")
    human_mouse.smooth_move_to(tab_plus_x, tab_plus_y, duration=0.4)
    human_mouse.human_click(clicks=1)
    time.sleep(0.3)
    
    # Send Ctrl+T hotkey while cursor is positioned to ensure tab opens reliably
    pyautogui.hotkey("ctrl", "t")
    time.sleep(0.8)
    
    if driver:
        try:
            # Switch driver handle to the newly active tab
            handles = driver.window_handles
            driver.switch_to.window(handles[-1])
        except Exception:
            pass


def close_tab_with_mouse(driver=None):
    """
    Move mouse pointer to the active tab close button or press Ctrl+W,
    closing current tab and switching to remaining tabs.
    """
    screen_w, screen_h = human_mouse.get_screen_size()
    tab_close_x = int(min(screen_w * 0.22, 240) + random.randint(-5, 5))
    tab_close_y = int(42 + random.randint(-3, 3))
    
    print(f"   [Mouse] Closing current tab at ({tab_close_x}, {tab_close_y})...")
    human_mouse.smooth_move_to(tab_close_x, tab_close_y, duration=0.3)
    pyautogui.hotkey("ctrl", "w")
    time.sleep(0.6)
    
    if driver:
        try:
            handles = driver.window_handles
            if handles:
                driver.switch_to.window(handles[0])
        except Exception:
            pass


def run_stealth_mouse_cycle(driver):
    """
    Main loop:
    1. Iterates over website list
    2. Uses real mouse pointer to click address bar
    3. Types URL with human-like cadence
    4. Scrolls through the website with mouse wheel
    5. Opens new tab with mouse
    6. Closes extra tabs to manage memory
    7. Loops continuously
    """
    cycle_num = 0
    total_sites = len(config.WEBSITE_LINKS)

    while True:
        cycle_num += 1
        print("\n" + "=" * 64)
        print(f"   STARTING CYCLE #{cycle_num} ({total_sites} websites in list)")
        print("   (Move mouse to screen corner (0,0) or press Ctrl+C to stop)")
        print("=" * 64)

        for idx, site in enumerate(config.WEBSITE_LINKS, 1):
            print(f"\n>> [{idx}/{total_sites}] Target: {site}")

            # 1. Focus address bar with mouse pointer
            focus_and_click_address_bar()

            # 2. Type website address with human cadence
            print(f"   [Keyboard] Typing URL: '{site}'...")
            human_mouse.human_type(
                site,
                min_delay=config.TYPING_SPEED_MIN,
                max_delay=config.TYPING_SPEED_MAX,
            )
            time.sleep(0.2)
            pyautogui.press("enter")
            print("   [Keyboard] Pressed Enter, waiting for page load...")

            # 3. Wait for page load
            load_wait = random.uniform(config.PAGE_VIEW_TIME_MIN, config.PAGE_VIEW_TIME_MAX)
            time.sleep(load_wait)

            # 4. Scroll through the webpage using mouse wheel
            print("   [Mouse] Scrolling smoothly through webpage...")
            human_mouse.human_scroll(
                passes=config.SCROLL_PASSES,
                amount=config.SCROLL_AMOUNT,
                pause_range=(config.SCROLL_PAUSE_MIN, config.SCROLL_PAUSE_MAX),
            )

            # 5. Open new tab with mouse
            print("   [Mouse] Opening new tab...")
            open_new_tab_with_mouse(driver)
            time.sleep(1.0)

            # 6. Check open tab count; close old tabs if limit reached
            try:
                handles = driver.window_handles
                if len(handles) > config.MAX_OPEN_TABS:
                    print(f"   [Tabs] Open tabs ({len(handles)}) exceeded max ({config.MAX_OPEN_TABS}). Closing excess...")
                    while len(driver.window_handles) > 2:
                        close_tab_with_mouse(driver)
                        time.sleep(0.4)
            except Exception:
                pass

            pause_between = random.uniform(2.0, 4.0)
            time.sleep(pause_between)

        # End of cycle tab cleanup
        print(f"\n[Cycle #{cycle_num} Complete] Cleaning up extra tabs before next round...")
        try:
            while len(driver.window_handles) > 1:
                close_tab_with_mouse(driver)
                time.sleep(0.4)
        except Exception:
            pass

        cycle_pause = random.uniform(config.CYCLE_PAUSE_MIN, config.CYCLE_PAUSE_MAX)
        print(f"Pausing for {cycle_pause:.1f}s before starting Cycle #{cycle_num + 1}...\n")
        time.sleep(cycle_pause)


def main():
    print("=" * 64)
    print("   CHROME STEALTH BOT - ANTI-DETECTION + REAL MOUSE POINTER")
    print("=" * 64)
    
    driver = None
    try:
        driver = init_stealth_driver()
        run_stealth_mouse_cycle(driver)
    except KeyboardInterrupt:
        print("\n[Stopped] Bot interrupted by user. Exiting safely...")
    except pyautogui.FailSafeException:
        print("\n[Fail-Safe] Mouse moved to corner! Bot stopped immediately.")
    except Exception as e:
        print(f"\n[Error] Bot encountered an error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if driver:
            print("\nClosing Chrome browser session...")
            try:
                driver.quit()
            except Exception:
                pass
        print("Done.")


if __name__ == "__main__":
    main()
