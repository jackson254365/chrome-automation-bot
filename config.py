#!/usr/bin/env python3
"""
config.py - Configuration settings and target website search list.
"""

from typing import List

# Comprehensive list of websites to visit and scroll through
WEBSITE_LINKS: List[str] = [
    "https://www.google.com",
    "https://www.wikipedia.org",
    "https://www.python.org",
    "https://github.com",
    "https://news.ycombinator.com",
    "https://duckduckgo.com",
    "https://www.stackoverflow.com",
    "https://www.bbc.com",
    "https://techcrunch.com",
    "https://archive.org",
]

# Scrolling behavior configuration
SCROLL_PASSES = 5               # Number of scroll actions per page
SCROLL_AMOUNT = -200            # Scroll distance per step (negative = down)
SCROLL_PAUSE_MIN = 0.8          # Min pause between scroll steps (seconds)
SCROLL_PAUSE_MAX = 2.0          # Max pause between scroll steps (seconds)

# Reading / viewing pause on page before moving on
PAGE_VIEW_TIME_MIN = 3.0        # Seconds
PAGE_VIEW_TIME_MAX = 6.0        # Seconds

# Keystroke typing speed (seconds per char)
TYPING_SPEED_MIN = 0.04
TYPING_SPEED_MAX = 0.12

# Max open tabs in browser before closing older tabs
MAX_OPEN_TABS = 4

# Inter-cycle pause
CYCLE_PAUSE_MIN = 4.0           # Seconds
CYCLE_PAUSE_MAX = 8.0           # Seconds
