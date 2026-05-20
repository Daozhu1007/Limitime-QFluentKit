"""
JSON-based i18n engine — drop-in compatible with KSC & RhythmAlign.
Loads locale files from the locales/ directory, falls back to raw keys.
"""

import sys
import os
import json

if getattr(sys, 'frozen', False):
    app_dir = os.path.dirname(sys.executable)
else:
    app_dir = os.path.dirname(os.path.abspath(__file__))


class I18nManager:
    def __init__(self, locale_code="en_US"):
        self.locale = locale_code
        self.texts = {}
        self.load_language()

    def load_language(self):
        lang_file = os.path.join(app_dir, "locales", f"{self.locale}.json")
        try:
            if os.path.exists(lang_file):
                with open(lang_file, 'r', encoding='utf-8') as f:
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
                text = text.format(*args)
            except Exception:
                pass
        return text

    def set_language(self, locale_code):
        self.locale = locale_code
        self.load_language()


# ---- Global translator instance ----
# Default to Chinese; override by setting I18N_LANG env var
# or change this line to "en_US" for English-default projects.
default_lang = os.environ.get("I18N_LANG", "zh_CN")
i18n = I18nManager(default_lang)


if __name__ == '__main__':
    print(f"Locale: {i18n.locale}")
    print(i18n.tr("tab_home"))
    print(i18n.tr("about_ver"))
