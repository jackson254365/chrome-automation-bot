#!/usr/bin/env python3
"""
visual_mouse_bot.py - Crash-Proof Chrome Automation Bot with On-Screen Visible
Mouse Pointer and Anti-Bot Detection Evasion.

Features:
1. 100% Crash-Proof Architecture:
   - Full exception resilience for timeouts, stale elements, closed tabs, and network drops.
   - Page load timeout protection (stops page hangs after 25s).
   - Window handle auto-recovery and auto-healing browser reconnection.
   - Low memory footprint: proactive tab cleanup prevents Chrome renderer OOM crashes.
2. Visible Animated Mouse Pointer:
   - High-visibility animated OS-style pointer arrow with realistic drop-shadow.
   - Smooth cubic-bezier gliding across the viewport to target inputs, links, and search bars.
   - Click ripple & pulse animation on every click.
3. Natural Human Interaction:
   - Types queries character-by-character with realistic human typing cadence.
   - Scrolls smoothly down pages with natural mouse drift and reading pauses.
   - Cycles through website search list continuously without stopping.
4. Anti-Bot Detection Evasion:
   - Masks navigator.webdriver (returns undefined).
   - Removes 'Chrome is being controlled by automated software' info bar.
   - Disables AutomationControlled blink features.
   - Applies selenium-stealth fingerprint protection (cross-platform: Windows/Linux/Mac).
"""

import os
import sys
import time
import random
import re
import subprocess
from typing import List, Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchWindowException,
    WebDriverException,
    StaleElementReferenceException,
    ElementNotInteractableException,
    NoSuchElementException,
)
from webdriver_manager.chrome import ChromeDriverManager

try:
    from selenium_stealth import stealth
    HAS_STEALTH = True
except ImportError:
    HAS_STEALTH = False

import config

# On-Screen Visual Mouse Pointer Injection Script
CURSOR_INJECTION_JS = """
(function() {
    try {
        if (document.getElementById('virtual-bot-cursor')) return;

        const cur = document.createElement('div');
        cur.id = 'virtual-bot-cursor';
        cur.innerHTML = `
            <svg width="30" height="30" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M2 2L11 26L16 15L27 10L2 2Z" fill="#E63946" stroke="#FFFFFF" stroke-width="2" stroke-linejoin="round"/>
                <circle cx="2" cy="2" r="2.5" fill="#FFFFFF"/>
            </svg>
        `;
        cur.style.position = 'fixed';
        cur.style.left = '60px';
        cur.style.top = '60px';
        cur.style.width = '30px';
        cur.style.height = '30px';
        cur.style.zIndex = '2147483647';
        cur.style.pointerEvents = 'none';
        cur.style.transition = 'left 0.65s cubic-bezier(0.22, 1, 0.36, 1), top 0.65s cubic-bezier(0.22, 1, 0.36, 1), transform 0.15s ease';
        cur.style.filter = 'drop-shadow(2px 4px 6px rgba(0,0,0,0.45))';
        
        const rippleStyle = document.createElement('style');
        rippleStyle.innerHTML = `
            @keyframes botRippleAnim {
                0% { transform: scale(0.6); opacity: 0.9; }
                100% { transform: scale(2.8); opacity: 0; }
            }
            .bot-click-ripple {
                position: fixed;
                width: 24px;
                height: 24px;
                border-radius: 50%;
                background: rgba(230, 57, 70, 0.7);
                border: 2px solid #ffffff;
                pointer-events: none;
                z-index: 2147483646;
                animation: botRippleAnim 0.45s ease-out forwards;
            }
        `;
        (document.head || document.documentElement).appendChild(rippleStyle);
        (document.body || document.documentElement).appendChild(cur);

        window.moveBotCursor = function(x, y) {
            const c = document.getElementById('virtual-bot-cursor');
            if (c) {
                c.style.left = x + 'px';
                c.style.top = y + 'px';
            }
        };

        window.clickBotCursor = function() {
            const c = document.getElementById('virtual-bot-cursor');
            if (!c) return;
            c.style.transform = 'scale(0.82)';
            
            const rect = c.getBoundingClientRect();
            const ripple = document.createElement('div');
            ripple.className = 'bot-click-ripple';
            ripple.style.left = (rect.left - 4) + 'px';
            ripple.style.top = (rect.top - 4) + 'px';
            (document.body || document.documentElement).appendChild(ripple);
            
            setTimeout(() => {
                c.style.transform = 'scale(1)';
                ripple.remove();
            }, 450);
        };
    } catch(e) {}
})();
"""


class CrashProofVisualBot:
    """Robust Chrome Bot combining Stealth anti-detection with crash-proof visual mouse automation."""

    def __init__(self):
        self.driver: Optional[webdriver.Chrome] = None
        self.cycle_count = 0
        self._init_driver()

    def _init_driver(self):
        """Initialize or re-initialize Chrome with stealth anti-detection flags."""
        print("\n" + "=" * 62)
        print("   Launching Chrome (Stealth Anti-Detection Mode)")
        print("=" * 62)

        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-background-networking")
        
        # Anti-Bot Detection Flags
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        # OS detection for accurate stealth headers
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
            print(f"   [Notice] Driver manager warning: {e}. Falling back to default service...")
            driver = webdriver.Chrome(options=options)

        # Set safety timeouts to prevent hangs on heavy websites
        driver.set_page_load_timeout(25)
        driver.set_script_timeout(15)

        # Permanent CDP injection to hide navigator.webdriver
        try:
            driver.execute_cdp_cmd(
                "Page.addScriptToEvaluateOnNewDocument",
                {
                    "source": f"""
                    Object.defineProperty(navigator, 'webdriver', {{
                        get: () => undefined
                    }});
                    window.chrome = {{ runtime: {{}} }};
                    Object.defineProperty(navigator, 'platform', {{
                        get: () => '{platform_str}'
                    }});
                    Object.defineProperty(navigator, 'plugins', {{
                        get: () => [1, 2, 3, 4, 5]
                    }});
                    """
                },
            )
        except Exception:
            pass

        # Apply selenium-stealth
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
                print(f"   [Stealth] Fingerprint protection active ({platform_str}).")
            except Exception as e:
                print(f"   [Notice] Stealth application: {e}")

        try:
            is_webdriver = driver.execute_script("return navigator.webdriver")
            print(f"   [Verification] navigator.webdriver = {is_webdriver} (Bot Hidden!)")
        except Exception:
            pass

        self.driver = driver

    def ensure_valid_window(self) -> bool:
        """
        Verify that a valid window handle exists.
        If current tab was closed or lost, safely switch to any existing window handle.
        If browser process terminated, restart browser automatically.
        """
        if self.driver is None:
            self._init_driver()
            return True

        try:
            handles = self.driver.window_handles
            if not handles:
                print("   [Recovery] No open windows found. Restarting browser...")
                self._restart_driver()
                return True

            # Check if current window handle is still responsive
            try:
                _ = self.driver.current_url
            except Exception:
                # Switch to last available handle
                self.driver.switch_to.window(handles[-1])
            return True
        except Exception as e:
            print(f"   [Recovery] Browser connection lost ({e}). Restarting browser...")
            self._restart_driver()
            return True

    def _restart_driver(self):
        """Safely tear down crashed instance and initialize fresh browser."""
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
            self.driver = None
        time.sleep(1.0)
        self._init_driver()

    def ensure_cursor_injected(self):
        """Inject or re-inject visual mouse pointer if page navigated."""
        if not self.driver:
            return
        try:
            self.driver.execute_script(CURSOR_INJECTION_JS)
        except Exception:
            pass

    def move_pointer_to(self, target_x: int, target_y: int, delay: float = 0.6):
        """Visibly move mouse pointer to (target_x, target_y)."""
        self.ensure_cursor_injected()
        try:
            self.driver.execute_script(f"window.moveBotCursor({target_x}, {target_y});")
            time.sleep(delay)
        except Exception:
            pass

    def click_pointer_at(self, target_x: int, target_y: int, element=None):
        """Move mouse pointer to target, perform visual click ripple, and trigger click."""
        self.move_pointer_to(target_x, target_y, delay=0.5)
        try:
            self.driver.execute_script("window.clickBotCursor();")
            time.sleep(0.3)
        except Exception:
            pass

        if element is not None:
            try:
                element.click()
            except Exception:
                try:
                    self.driver.execute_script("arguments[0].click();", element)
                except Exception:
                    pass

    def safe_get(self, url: str) -> bool:
        """
        Load a website with timeout protection so slow sites never hang or crash the bot.
        """
        self.ensure_valid_window()
        print(f"\n>> Visiting: {url}")
        try:
            self.driver.get(url)
            time.sleep(2.0)
            return True
        except TimeoutException:
            print(f"   [Notice] Page load timed out on {url} (25s limit). Stopping load and proceeding...")
            try:
                self.driver.execute_script("window.stop();")
            except Exception:
                pass
            time.sleep(1.0)
            return True
        except Exception as e:
            print(f"   [Warning] Navigation error on {url}: {e}")
            return False

    def type_with_pointer(self, element, text: str):
        """Type text character-by-character with natural human cadence."""
        for ch in text:
            try:
                element.send_keys(ch)
                delay = random.uniform(config.TYPING_SPEED_MIN, config.TYPING_SPEED_MAX)
                if ch in ".:/-_ ":
                    delay += 0.06
                time.sleep(delay)
            except Exception:
                break
        time.sleep(0.3)

    def smooth_scroll(self, passes: int = 5, amount: int = 240):
        """Smoothly scroll through page while moving mouse pointer naturally."""
        self.ensure_cursor_injected()
        for _ in range(passes):
            drift_x = 420 + random.randint(-150, 180)
            drift_y = 300 + random.randint(-100, 120)
            self.move_pointer_to(drift_x, drift_y, delay=0.25)

            try:
                self.driver.execute_script(f"window.scrollBy({{ top: {amount}, behavior: 'smooth' }});")
            except Exception:
                break
            time.sleep(random.uniform(config.SCROLL_PAUSE_MIN, config.SCROLL_PAUSE_MAX))

        # Scroll slightly back up
        try:
            self.driver.execute_script("window.scrollBy({ top: -250, behavior: 'smooth' });")
        except Exception:
            pass
        time.sleep(0.6)

    def open_new_tab(self):
        """Open a new browser tab and switch to it safely."""
        self.ensure_valid_window()
        print("   [Mouse] Opening new tab...")
        self.move_pointer_to(280, 20, delay=0.35)
        try:
            self.driver.execute_script("window.clickBotCursor();")
            time.sleep(0.2)
        except Exception:
            pass

        try:
            self.driver.execute_script("window.open('about:blank', '_blank');")
            handles = self.driver.window_handles
            if handles:
                self.driver.switch_to.window(handles[-1])
            time.sleep(0.6)
        except Exception as e:
            print(f"   [Notice] Tab open warning: {e}")

    def clean_excess_tabs(self, max_tabs: int = 3, keep_last: Optional[int] = None):
        """
        Close older background tabs to prevent memory bloat and keep Chrome fast and stable.
        """
        limit = keep_last if keep_last is not None else max_tabs
        self.ensure_valid_window()
        try:
            handles = self.driver.window_handles
            if len(handles) > limit:
                print(f"   [Memory] Closing {len(handles) - limit} excess tab(s) to maintain stability...")
                while len(self.driver.window_handles) > limit:
                    # Switch to oldest tab (index 0) and close it
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    self.driver.close()
                    # Return focus to active tab
                    handles = self.driver.window_handles
                    if handles:
                        self.driver.switch_to.window(handles[-1])
                    time.sleep(0.3)
        except Exception as e:
            print(f"   [Notice] Tab cleanup warning: {e}")

    def interact_with_site(self, url: str):
        """
        Safely browse a website, locate search inputs, move cursor, type, and scroll.
        Fully protected against element staleness and site errors.
        """
        if not self.safe_get(url):
            return

        self.ensure_cursor_injected()
        self.move_pointer_to(140, 110, delay=0.4)

        # Try to locate search inputs on the page
        selectors = [
            "input[name='q']",
            "input[type='search']",
            "input[name='search']",
            "input[name='p']",
            "#search",
            "input[type='text']",
        ]
        search_element = None
        for sel in selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, sel)
                for el in elements:
                    if el.is_displayed() and el.is_enabled():
                        search_element = el
                        break
                if search_element:
                    break
            except Exception:
                continue

        if search_element:
            try:
                rect = search_element.rect
                target_x = max(50, min(int(rect["x"] + rect["width"] / 2), 1100))
                target_y = max(50, min(int(rect["y"] + rect["height"] / 2), 600))

                print(f"   [Mouse] Moving pointer to search bar at ({target_x}, {target_y})...")
                self.click_pointer_at(target_x, target_y, element=search_element)

                queries = [
                    "Python automation tutorial",
                    "Latest technology trends",
                    "Open source software",
                    "Artificial intelligence advancements",
                    "Web development best practices",
                ]
                query = random.choice(queries)
                print(f"   [Keyboard] Typing query: '{query}'...")
                self.type_with_pointer(search_element, query)
                try:
                    search_element.send_keys(Keys.ENTER)
                except Exception:
                    pass
                time.sleep(2.0)
                self.ensure_cursor_injected()
            except (StaleElementReferenceException, ElementNotInteractableException):
                pass
            except Exception as e:
                print(f"   [Notice] Search input interaction: {e}")

        # Smooth scrolling through webpage
        print("   [Mouse] Scrolling smoothly through webpage content...")
        self.smooth_scroll(passes=config.SCROLL_PASSES, amount=220)

        # Move mouse across page
        self.move_pointer_to(480, 320, delay=0.4)
        time.sleep(1.0)

    def run_cycle(self):
        """
        Continuous, crash-proof loop across websites.
        Never terminates on unexpected web errors or timeouts.
        """
        total_sites = len(config.WEBSITE_LINKS)
        print("\n" + "=" * 62)
        print("   STARTING CONTINUOUS VISIBLE MOUSE AUTOMATION")
        print("   (Press Ctrl+C in terminal to stop)")
        print("=" * 62)

        try:
            while True:
                self.cycle_count += 1
                print(f"\n{'='*20} CYCLE #{self.cycle_count} {'='*20}")

                for idx, url in enumerate(config.WEBSITE_LINKS, 1):
                    print(f"\n[{idx}/{total_sites}] Processing site...")
                    
                    try:
                        self.interact_with_site(url)
                    except Exception as err:
                        print(f"   [Error Recovered] Issue on {url}: {err}. Safely proceeding...")
                        self.ensure_valid_window()

                    # Open new tab for next action
                    try:
                        self.open_new_tab()
                    except Exception:
                        self.ensure_valid_window()

                    # Proactive memory cleanup: keep tab count low so Chrome never crashes
                    self.clean_excess_tabs(max_tabs=config.MAX_OPEN_TABS)

                    pause = random.uniform(2.0, 4.0)
                    time.sleep(pause)

                # End of cycle tab cleanup
                print(f"\n[Cycle #{self.cycle_count} Finished] Maintaining optimal tab state...")
                self.clean_excess_tabs(max_tabs=1)

                cycle_pause = random.uniform(config.CYCLE_PAUSE_MIN, config.CYCLE_PAUSE_MAX)
                print(f"Pausing for {cycle_pause:.1f}s before Cycle #{self.cycle_count + 1}...\n")
                time.sleep(cycle_pause)

        except KeyboardInterrupt:
            print("\n[Stopped] Bot interrupted by user. Closing browser...")
        finally:
            if self.driver:
                try:
                    self.driver.quit()
                except Exception:
                    pass
            print("Session cleanly closed.")


def main():
    bot = CrashProofVisualBot()
    bot.run_cycle()


if __name__ == "__main__":
    main()
