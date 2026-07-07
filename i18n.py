"""JSON-based i18n engine for the desktop app template."""

import json
import os

from app_config import app_dir, cfg


class I18nManager:
    def __init__(self, locale_code="en_US"):
        self.locale = locale_code
        self.texts = {}
        self.load_language()

    def load_language(self):
        lang_file = os.path.join(app_dir, "locales", f"{self.locale}.json")
        try:
            if os.path.exists(lang_file):
                with open(lang_file, "r", encoding="utf-8") as f:
                    self.texts = json.load(f)
            else:
                self.texts = {}
        except Exception as e:
            print(f"[i18n] Failed to load language file: {e}")
            self.texts = {}

    def tr(self, key, *args):
        text = self.texts.get(key, key)
        if args:
            try:
                return text.format(*args)
            except Exception:
                return text
        return text

    def set_language(self, locale_code):
        self.locale = locale_code
        self.load_language()


def _load_config():
    config_path = os.path.join(app_dir, "config.json")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_config(config):
    config_path = os.path.join(app_dir, "config.json")
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"[i18n] Failed to save config: {e}")


raw_config = _load_config()
default_lang = (
    raw_config.get("Settings", {}).get("Language")
    or os.environ.get("I18N_LANG")
    or cfg.language.value
    or "zh_CN"
)
i18n = I18nManager(default_lang)


if __name__ == "__main__":
    print(f"Locale: {i18n.locale}")
    print(i18n.tr("tab_home"))
    print(i18n.tr("about_ver"))
