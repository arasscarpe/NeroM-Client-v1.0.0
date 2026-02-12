import sys
import time
import random
import threading
import pyautogui
import psutil
from pynput import keyboard
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QFrame, QGridLayout, 
                             QStackedWidget, QLineEdit, QGraphicsDropShadowEffect, QScrollArea)
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QObject
from PyQt5.QtGui import QColor
import os

os.environ['QT_LOGGING_RULES'] = '*.debug=false;qt.qpa.*=false;*.warning=false'
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

SETTINGS = {"toggle_key": "f4", "current_theme": "Dark Red"}
THEME_MAP = {
    "Dark Red": {"glow": "#ff2d5f", "bg": "#12080a", "desc": "Official Nero Blood style."},
    "Purple": {"glow": "#a020f0", "bg": "#0f0812", "desc": "Deep purple abyss look."},
    "Green": {"glow": "#00ff88", "bg": "#08120b", "desc": "Toxic green automation."},
    "Blue": {"glow": "#00aaff", "bg": "#080d12", "desc": "Arctic frost crystal."},
    "Orange": {"glow": "#ff8800", "bg": "#120e08", "desc": "Fireside ember heat."},
    "Slate": {"glow": "#ffffff", "bg": "#1a1a1a", "desc": "Pure minimalistic slate."}
}

MACRO_DATA = {
    "Slow Hit": {"bind": "v", "active": False, "delay": 120, "slots": ["1", "2", "3"]},
    "Auto Crystal": {"bind": "x", "active": False, "delay": 50, "slots": ["2", "3"]},
    "Fast XP": {"bind": "z", "active": False, "delay": 40, "slots": ["9"]},
    "Single Anchor": {"bind": "b", "active": False, "delay": 80, "slots": ["5", "6", "1"]},
    "Double Anchor": {"bind": "n", "active": False, "delay": 60, "slots": ["5", "6", "1"]},
    "Triple Anchor": {"bind": "h", "active": False, "delay": 50, "slots": ["5", "6", "1"]},
    "Quadra Anchor": {"bind": "u", "active": False, "delay": 40, "slots": ["5", "6", "1"]},
    "Auto Offhand": {"bind": "f", "active": False, "delay": 30, "slots": ["1"]},
    "Shield Break": {"bind": "j", "active": False, "delay": 60, "slots": ["8", "1"]},
    "Stun Slam": {"bind": "g", "active": False, "delay": 100, "slots": ["8", "7"]},
    "Elytra Swap": {"bind": "t", "active": False, "delay": 40, "slots": ["2"]}
}

class CommSignal(QObject):
    toggle_visibility = pyqtSignal()
    theme_changed = pyqtSignal()

comm = CommSignal()

def run_macro(name):
    cfg = MACRO_DATA[name]
    if not cfg["active"]: return
    try:
        if name == "Slow Hit":
            pyautogui.press(cfg["slots"][0]); pyautogui.click(button='left')
            time.sleep(random.uniform(0.05, 0.08))
            pyautogui.press(cfg["slots"][1]); pyautogui.click(button='right')
            time.sleep(random.uniform(0.05, 0.08))
            pyautogui.press(cfg["slots"][2]); pyautogui.click(button='right')
        elif name == "Auto Crystal":
            pyautogui.click(button='right'); time.sleep(random.uniform(0.02, 0.04)); pyautogui.click(button='left')
        elif "Anchor" in name:
            loops = {"Single": 1, "Double": 2, "Triple": 3, "Quadra": 4}.get(name.split()[0], 1)
            for _ in range(loops):
                pyautogui.press(cfg["slots"][0]); pyautogui.click(button='right')
                time.sleep(random.uniform(0.02, 0.04))
                pyautogui.press(cfg["slots"][1]); pyautogui.click(button='right')
                time.sleep(random.uniform(0.02, 0.04))
                pyautogui.press(cfg["slots"][2])
        elif name == "Auto Offhand":
            pyautogui.press(cfg["slots"][0])
        else:
            for slot in cfg["slots"]:
                if slot.strip():
                    pyautogui.press(slot.strip())
                    pyautogui.mouseDown(button='right'); time.sleep(random.uniform(0.07, 0.12)); pyautogui.mouseUp(button='right')
                    time.sleep(int(cfg["delay"]) / 1000)
    except: pass

def on_key_press(key):
    try: k = key.char.lower()
    except: k = str(key).replace("Key.", "").lower()
    if k == SETTINGS["toggle_key"].lower(): comm.toggle_visibility.emit(); return
    for name, data in MACRO_DATA.items():
        if data["active"] and data["bind"] == k: threading.Thread(target=run_macro, args=(name,), daemon=True).start()

class MacroCard(QFrame):
    def __init__(self, name, code, desc, fields):
        super().__init__()
        self.name = name
        self.setFixedSize(360, 190)
        self.glow = QGraphicsDropShadowEffect(self); self.glow.setBlurRadius(0); self.glow.setOffset(0, 0); self.setGraphicsEffect(self.glow)
        lay = QVBoxLayout(self); head = QHBoxLayout()
        icon = QLabel(code); icon.setObjectName("IconBox"); icon.setFixedSize(35, 35); icon.setAlignment(Qt.AlignCenter)
        tv = QVBoxLayout(); tv.addWidget(QLabel(name, styleSheet="color:white; font-weight:bold; font-size: 11px;")); tv.addWidget(QLabel(desc, styleSheet="color:#555; font-size: 8px;"))
        self.power = QPushButton("⏻"); self.power.setCheckable(True); self.power.setObjectName("PowerBtn"); self.power.setFixedSize(30, 30); self.power.toggled.connect(self.update_state)
        head.addWidget(icon); head.addLayout(tv); head.addStretch(); head.addWidget(self.power); lay.addLayout(head)
        grid = QGridLayout()
        ki = QLineEdit(MACRO_DATA[self.name]["bind"]); ki.setObjectName("InputBox"); ki.setFixedWidth(45)
        ki.textChanged.connect(lambda t: MACRO_DATA[self.name].update({"bind": t.lower()}))
        grid.addWidget(QLabel("Key", styleSheet="color:#888;"), 0, 0); grid.addWidget(ki, 0, 1)
        di = QLineEdit(str(MACRO_DATA[self.name]["delay"])); di.setObjectName("InputBox"); di.setFixedWidth(45)
        di.textChanged.connect(lambda t: MACRO_DATA[self.name].update({"delay": t if t.isdigit() else 80}))
        grid.addWidget(QLabel("Ms", styleSheet="color:#888;"), 0, 2); grid.addWidget(di, 0, 3)
        for i, f in enumerate(fields):
            r, c = (i // 2) + 1, (i % 2) * 2
            inp = QLineEdit(MACRO_DATA[self.name]["slots"][i]); inp.setObjectName("InputBox"); inp.setFixedWidth(45)
            inp.textChanged.connect(lambda t, idx=i: MACRO_DATA[self.name]["slots"].__setitem__(idx, t))
            grid.addWidget(QLabel(f, styleSheet="color:#888;"), r, c); grid.addWidget(inp, r, c + 1)
        lay.addLayout(grid); comm.theme_changed.connect(self.refresh_theme); self.refresh_theme()
    def update_state(self, s): MACRO_DATA[self.name]["active"] = s; self.refresh_theme()
    def refresh_theme(self):
        theme = THEME_MAP[SETTINGS["current_theme"]]
        self.glow.setColor(QColor(theme["glow"]))
        if MACRO_DATA[self.name]["active"]: self.glow.setBlurRadius(20); self.setStyleSheet(f"background: {theme['bg']}; border-radius: 10px; border: none;")
        else: self.glow.setBlurRadius(0); self.setStyleSheet("background: #0e0e0e; border-radius: 10px; border: none;")

class NeroClient(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint); self.setAttribute(Qt.WA_TranslucentBackground); self.resize(1100, 720)
        self.main_frame = QFrame(self); self.main_frame.setObjectName("MainFrame"); self.main_frame.setGeometry(10, 10, 1080, 700)
        layout = QHBoxLayout(self.main_frame); layout.setContentsMargins(0, 0, 0, 0); layout.setSpacing(0)
        sidebar = QFrame(); sidebar.setObjectName("Sidebar"); sidebar.setFixedWidth(200)
        s_lay = QVBoxLayout(sidebar); self.brand = QLabel("NeroM | v1.0.0"); s_lay.addWidget(self.brand)
        self.stack = QStackedWidget()
        nav = [("Crystal", "⟁"), ("Sword", "⚔"), ("Mace", "🔨"), ("Themes", "🎨"), ("Settings", "⚙")]
        for i, (n, ic) in enumerate(nav):
            btn = QPushButton(f"  {ic}  {n}"); btn.setObjectName("NavBtn"); btn.setCheckable(True); btn.setAutoExclusive(True)
            btn.clicked.connect(lambda _, x=i: self.stack.setCurrentIndex(x))
            s_lay.addWidget(btn); 
            if i == 0: btn.setChecked(True)
        s_lay.addStretch()
        prof = QFrame(); prof.setObjectName("ProfileBox"); pl = QHBoxLayout(prof)
        av = QFrame(); av.setFixedSize(30, 30); av.setStyleSheet("background:#222; border-radius:15px; border:none;")
        info = QVBoxLayout(); u = QLabel("flaxypasha"); u.setStyleSheet("color:white; font-weight:bold; font-size:10px;"); st = QLabel("● Active"); st.setStyleSheet("color:#00ff88; font-size:8px;")
        info.addWidget(u); info.addWidget(st); info.setSpacing(0); pl.addWidget(av); pl.addLayout(info); s_lay.addWidget(prof)
        content = QFrame(); content.setObjectName("Content"); c_lay = QVBoxLayout(content); top = QHBoxLayout(); top.addStretch()
        m_b = QPushButton("—"); m_b.setObjectName("TBtn"); m_b.clicked.connect(self.showMinimized)
        c_b = QPushButton("✕"); c_b.setObjectName("TBtn"); c_b.clicked.connect(self.close)
        top.addWidget(m_b); top.addWidget(c_b); c_lay.addLayout(top); self.init_pages(); c_lay.addWidget(self.stack)
        bot = QHBoxLayout(); bot.addStretch(); self.conn = QLabel("CONNECTED"); self.conn.setStyleSheet("color:#00ff88; font-weight:bold; font-size:10px; margin: 10px 20px;"); bot.addWidget(self.conn); c_lay.addLayout(bot)
        layout.addWidget(sidebar); layout.addWidget(content); comm.theme_changed.connect(self.apply_styles); self.apply_styles()
    def init_pages(self):
        p1 = self.make_page([("Slow Hit", "SH", "Sword+Obsi+Crys", ["Sword", "Obsi", "Crys"]), ("Auto Crystal", "AC", "Right+Left loop", ["Obsi", "Crys"]), ("Fast XP", "XP", "Fast Bottle", ["XP Slot"]), ("Single Anchor", "SA", "1 Cycle", ["Anc", "Glow", "Totem"]), ("Double Anchor", "DA", "2 Cycle", ["Anc", "Glow", "Totem"]), ("Triple Anchor", "TA", "3 Cycle", ["Anc", "Glow", "Totem"]), ("Quadra Anchor", "QA", "4 Cycle", ["Anc", "Glow", "Totem"]), ("Auto Offhand", "AO", "Instant Swap", ["Slot"])])
        p2 = self.make_page([("Shield Break", "SB", "Axe combo", ["Axe", "Sword"])])
        p3 = self.make_page([("Stun Slam", "SS", "Shield bypass", ["Axe", "Mace"]), ("Elytra Swap", "ES", "Instant air", ["Chest"])])
        p4 = self.make_page_theme()
        p5 = QWidget(); p5l = QVBoxLayout(p5); box = QFrame(); box.setObjectName("SettingsBox"); bl = QVBoxLayout(box); bl.addWidget(QLabel("Menu Keybind", styleSheet="color:#eee;"))
        ed = QLineEdit(SETTINGS["toggle_key"].upper()); ed.setObjectName("InputBox"); ed.textChanged.connect(lambda t: SETTINGS.update({"toggle_key": t}))
        bl.addWidget(ed); p5l.addWidget(box); p5l.addStretch()
        for p in [p1, p2, p3, p4, p5]: self.stack.addWidget(p)
    def make_page(self, macros):
        sc = QScrollArea(); sc.setWidgetResizable(True); sc.setStyleSheet("background: transparent; border: none;")
        sc.verticalScrollBar().setStyleSheet("width: 0px; background: transparent;") # Kaydırma çubuğunu gizle
        w = QWidget(); w.setStyleSheet("background: transparent;"); l = QVBoxLayout(w); g = QGridLayout(); g.setSpacing(15); g.setAlignment(Qt.AlignTop)
        for i, m in enumerate(macros): g.addWidget(MacroCard(*m), i // 2, i % 2)
        l.addLayout(g); l.addStretch(); sc.setWidget(w); return sc
    def make_page_theme(self):
        sc = QScrollArea(); sc.setWidgetResizable(True); sc.setStyleSheet("background: transparent; border: none;")
        sc.verticalScrollBar().setStyleSheet("width: 0px; background: transparent;")
        w = QWidget(); l = QVBoxLayout(w); g = QGridLayout(); g.setSpacing(10); g.setAlignment(Qt.AlignTop)
        from __main__ import ThemeCard
        for i, name in enumerate(THEME_MAP.keys()): g.addWidget(ThemeCard(name, THEME_MAP[name]), i // 2, i % 2)
        l.addLayout(g); l.addStretch(); sc.setWidget(w); return sc
    def apply_styles(self):
        g = THEME_MAP[SETTINGS["current_theme"]]["glow"]
        self.brand.setStyleSheet(f"color: {g}; font-weight: bold; font-size: 14px; margin: 15px;")
        self.setStyleSheet(f"#MainFrame{{background:#0b0b0b; border-radius:12px; border:none;}} #Sidebar{{background:#080808; border:none;}} #NavBtn{{background:transparent; color:#555; text-align:left; padding:12px; border:none;}} #NavBtn:checked{{background:#121212; color:white; border-left:3px solid {g};}} #InputBox{{background:#000; color:white; border:none; border-radius:4px; padding:4px;}} #PowerBtn{{background:#1a1a1a; color:#444; border-radius:15px; border:none;}} #PowerBtn:checked{{background:{g}; color:white;}} #IconBox{{background:#1a1a1a; color:{g}; border-radius:8px; font-weight:bold;}} #TBtn{{color:#444; background:transparent; font-size:16px; padding:5px;}} #ProfileBox{{background:#111; border-radius:10px; margin:10px; padding:5px; border:none;}} #SettingsBox{{background:#111; border-radius:10px; padding:15px; border:none;}}")
    def mousePressEvent(self, e): self.oldPos = e.globalPos()
    def mouseMoveEvent(self, e): delta = QPoint(e.globalPos() - self.oldPos); self.move(self.x() + delta.x(), self.y() + delta.y()); self.oldPos = e.globalPos()

class ThemeCard(QFrame):
    def __init__(self, name, config):
        super().__init__(); self.setFixedSize(300, 80); self.setStyleSheet("background:#111; border-radius:10px; border:none;")
        lay = QHBoxLayout(self); pr = QFrame(); pr.setFixedSize(25, 25); pr.setStyleSheet(f"background:{config['glow']}; border-radius:12px; border:none;")
        info = QVBoxLayout(); info.addWidget(QLabel(name, styleSheet="color:white; font-weight:bold; font-size:11px; border:none;")); info.addWidget(QLabel(config['desc'], styleSheet="color:#444; font-size:8px; border:none;"))
        btn = QPushButton("Apply"); btn.setFixedSize(50, 22); btn.setStyleSheet("background:#1a1a1a; color:white; border-radius:4px; border:none;"); btn.clicked.connect(lambda: self.apply_t(name))
        lay.addWidget(pr); lay.addLayout(info); lay.addStretch(); lay.addWidget(btn)
    def apply_t(self, name): SETTINGS["current_theme"] = name; comm.theme_changed.emit()

if __name__ == "__main__":
    app = QApplication(sys.argv); window = NeroClient()
    comm.toggle_visibility.connect(lambda: window.show() if window.isHidden() else window.hide())
    threading.Thread(target=lambda: keyboard.Listener(on_press=on_key_press).start(), daemon=True).start()
    window.show(); sys.exit(app.exec_())