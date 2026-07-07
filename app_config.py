import json
import os
import sys

from qfluentwidgets import (
    ConfigItem,
    OptionsConfigItem,
    OptionsValidator,
    QConfig,
    Theme,
    qconfig,
)


if getattr(sys, "frozen", False):
    app_dir = os.path.dirname(sys.executable)
else:
    app_dir = os.path.dirname(os.path.abspath(__file__))


APP_NAME = "YourApp"
APP_DISPLAY_VERSION = "v1.0"
APP_AUTHOR = "Limitime"
APP_EMAIL = "Daozhu1007@outlook.com"
APP_USER_MODEL_ID = "yourcompany.yourapp.v1"

GITHUB_URL = "https://github.com/yourusername/yourproject"
BILIBILI_URL = "https://space.bilibili.com/477852567"
COMMUNITY_URL = "https://qm.qq.com/your-group-link"
SPONSOR_URL = "https://afdian.com/a/Limitime"

CONFIG_PATH = os.path.join(app_dir, "config.json")

LANG_OPTIONS = {
    "zh_CN": "lang_zh",
    "en_US": "lang_en",
}

THEME_TEXT_KEYS = {
    Theme.LIGHT: "theme_light",
    Theme.DARK: "theme_dark",
    Theme.AUTO: "theme_auto",
}


class AppConfig(QConfig):
    language = OptionsConfigItem(
        "Settings",
        "Language",
        "zh_CN",
        OptionsValidator(list(LANG_OPTIONS.keys())),
        restart=True,
    )
    startup_page = ConfigItem("Settings", "StartupPage", "home")


cfg = AppConfig()
qconfig.load(CONFIG_PATH, cfg)


def _has_saved_theme_mode():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return "ThemeMode" in data.get("QFluentWidgets", {})
    except Exception:
        return False


if not _has_saved_theme_mode():
    qconfig.set(qconfig.themeMode, Theme.DARK, save=False)
