<div align="center">
  <h1>
    <br/>
    Limitime-QFluentKit
  </h1>

  <p>
    A production-hardened PyQt6 + <a href="https://github.com/zhiyiYo/PyQt-Fluent-Widgets">QFluentWidgets</a> desktop app template.
    <br />
    <i>Critical layout fixes, JSON-based i18n, AI-agent-friendly — clone and build.</i>
  </p>
</div>

<!-- Badges -->
<div align="center">

![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

</div>

[简体中文说明](README_zh.md) | English Readme

---

## What is this?

This is **not** a framework or a library. It's a pre-configured, bug-fixed, ready-to-clone desktop app skeleton built on top of PyQt6 and QFluentWidgets.

When you clone raw QFluentWidgets and start building, you'll hit the same hidden traps every time:
- The left sidebar auto-collapses when you resize the window below 1008px
- The branding logo and title get squeezed out of existence
- There's no i18n system, no About page, no config persistence

This template fixes all of that **before you write a single line of business logic**. It was battle-tested in production apps ([KeanSeatsCatcher](https://github.com/Daozhu1007/KeanSeatsCatcher), [RhythmAlign](https://github.com/Daozhu1007/RhythmAlign)) and then extracted into a reusable form.

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/yourusername/yourproject.git
cd yourproject

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
python main.py
```

**Requirements:** Python 3.10+, PyQt6 >= 6.5, QFluentWidgets >= 1.5.0

---

## Project Structure

```
yourproject/
├── main.py              # QApplication entry point, High-DPI config
├── ui_main.py           # MainWindow + BrandingWidget + layout fixes
├── ui_home.py           # Placeholder home page
├── ui_settings.py       # Settings page (language)
├── ui_about.py          # About page (author, links, warnings)
├── i18n.py              # JSON-based I18nManager + config persistence
├── locales/
│   ├── zh_CN.json       # Chinese translations
│   └── en_US.json       # English translations
├── assets/
│   ├── logo.png         # Sidebar branding logo
│   ├── logo.ico         # Window icon
│   ├── github.png       # GitHub button icon
│   └── bilibili.png     # Bilibili button icon
└── CLAUDE.md            # Comprehensive AI agent instructions
```

---

## Key Features (Pre-Applied Fixes)

### Sidebar Squeeze Protection

QFluentWidgets' `NavigationPanel` has **two independent collapse thresholds**. The `eventFilter(Resize)` handler collapses the sidebar when the window is narrower than 1008px — even if `expand()` logic says otherwise. This template sets `minimumExpandWidth` to 800, putting it safely below the window's minimum size of 900px, so the sidebar **never** auto-collapses.

### BrandingWidget with Locked Size Policies

The logo icon uses `QSizePolicy.Fixed` so it never scales. The title label uses `QSizePolicy.Minimum` so its width equals its natural text width — the layout can't squeeze it narrower. `setWordWrap(False)` prevents multi-line fallback.

### JSON-based i18n with Config Persistence

Drop-in compatible with both KSC and RhythmAlign. Language choice is saved to `config.json` and survives restarts. Adding a new translation key is a two-line change in two JSON files.

### AI-Ready CLAUDE.md

A 580+ line document that teaches any AI coding agent (Claude Code, Codex, Cursor) how to use this template: project structure, architecture diagram, 2-step page creation workflow, all 5 critical layout constraints with source-code rationale, common pitfalls, and a complete import catalog.

---

## Adding a New Page

```python
# 1. Create ui_myfeature.py with a QWidget subclass
class MyFeatureInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("MyFeatureInterface")  # REQUIRED
        ...

# 2. Register in ui_main.py
from ui_myfeature import MyFeatureInterface
self.myfeature_interface = MyFeatureInterface(self)
self.addSubInterface(
    self.myfeature_interface,
    FIF.DEVELOPER_TOOLS, "My Feature",
    position=NavigationItemPosition.SCROLL
)
```

Full instructions in [CLAUDE.md](CLAUDE.md).

---

## Apps Built with This Template

- [KeanSeatsCatcher](https://github.com/Daozhu1007/KeanSeatsCatcher) — Kean University seat availability monitor & auto-catcher
- [RhythmAlign](https://github.com/Daozhu1007/RhythmAlign) — Rhythm game hand-cam audio auto-sync tool

---

## Credits

- **Author:** [Limitime](https://github.com/Daozhu1007)
- **UI Framework:** [zhiyiYo/PyQt-Fluent-Widgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets)
- **Design inspiration:** [ok-oldking/ok-wuthering-waves](https://github.com/ok-oldking/ok-wuthering-waves)

---

## License

MIT — use it for anything, attribution appreciated.
