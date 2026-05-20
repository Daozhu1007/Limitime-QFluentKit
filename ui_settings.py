from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from qfluentwidgets import (SubtitleLabel, BodyLabel, CardWidget,
                            SwitchButton, Theme, setTheme, qconfig)

from i18n import i18n


class SettingsInterface(QWidget):
    """Settings page — extend with your own options."""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("SettingsInterface")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 32, 24, 24)
        self.layout.setSpacing(20)

        title = SubtitleLabel(i18n.tr("Settings"))
        title.setStyleSheet("font-size: 26px; font-weight: bold;")
        self.layout.addWidget(title)

        # --- Theme toggle ---
        theme_card = CardWidget()
        theme_layout = QHBoxLayout(theme_card)
        theme_layout.setContentsMargins(20, 16, 20, 16)
        theme_layout.setSpacing(15)

        theme_text_layout = QVBoxLayout()
        theme_text_layout.setSpacing(4)
        theme_title = BodyLabel(i18n.tr("Dark Theme"))
        theme_title.setStyleSheet("font-size: 14px;")
        theme_desc = BodyLabel(i18n.tr("Toggle between dark and light mode"))
        theme_desc.setStyleSheet("color: #a0a0a0; font-size: 12px;")
        theme_text_layout.addWidget(theme_title)
        theme_text_layout.addWidget(theme_desc)

        self.theme_switch = SwitchButton()
        self.theme_switch.setChecked(True)  # dark by default
        self.theme_switch.checkedChanged.connect(self._on_theme_changed)

        theme_layout.addLayout(theme_text_layout, 1)
        theme_layout.addWidget(self.theme_switch)
        self.layout.addWidget(theme_card)

        self.layout.addStretch(1)

    def _on_theme_changed(self, checked):
        if checked:
            setTheme(Theme.DARK)
            qconfig.set(qconfig.themeMode, Theme.DARK)
        else:
            setTheme(Theme.LIGHT)
            qconfig.set(qconfig.themeMode, Theme.LIGHT)
