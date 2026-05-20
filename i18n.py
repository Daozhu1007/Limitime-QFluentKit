"""
Minimal i18n stub — drop-in replacement for KSC's I18nManager.
Returns English text directly; swap in JSON-based I18nManager when
you need multi-language support.
"""


class I18nManager:
    """Minimal i18n that returns keys as-is (English mode)."""
    locale = "en_US"

    def tr(self, key, *args):
        text = str(key)
        if args:
            try:
                text = text.format(*args)
            except Exception:
                pass
        return text

    def set_language(self, locale_code):
        self.locale = locale_code


i18n = I18nManager()
