# Limitime-QFluentKit — AI Agent Instructions

A production-hardened PyQt6 + qfluentwidgets desktop app template.
This is NOT raw qfluentwidgets — it contains critical layout fixes
discovered through source-code analysis and real-world testing.

**Creator:** Limitime
**Base:** PyQt6 + QFluentWidgets (zhiyiYo/PyQt-Fluent-Widgets)
**Python:** 3.10+


## Project Structure

```
YourApp/
├── main.py              # Entry point, QApplication, High-DPI config
├── ui_main.py           # MainWindow (FluentWindow) + BrandingWidget + layout fixes
├── ui_home.py           # Home page (replace with your content)
├── ui_settings.py       # Settings page template
├── i18n.py              # Minimal i18n stub (swap for multi-language)
├── assets/
│   ├── logo.png         # Sidebar branding logo (22px height recommended)
│   └── logo.ico         # Window icon
└── CLAUDE.md            # This file
```


## Architecture

```
main.py
  └── QApplication
        └── MainWindow (FluentWindow)
              ├── NavigationInterface (left sidebar)
              │     ├── BrandingWidget (logo + title, TOP position)
              │     ├── Home tab (FIF.HOME)
              │     └── Settings tab (FIF.SETTING, BOTTOM position)
              └── StackedWidget (right content area)
                    ├── HomeInterface (QWidget)
                    └── SettingsInterface (QWidget)
```


## How To Add A New Page

### Step 1: Create the interface file

```python
# ui_myfeature.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import SubtitleLabel, CardWidget

class MyFeatureInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("MyFeatureInterface")  # REQUIRED for qfluentwidgets routing
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 32, 24, 24)
        self.layout.setSpacing(16)

        title = SubtitleLabel("My Feature")
        title.setStyleSheet("font-size: 26px; font-weight: bold;")
        self.layout.addWidget(title)
        self.layout.addStretch(1)
```

### Step 2: Register in ui_main.py

```python
from ui_myfeature import MyFeatureInterface

# In MainWindow.__init__:
self.myfeature_interface = MyFeatureInterface(self)
self.addSubInterface(
    self.myfeature_interface,
    FIF.DEVELOPER_TOOLS,         # icon (FluentIcon)
    "My Feature",                # label text
    position=NavigationItemPosition.SCROLL   # TOP, SCROLL, or BOTTOM
)
```

### Navigation item positions:
- `NavigationItemPosition.TOP` — above the scroll area (fixed)
- `NavigationItemPosition.SCROLL` — inside the scrollable area
- `NavigationItemPosition.BOTTOM` — below the scroll area (fixed, good for Settings/About)


## Critical Layout Constraints (DO NOT TOUCH)

These exist to prevent the left sidebar from collapsing when the window is resized.
They were discovered by reading the qfluentwidgets source code.

### 1. `setMinimumExpandWidth(800)` — THE KEY FIX

```python
self.navigationInterface.panel.setMinimumExpandWidth(800)
```

**Why:** NavigationPanel.eventFilter() listens to window Resize events.
If window width < `minimumExpandWidth` (default: 1008), it calls `collapse()`
automatically — switching the sidebar to 48px compact mode and hiding your
BrandingWidget. This check is INDEPENDENT of the threshold in `expand()`.

Setting it to 800 puts it safely below our `setMinimumSize(900, 650)`,
so the sidebar NEVER auto-collapses.

### 2. `setMinimumSize(900, 650)`

Prevents the window from going below a usable size. With sidebar=207px,
the content area gets at least 693px.

### 3. BrandingWidget size policies

- `icon_label` → `QSizePolicy.Fixed, QSizePolicy.Fixed` — logo never scales
- `title_label` → `QSizePolicy.Minimum, QSizePolicy.Preferred` — text width
  matches its natural content width, can't be squeezed narrower
- `setWordWrap(False)` — no multi-line fallback

### 4. Menu button removed

```python
nav_panel.vBoxLayout.removeWidget(nav_panel.menuButton)
nav_panel.menuButton.hide()
nav_panel.menuButton.setParent(None)
```

Prevents users from manually collapsing the sidebar.

### 5. Title bar icon/label hidden

```python
self.titleBar.titleLabel.hide()
self.titleBar.iconLabel.hide()
```

The BrandingWidget already shows logo + title. Avoids duplication.


## i18n Usage

```python
from i18n import i18n

label = i18n.tr("my_key")            # Returns key if no translation
label = i18n.tr("Hello, {0}", name)  # Format with args
```

The stub returns keys as-is (English). To add multi-language:
1. Replace `i18n.py` with KSC-style `I18nManager` that reads JSON files
2. Keep the `tr(key, *args)` signature — it's the same API


## Common Pitfalls

### "My new page doesn't show up"
Check that your interface widget has a unique `setObjectName("...")` call.
qfluentwidgets uses the object name for internal routing.

### "The sidebar collapsed after I changed expandWidth"
Recalculate: `minimumExpandWidth` must be ≤ `setMinimumSize.width`.
With expandWidth=250, your window minimum should be ≥ 250 + 600 = 850.

### "The branding title is clipped"
Adjust `expandWidth` or shorten the title. The title_label Minimum policy
will try to claim its full text width — if sidebar is too narrow, layout
will fight. Keep `expandWidth ≥ title_natural_width + icon_width + margins`.

### "I want to enable sidebar collapse"
If you WANT users to collapse the sidebar:
1. Remove the `setMinimumExpandWidth(800)` line
2. Remove the menuButton removal code
3. Ensure your interface widgets handle compacted mode gracefully


## Available Imports

```python
# Qt
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QUrl, QTimer
from PyQt6.QtGui import QPixmap, QIcon, QDesktopServices
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QSizePolicy, QFrame)

# qfluentwidgets (most-used)
from qfluentwidgets import (
    FluentWindow, FluentIcon as FIF,
    SubtitleLabel, BodyLabel, LineEdit, TextEdit,
    PushButton, PrimaryPushButton, SwitchButton,
    CardWidget, ComboBox, ScrollArea,
    InfoBar, InfoBarPosition,
    Theme, setTheme, qconfig,
    NavigationItemPosition,
)
```


## Design Patterns (learned from ok-wuthering-waves)

The ok-ww project (which inspired this template) uses a **declarative config
pattern** that eliminates repetitive widget code. When your app grows beyond
a few settings, adopt this approach:

### Declarative Settings (instead of hand-writing Cards)

```python
# BEFORE (verbose — one Card per setting, ~15 lines each):
card = CardWidget()
layout = QHBoxLayout(card)
label = BodyLabel("Keep Browser Open")
switch = SwitchButton()
switch.setChecked(config.get("keep_open", False))
switch.checkedChanged.connect(self._on_keep_open_changed)
layout.addWidget(label)
layout.addWidget(switch)

# AFTER (declarative — define data, framework renders widgets):
class SettingDef:
    """A single setting definition. The framework renders the right widget."""
    def __init__(self, key, label, description="", widget="switch",
                 default=None, options=None):
        self.key = key
        self.label = label
        self.description = description
        self.widget = widget      # "switch", "combo", "text", "number"
        self.default = default
        self.options = options    # for combo boxes

# Then in your interface:
def _build_settings(self):
    for s in self.setting_defs:
        value = self.config.get(s.key, s.default)
        if s.widget == "switch":
            card = self._make_switch_card(s, value)
        elif s.widget == "combo":
            card = self._make_combo_card(s, value)
        self.layout.addWidget(card)

    self.setting_defs = [
        SettingDef("KeepBrowserOpen", "Keep Browser Open",
                   "Browser stays open after login", widget="switch", default=False),
        SettingDef("Language", "Language",
                   "Requires restart", widget="combo", options=["zh_CN", "en_US"]),
    ]
```

The key insight from ok-ww: when every setting is `ConfigOption(name, defaults_dict,
description)`, adding a new setting is a one-line data change — not a 15-line
widget assembly.

### Task/Feature Registration Pattern

```python
# Instead of manually calling addSubInterface for each page,
# declare pages as data and let a loop register them:
PAGES = [
    (HomeInterface, FIF.HOME, "Home", NavigationItemPosition.TOP),
    (MyFeatureInterface, FIF.DEVELOPER_TOOLS, "My Feature", NavigationItemPosition.SCROLL),
    (SettingsInterface, FIF.SETTING, "Settings", NavigationItemPosition.BOTTOM),
]

for cls, icon, label, pos in PAGES:
    instance = cls(self)
    setattr(self, f"{cls.__name__.lower()}_interface", instance)
    self.addSubInterface(instance, icon, label, position=pos)
```

This makes adding a new page a one-line data entry.


## Quick Start For AI Agents

When asked to add a feature, follow this workflow:

1. **Create** `ui_featurename.py` with a `QWidget` subclass
2. **Import** it in `ui_main.py`
3. **Register** it via `self.addSubInterface()` with an icon, label, and position
   - Or use the PAGES list pattern above if the project has adopted it
4. **Test** — run `python main.py`

Do NOT modify the layout constraints in `ui_main.py` unless you understand
the qfluentwidgets NavigationPanel source code.
