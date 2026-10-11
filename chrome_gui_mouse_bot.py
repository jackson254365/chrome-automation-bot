#!/usr/bin/env python3
"""
chrome_gui_mouse_bot.py - Pure Desktop GUI Mouse Automation Bot.

Features:
1. Opens Chrome by clicking the application launcher / Activities menu,
   searching 'google-chrome' via keyboard, and clicking the Chrome icon with the mouse pointer.
2. Focuses and clicks the address bar using the mouse pointer.
3. Types website links from the configured list.
4. Scrolls smoothly through each website using the mouse wheel.
5. Opens new tabs with the mouse pointer.
6. Closes tabs with the mouse pointer.
7. Repeats the loop continuously over all links.
"""

import sys
import time
import random
import subprocess
import os

# Ensure X11/XWayland display authorization
try:
    subprocess.run(["xhost", "+local:"], capture_output=True, timeout=2)
except Exception:
    pass

import pyautogui
import config
import human_mouse

pyautogui.FAIL_SAFE = True


def launch_chrome_via_mouse_search():
    """
    Open Chrome by:
    1. Clicking Activities / App Launcher (or pressing Super key).
    2. Typing 'google-chrome' into the search field.
    3. Moving the mouse pointer over the Chrome icon and clicking it.
    """
    print("\n[Launcher] Step 1: Opening Application Search Launcher...")
    screen_w, screen_h = human_mouse.get_screen_size()

    # Move mouse to GNOME top-left Activities corner and click
    print("   [Mouse] Moving to top-left corner (Activities)...")
    human_mouse.smooth_move_to(20, 15, duration=0.5)
    human_mouse.human_click()
    time.sleep(1.0)

    # Search for Chrome in the launcher
    print("   [Keyboard] Typing search query: 'google-chrome'...")
    human_mouse.human_type("google-chrome", min_delay=0.05, max_delay=0.1)
    time.sleep(1.2)

    # In GNOME, the top search result appears in the upper center area
    # typically around x = screen_w // 2, y ≈ screen_h * 0.28
    result_x = int(screen_w // 2 + random.randint(-20, 20))
    result_y = int(screen_h * 0.28 + random.randint(-10, 10))

    print(f"   [Mouse] Moving to Chrome search result icon at ({result_x}, {result_y})...")
    human_mouse.smooth_move_to(result_x, result_y, duration=0.6)
    time.sleep(0.3)
    human_mouse.human_click(clicks=1)
    print("   [Mouse] Clicked Chrome icon!")
    
    # Also press enter as insurance in case cursor was slightly off the icon center
    time.sleep(0.4)
    pyautogui.press("enter")
    
    print("   Waiting for Chrome browser window to appear...")
    time.sleep(4.0)


def click_and_type_url(url: str):
    """
    Move mouse to Chrome address bar, click, and type the URL.
    """
    screen_w, screen_h = human_mouse.get_screen_size()
    
    # Address bar coordinates in maximized window
    addr_x = int(screen_w * 0.45 + random.randint(-30, 30))
    addr_y = int(82 + random.randint(-4, 4))

    print(f"   [Mouse] Clicking address bar at ({addr_x}, {addr_y})...")
    human_mouse.smooth_move_to(addr_x, addr_y, duration=0.5)
    human_mouse.human_click()
    time.sleep(0.2)
    
    # Ensure URL bar is focused and selected
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.15)
    
    print(f"   [Keyboard] Typing URL: '{url}'...")
    human_mouse.human_type(
        url,
        min_delay=config.TYPING_SPEED_MIN,
        max_delay=config.TYPING_SPEED_MAX,
    )
    time.sleep(0.2)
    pyautogui.press("enter")
    print("   [Keyboard] Pressed Enter.")


def open_new_tab_gui():
    """
    Move mouse pointer to '+' button on the Chrome tab strip and click.
    """
    screen_w, screen_h = human_mouse.get_screen_size()
    plus_x = int(min(screen_w * 0.35, 360) + random.randint(-10, 10))
    plus_y = int(42 + random.randint(-3, 3))

    print(f"   [Mouse] Moving to New Tab '+' area ({plus_x}, {plus_y})...")
    human_mouse.smooth_move_to(plus_x, plus_y, duration=0.4)
    human_mouse.human_click()
    time.sleep(0.2)
    pyautogui.hotkey("ctrl", "t")
    time.sleep(0.8)


def close_tab_gui():
    """
    Move mouse pointer to tab close area and close tab.
    """
    screen_w, screen_h = human_mouse.get_screen_size()
    close_x = int(min(screen_w * 0.22, 240) + random.randint(-5, 5))
    close_y = int(42 + random.randint(-3, 3))

    print(f"   [Mouse] Closing tab at ({close_x}, {close_y})...")
    human_mouse.smooth_move_to(close_x, close_y, duration=0.4)
    pyautogui.hotkey("ctrl", "w")
    time.sleep(0.5)


def run_gui_mouse_cycle():
    """
    Continuous cycle of visiting sites, scrolling, opening & closing tabs.
    """
    launch_chrome_via_mouse_search()

    cycle_num = 0
    total_sites = len(config.WEBSITE_LINKS)

    while True:
        cycle_num += 1
        print("\n" + "=" * 64)
        print(f"   GUI MOUSE CYCLE #{cycle_num} ({total_sites} websites in list)")
        print("   (Move mouse to screen corner (0,0) or press Ctrl+C to stop)")
        print("=" * 64)

        for idx, site in enumerate(config.WEBSITE_LINKS, 1):
            print(f"\n>> [{idx}/{total_sites}] Visiting: {site}")

            # 1. Click address bar and type URL
            click_and_type_url(site)

            # 2. Allow page to load
            load_wait = random.uniform(config.PAGE_VIEW_TIME_MIN, config.PAGE_VIEW_TIME_MAX)
            print(f"   Waiting {load_wait:.1f}s for page render...")
            time.sleep(load_wait)

            # 3. Scroll through webpage with mouse wheel
            print("   [Mouse] Scrolling webpage content...")
            human_mouse.human_scroll(
                passes=config.SCROLL_PASSES,
                amount=config.SCROLL_AMOUNT,
                pause_range=(config.SCROLL_PAUSE_MIN, config.SCROLL_PAUSE_MAX),
            )

            # 4. Open new tab using mouse
            print("   [Mouse] Opening new tab...")
            open_new_tab_gui()
            time.sleep(1.0)

            # 5. Manage tabs: close extra tab every few sites to prevent clutter
            if idx % config.MAX_OPEN_TABS == 0:
                print("   [Tabs] Managing tabs: closing background tab...")
                close_tab_gui()

            time.sleep(random.uniform(2.0, 4.0))

        # End of cycle pause
        cycle_pause = random.uniform(config.CYCLE_PAUSE_MIN, config.CYCLE_PAUSE_MAX)
        print(f"\n[Cycle #{cycle_num} Complete] Pausing for {cycle_pause:.1f}s before next round...\n")
        time.sleep(cycle_pause)


def main():
    print("=" * 64)
    print("   CHROME GUI MOUSE BOT - DESKTOP INTERACTION")
    print("=" * 64)
    try:
        run_gui_mouse_cycle()
    except KeyboardInterrupt:
        print("\n[Stopped] Bot stopped by user.")
    except pyautogui.FailSafeException:
        print("\n[Fail-Safe] Mouse moved to screen corner (0,0). Bot halted immediately.")
    except Exception as e:
        print(f"\n[Error] {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
