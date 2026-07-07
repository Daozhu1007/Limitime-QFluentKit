# Limitime-QFluentKit

A production-hardened PyQt6 + QFluentWidgets desktop app template.

This repository is a small application shell, not a framework. It keeps the
parts that tend to be annoying in every new QFluentWidgets project:

- stable expanded navigation
- protected sidebar branding
- JSON i18n with persisted settings
- theme-aware scroll pages
- a reusable Home / Settings / About structure
- high-DPI app icon and image scaling helpers

[简体中文说明](README_zh.md) | English

## Quick Start

```bash
pip install -r requirements.txt
python main.py
```

Requirements: Python 3.10+, PyQt6 >= 6.5, PyQt6-Fluent-Widgets >= 1.5.0.

## Project Structure

```text
yourproject/
|-- main.py              # QApplication entry point
|-- app_config.py        # App constants and QFluentWidgets config items
|-- ui_utils.py          # Resource, icon, theme, and ScrollArea helpers
|-- ui_main.py           # FluentWindow shell and navigation
|-- ui_home.py           # Starter home page
|-- ui_settings.py       # Theme and language settings
|-- ui_about.py          # Generic about page
|-- i18n.py              # JSON i18n loader
|-- locales/
|   |-- zh_CN.json
|   `-- en_US.json
`-- assets/
    |-- github.png
    `-- bilibili.png
```

## What Was Extracted

This template takes the reusable shell practices from mature apps such as
RhythmAlign and leaves product-specific logic behind. The useful pieces are
navigation behavior, theme refresh, ScrollArea background handling, setting
cards, i18n, and asset scaling.

## Customization Checklist

1. Change app constants and URLs in `app_config.py`.
2. Replace icons in `assets/`.
3. Replace the placeholder Home page with your first real page.
4. Add translation keys to both locale files.
5. Register additional pages in `ui_main.py`.

## License

MIT.
