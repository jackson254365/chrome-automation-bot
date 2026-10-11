#!/usr/bin/env python3
"""
human_mouse.py - Helper module for realistic human-like mouse movements,
natural typing with slight jitter, and smooth scrolling.
"""

import time
import random
import math
import subprocess
import os

# Ensure X11/XWayland display permissions for PyAutoGUI on Linux
if sys.platform.startswith("linux"):
    try:
        subprocess.run(["xhost", "+local:"], capture_output=True, timeout=2)
    except Exception:
        pass

import pyautogui

# Safety fail-safe: move mouse to any screen corner (0,0) to stop immediately
pyautogui.FAIL_SAFE = True
pyautogui.PAUSE = 0.05


def get_screen_size():
    """Return (width, height) of primary screen."""
    return pyautogui.size()


def bezier_curve(p0, p1, p2, p3, t):
    """Cubic Bezier curve calculation for human-like curved path."""
    x = (
        (1 - t) ** 3 * p0[0]
        + 3 * (1 - t) ** 2 * t * p1[0]
        + 3 * (1 - t) * t**2 * p2[0]
        + t**3 * p3[0]
    )
    y = (
        (1 - t) ** 3 * p0[1]
        + 3 * (1 - t) ** 2 * t * p1[1]
        + 3 * (1 - t) * t**2 * p2[1]
        + t**3 * p3[1]
    )
    return int(x), int(y)


def smooth_move_to(target_x, target_y, duration=None, steps=25):
    """
    Move mouse pointer from current position to (target_x, target_y)
    following a natural curved trajectory with human-like acceleration/deceleration.
    """
    start_x, start_y = pyautogui.position()
    
    # If already at target, return
    if abs(start_x - target_x) < 5 and abs(start_y - target_y) < 5:
        return

    if duration is None:
        dist = math.hypot(target_x - start_x, target_y - start_y)
        # Dynamic duration based on distance: 0.3s to 1.2s
        duration = min(max(dist / 1200.0, 0.3), 1.2) + random.uniform(0.05, 0.2)

    # Random control points for natural curvature
    dx = target_x - start_x
    dy = target_y - start_y
    ctrl1 = (
        start_x + dx * random.uniform(0.2, 0.4) + random.uniform(-40, 40),
        start_y + dy * random.uniform(0.1, 0.3) + random.uniform(-40, 40),
    )
    ctrl2 = (
        start_x + dx * random.uniform(0.6, 0.8) + random.uniform(-30, 30),
        start_y + dy * random.uniform(0.7, 0.9) + random.uniform(-30, 30),
    )

    interval = duration / max(steps, 10)
    for i in range(steps + 1):
        t = i / float(steps)
        # Ease in-out parameter
        ease_t = 0.5 * (1 - math.cos(math.pi * t))
        cx, cy = bezier_curve((start_x, start_y), ctrl1, ctrl2, (target_x, target_y), ease_t)
        pyautogui.moveTo(cx, cy)
        time.sleep(interval)


def human_click(target_x=None, target_y=None, clicks=1, button="left"):
    """
    Move to position with natural movement and click with human release delay.
    """
    if target_x is not None and target_y is not None:
        smooth_move_to(target_x, target_y)
        time.sleep(random.uniform(0.08, 0.2))

    for _ in range(clicks):
        pyautogui.mouseDown(button=button)
        time.sleep(random.uniform(0.06, 0.15))
        pyautogui.mouseUp(button=button)
        if clicks > 1:
            time.sleep(random.uniform(0.08, 0.18))


def human_type(text, min_delay=0.04, max_delay=0.12):
    """
    Type text character-by-character with realistic typing cadence.
    """
    for ch in text:
        pyautogui.write(ch)
        delay = random.uniform(min_delay, max_delay)
        # Slight pause after punctuation
        if ch in ".:/?-_":
            delay += random.uniform(0.08, 0.18)
        time.sleep(delay)


def human_scroll(passes=5, amount=-180, pause_range=(0.8, 1.8)):
    """
    Perform natural mouse-wheel scrolling downwards with human reading pauses,
    then scroll slightly back up.
    """
    screen_w, screen_h = get_screen_size()
    # Move mouse into viewport reading area
    smooth_move_to(
        screen_w // 2 + random.randint(-150, 150),
        screen_h // 2 + random.randint(-100, 100),
        duration=0.4
    )

    for i in range(passes):
        # Slight variation in scroll step
        scroll_step = int(amount + random.randint(-30, 30))
        pyautogui.scroll(scroll_step)
        
        # Small mouse drift while reading
        drift_x = random.randint(-20, 20)
        drift_y = random.randint(-15, 15)
        cur_x, cur_y = pyautogui.position()
        pyautogui.moveTo(max(50, cur_x + drift_x), max(100, cur_y + drift_y), duration=0.2)

        pause = random.uniform(*pause_range)
        time.sleep(pause)

    # Scroll slightly back up to mimic realistic browsing
    if passes > 2:
        pyautogui.scroll(int(abs(amount) * 1.5))
        time.sleep(0.5)
