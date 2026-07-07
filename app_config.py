import os
import sys

from qfluentwidgets import (
    BoolValidator,
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


APP_NAME = "RhythmAlign"
APP_DISPLAY_VERSION = "v1.1.2"
APP_TITLE = f"{APP_NAME} {APP_DISPLAY_VERSION}"
APP_PUBLISHER = "Limitime"
GITHUB_HOME_URL = "https://github.com/Daozhu1007/RhythmAlign"
GITHUB_RELEASES_URL = "https://github.com/Daozhu1007/RhythmAlign/releases"
BILIBILI_URL = "https://space.bilibili.com/477852567"
DONATE_URL = "https://afdian.com/a/Limitime"
QQ_GROUP_ID = "1046879299"
WINDOWS_APP_USER_MODEL_ID = "Limitime.RhythmAlign.QFluentKit"

CONFIG_PATH = os.path.join(app_dir, "config.json")

LANG_OPTIONS = {
    "zh_CN": "lang_zh",
    "en_US": "lang_en",
}

BITRATE_OPTIONS = ["6000k", "10000k", "20000k"]

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
    use_gpu = ConfigItem("Settings", "UseGPU", False, BoolValidator())
    bitrate = OptionsConfigItem(
        "Settings",
        "Bitrate",
        "10000k",
        OptionsValidator(BITRATE_OPTIONS),
    )
    open_folder = ConfigItem("Settings", "OpenFolder", True, BoolValidator())
    stream_copy = ConfigItem("Settings", "StreamCopy", True, BoolValidator())
    check_updates_on_startup = ConfigItem(
        "Settings",
        "CheckUpdatesOnStartup",
        True,
        BoolValidator(),
    )


def _has_saved_theme_mode():
    try:
        import json

        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return "ThemeMode" in data.get("QFluentWidgets", {})
    except Exception:
        return False


cfg = AppConfig()
qconfig.load(CONFIG_PATH, cfg)

if not _has_saved_theme_mode():
    qconfig.set(qconfig.themeMode, Theme.DARK, save=False)
