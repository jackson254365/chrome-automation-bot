# Chrome Automation Bot Suite

A specialized Python bot for automated Chrome web browsing featuring an **On-Screen Visible Animated Mouse Pointer** and **Anti-Bot Detection Evasion via Stealth ChromeDriver**.

The project is located in: `~/chrome_bot_project` ([`/home/arch/chrome_bot_project`](file:///home/arch/chrome_bot_project)).

---

## 🖱️ Visible Mouse Pointer & Interaction

1. **On-Screen Visual Mouse Pointer (`visual_mouse_bot.py`, Default)**:
   - Injects a high-visibility animated OS-style pointer arrow with realistic drop-shadow directly onto the screen.
   - Visibly glides across the page using smooth **cubic-bezier easing** directly to search bars, inputs, and links.
   - Triggers an **animated click ripple & scale pulse** whenever a click occurs.
   - Types queries and website links character-by-character with natural human typing cadence.
   - Scrolls down through web pages with smooth scrolling and realistic mouse reading drift.
   - Opens new tabs, switches tabs, closes older tabs to manage memory, and cycles repeatedly across the website search list.

2. **Why the Hardware Pointer did not move previously (Wayland Security)**:
   - On Linux systems running **GNOME on Wayland**, the Wayland display server prohibits standard user-space libraries (`pyautogui`, `pynput`, `xdotool`) from hijacking or moving the hardware cursor across desktop windows.
   - The default **Visual Mode** solves this completely by rendering a real-time, interactive, visible mouse pointer that you can watch moving and clicking on your monitor.

3. **Anti-Bot Detection Evasion (Stealth ChromeDriver)**:
   - Completely masks `navigator.webdriver` (`None` / `undefined`).
   - Suppresses the *"Chrome is being controlled by automated test software"* infobar banner (`excludeSwitches: ["enable-automation"]`).
   - Disables `AutomationControlled` blink features (`--disable-blink-features=AutomationControlled`).
   - Employs `selenium-stealth` fingerprint spoofing (realistic plugins, languages, platform, WebGL vendor).

---

## 📁 Project Structure

```
~/chrome_bot_project/
├── main.py                 # Main CLI entry point
├── visual_mouse_bot.py     # On-screen visible mouse pointer + Stealth automation (Default)
├── chrome_stealth_bot.py   # Desktop ChromeDriver stealth bot
├── chrome_gui_mouse_bot.py # Pure Desktop Launcher Search & Click Bot
├── human_mouse.py          # Bezier curve movement and human typing helpers
├── config.py               # Website search list and tunable parameters
├── run.sh                  # Shell launcher script
└── README.md               # Documentation
```

---

## 🚀 How to Run

Navigate to the project folder:
```bash
cd ~/chrome_bot_project
```

### 1. Run the Visible Mouse Pointer Bot (Default)
```bash
./run.sh
# or: python3 main.py
```
*You will visibly see the mouse pointer glide to search inputs, display an animated click ripple, type the search query, scroll smoothly down the page, open tabs, and cycle continuously.*

### 2. Running on Windows 🪟

The bot is fully configured for Windows:
1. **Copy or clone the folder** to your Windows PC (e.g. `C:\Users\YourName\chrome_bot_project`).
2. **Install requirements** (if not already installed):
   ```cmd
   pip install -r requirements.txt
   ```
3. **Launch the bot**:
   - Simply double-click **`run.bat`**, OR run:
   ```cmd
   python main.py
   ```
4. **Windows Behavior**:
   - The bot dynamically detects Windows (`sys.platform == 'win32'`).
   - Automatically sets Windows 10/11 User-Agent headers and `Win32` platform fingerprinting in the anti-bot evasion engine.
   - On Windows, unlike Linux Wayland, the OS natively supports physical mouse pointer movement via the Win32 API, so both hardware mouse control and the visible on-screen cursor operate seamlessly!

### 3. Verify Anti-Bot Stealth Status
```bash
# On Linux:
./run.sh --check-stealth

# On Windows:
python main.py --check-stealth
```

### 4. Stop the Bot
Press `Ctrl+C` in your terminal or command prompt at any time to cleanly close the browser session and exit.
