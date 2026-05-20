from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from qfluentwidgets import (SubtitleLabel, BodyLabel, CardWidget, ComboBox,
                            SwitchButton, Theme, setTheme, qconfig, InfoBar)

from i18n import i18n, save_config, _load_config

LANG_OPTIONS = {
    "zh_CN": "简体中文",
    "en_US": "English",
}


class SettingsInterface(QWidget):
    """Settings page — extend with your own options."""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("SettingsInterface")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 32, 24, 24)
        self.layout.setSpacing(20)

        title = SubtitleLabel(i18n.tr("settings_title"))
        title.setStyleSheet("font-size: 26px; font-weight: bold;")
        self.layout.addWidget(title)

        # --- Theme toggle ---
        theme_card = CardWidget()
        theme_layout = QHBoxLayout(theme_card)
        theme_layout.setContentsMargins(20, 16, 20, 16)
        theme_layout.setSpacing(15)

        theme_text_layout = QVBoxLayout()
        theme_text_layout.setSpacing(4)
        theme_title = BodyLabel(i18n.tr("settings_dark_theme"))
        theme_title.setStyleSheet("font-size: 14px;")
        theme_desc = BodyLabel(i18n.tr("settings_dark_theme_desc"))
        theme_desc.setStyleSheet("color: #a0a0a0; font-size: 12px;")
        theme_text_layout.addWidget(theme_title)
        theme_text_layout.addWidget(theme_desc)

        self.theme_switch = SwitchButton()
        self.theme_switch.setChecked(True)  # dark by default
        self.theme_switch.checkedChanged.connect(self._on_theme_changed)

        theme_layout.addLayout(theme_text_layout, 1)
        theme_layout.addWidget(self.theme_switch)
        self.layout.addWidget(theme_card)

        # --- Language ---
        lang_card = CardWidget()
        lang_layout = QHBoxLayout(lang_card)
        lang_layout.setContentsMargins(20, 16, 20, 16)
        lang_layout.setSpacing(15)

        lang_text_layout = QVBoxLayout()
        lang_text_layout.setSpacing(4)
        lang_title = BodyLabel(i18n.tr("settings_language"))
        lang_title.setStyleSheet("font-size: 14px;")
        lang_desc = BodyLabel(i18n.tr("settings_language_desc"))
        lang_desc.setStyleSheet("color: #a0a0a0; font-size: 12px;")
        lang_text_layout.addWidget(lang_title)
        lang_text_layout.addWidget(lang_desc)

        self.lang_combo = ComboBox()
        for code, label in LANG_OPTIONS.items():
            self.lang_combo.addItem(label, userData=code)
        current_idx = list(LANG_OPTIONS.keys()).index(i18n.locale)
        self.lang_combo.setCurrentIndex(current_idx)
        self.lang_combo.currentIndexChanged.connect(self._on_lang_changed)

        lang_layout.addLayout(lang_text_layout, 1)
        lang_layout.addWidget(self.lang_combo)
        self.layout.addWidget(lang_card)

        self.layout.addStretch(1)

    def _on_theme_changed(self, checked):
        if checked:
            setTheme(Theme.DARK)
            qconfig.set(qconfig.themeMode, Theme.DARK)
        else:
            setTheme(Theme.LIGHT)
            qconfig.set(qconfig.themeMode, Theme.LIGHT)

    def _on_lang_changed(self, index):
        lang_code = self.lang_combo.itemData(index)
        if lang_code == i18n.locale:
            return
        i18n.set_language(lang_code)
        # Persist to config.json
        config = _load_config()
        config.setdefault("Settings", {})["Language"] = lang_code
        save_config(config)
        InfoBar.success(
            i18n.tr("settings_language_changed"),
            i18n.tr("settings_language_restart"),
            duration=5000,
            parent=self
        )
