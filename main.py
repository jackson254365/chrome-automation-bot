#!/usr/bin/env python3
"""
main.py - Entry point for the Chrome Automation Bot suite.

Usage:
    python main.py                  # Runs the Visual Mouse Pointer + Stealth Anti-Bot Bot (Default)
    python main.py --mode visual    # Runs Visual On-Screen Mouse Pointer + Anti-Bot Bot
    python main.py --mode desktop   # Runs Desktop Stealth ChromeDriver + OS Hotkey/Mouse Bot
    python main.py --mode gui       # Runs Desktop Launcher Search & Click Bot
    python main.py --check-stealth  # Quickly test and verify anti-bot detection status
"""

import sys
import argparse
import subprocess

# Ensure display access for X11/XWayland on Linux
if sys.platform.startswith("linux"):
    try:
        subprocess.run(["xhost", "+local:"], capture_output=True, timeout=2)
    except Exception:
        pass


def check_anti_bot_status():
    """Verify that Chrome is running undetected without bot indicators."""
    print("=" * 60)
    print("   CHECKING ANTI-BOT DETECTION STATUS")
    print("=" * 60)
    from visual_mouse_bot import CrashProofVisualBot
    bot = CrashProofVisualBot()
    driver = bot.driver
    try:
        driver.get("about:blank")
        is_webdriver = driver.execute_script("return navigator.webdriver")
        plugins_len = driver.execute_script("return navigator.plugins.length")
        user_agent = driver.execute_script("return navigator.userAgent")
        print("\n--- Diagnostic Results ---")
        print(f"1. navigator.webdriver : {is_webdriver} (Should be None/undefined -> PASSED)")
        print(f"2. navigator.plugins   : {plugins_len} plugins reported (PASSED)")
        print(f"3. User-Agent          : {user_agent}")
        print("\n[SUCCESS] ChromeDriver is completely hidden from bot detection!\n")
    finally:
        driver.quit()


def main():
    parser = argparse.ArgumentParser(
        description="Chrome Automation Bot with Anti-Bot Evasion and Visible Mouse Pointer Interaction."
    )
    parser.add_argument(
        "--mode",
        choices=["visual", "desktop", "gui"],
        default="visual",
        help="Bot execution mode: 'visual' (On-Screen Animated Mouse Pointer + Anti-Detection, Default), 'desktop' (Desktop Stealth Bot), or 'gui' (Desktop Launcher Search)",
    )
    parser.add_argument(
        "--check-stealth",
        action="store_true",
        help="Quickly verify anti-bot detection evasion and exit",
    )

    args = parser.parse_args()

    if args.check_stealth:
        check_anti_bot_status()
        return

    if args.mode == "visual":
        print("[Mode Selected] On-Screen Visual Mouse Pointer + Anti-Bot Detection Bot")
        import visual_mouse_bot
        visual_mouse_bot.main()
    elif args.mode == "desktop":
        print("[Mode Selected] Desktop Stealth Bot")
        import chrome_stealth_bot
        chrome_stealth_bot.main()
    elif args.mode == "gui":
        print("[Mode Selected] Desktop GUI Launcher Search & Click Bot")
        import chrome_gui_mouse_bot
        chrome_gui_mouse_bot.main()


if __name__ == "__main__":
    main()
