from PyQt6.QtWidgets import QVBoxLayout, QWidget
from qfluentwidgets import (
    FluentIcon as FIF,
    InfoBar,
    InfoBarPosition,
    OptionsSettingCard,
    ScrollArea,
    SettingCardGroup,
    SubtitleLabel,
    qconfig,
    setTheme,
)

from app_config import LANG_OPTIONS, THEME_TEXT_KEYS, cfg
from i18n import i18n
from ui_utils import apply_scroll_area_theme, color_style


class SettingsInterface(ScrollArea):
    """Template settings page using native QFluentWidgets setting cards."""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("SettingsInterface")
        self.view = QWidget(self)
        self.layout = QVBoxLayout(self.view)
        self.layout.setContentsMargins(24, 24, 24, 24)
        self.layout.setSpacing(16)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.title = SubtitleLabel(i18n.tr("settings_title"))
        self.layout.addWidget(self.title)

        self.general_group = SettingCardGroup(i18n.tr("settings_general"), self.view)

        self.theme_card = OptionsSettingCard(
            configItem=qconfig.themeMode,
            icon=FIF.PALETTE,
            title=i18n.tr("settings_theme"),
            content=i18n.tr("settings_theme_desc"),
            texts=[i18n.tr(THEME_TEXT_KEYS[theme]) for theme in qconfig.themeMode.options],
            parent=self.general_group,
        )
        self.theme_card.optionChanged.connect(self._on_theme_changed)

        self.lang_card = OptionsSettingCard(
            configItem=cfg.language,
            icon=FIF.LANGUAGE,
            title=i18n.tr("settings_language"),
            content=i18n.tr("settings_language_desc"),
            texts=[i18n.tr(LANG_OPTIONS[code]) for code in LANG_OPTIONS],
            parent=self.general_group,
        )
        self.lang_card.optionChanged.connect(self._on_lang_changed)

        self.general_group.addSettingCard(self.theme_card)
        self.general_group.addSettingCard(self.lang_card)
        self.layout.addWidget(self.general_group)
        self.layout.addStretch(1)
        self.apply_theme_styles()

    def _setting_value(self, config_item):
        return getattr(config_item, "value", config_item)

    def _on_theme_changed(self, config_item):
        setTheme(self._setting_value(config_item), save=True)
        window = self.window()
        if hasattr(window, "apply_theme_styles"):
            window.apply_theme_styles()

    def _on_lang_changed(self, config_item):
        lang_code = self._setting_value(config_item)
        if lang_code == i18n.locale:
            return
        InfoBar.success(
            title=i18n.tr("settings_language_changed"),
            content=i18n.tr("settings_language_restart"),
            duration=5000,
            parent=self,
            position=InfoBarPosition.TOP,
        )

    def apply_theme_styles(self):
        apply_scroll_area_theme(self, self.view)
        self.title.setStyleSheet(color_style("font-size: 26px; font-weight: bold;", "text"))
