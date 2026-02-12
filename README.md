# NeroM-Client-v1.0.0
NeroM Client For Minecraft

Nero Client | v1.0.0
Nero Client is a high-performance macro automation suite developed in Python and PyQt5. Designed specifically for PvP environments, it features a modern, frameless graphical user interface (GUI) with low-latency execution and categorized combat modules.

Technical Specifications
Language: Python 3.8+

Framework: PyQt5 (GUI)

Input Control: Pynput, PyAutoGUI

System Integration: Psutil

Build Version: 1.0.0

Functional Modules
Crystal Combat Suite
Slow Hit: Synchronized rotation for Sword, Obsidian, and Crystal deployment.

Auto Crystal: High-frequency loop for automated crystal placement and detonation.

Anchor Meta: Pre-configured cycles for Single, Double, Triple, and Quadra Anchor maneuvers.

Auto Offhand: Instantaneous offhand item replenishment via hotkey trigger.

Fast XP: Optimized delay for rapid Experience Bottle usage.

Sword & Mace Utilities
Shield Breaker: Automated Axe-to-Sword transitions for defensive bypass.

Stun Slam: Optimized timing for Mace-based stun attacks.

Elytra Swap: Frame-perfect chestplate-to-elytra switching.

Interface and User Experience
Theming System: Six professionally curated themes (Dark Red, Purple, Green, Blue, Orange, Slate).

Reactive UI: Dynamic glow effects indicate active module status.

Optimized Scrolling: A customized, borderless scroll area with hidden scrollbars for a clean visual footprint.

Status Monitoring: Real-time client connectivity and active user tracking.

Installation
Prerequisites
Ensure Python 3.8 or higher is installed on your system.

Dependency Installation
Install the required libraries using the following command:

Bash
pip install PyQt5 pyautogui pynput psutil
Execution
Run the client from the source directory:

Bash
python main.py
Deployment (Compilation)
To compile the source code into a standalone executable (.exe) for Windows deployment, use PyInstaller:

Bash
pip install pyinstaller
pyinstaller --noconsole --onefile main.py
The resulting executable will be located in the dist directory.

Configuration and Usage
Toggle Interface: The default key to show/hide the GUI is F4.

Administrative Privileges: To ensure consistent input simulation, it is recommended to run the executable with Administrative privileges.

Precision Tuning: Delay values (ms) can be adjusted in real-time within the UI to accommodate varying network conditions and server latency.
