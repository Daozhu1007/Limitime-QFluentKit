from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import QVBoxLayout, QWidget
from qfluentwidgets import (
    FluentIcon as FIF,
    InfoBar,
    InfoBarPosition,
    OptionsSettingCard,
    PrimaryPushSettingCard,
    PushSettingCard,
    ScrollArea,
    SettingCardGroup,
    SubtitleLabel,
    SwitchSettingCard,
    qconfig,
    setTheme,
)

from app_config import (
    APP_DISPLAY_VERSION,
    GITHUB_RELEASES_URL,
    LANG_OPTIONS,
    THEME_TEXT_KEYS,
    cfg,
)
from i18n import i18n
from ui_common import apply_scroll_area_theme, color_style


class SettingsInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("SettingsInterface")
        self.view = QWidget(self)
        self.layout = QVBoxLayout(self.view)
        self.layout.setContentsMargins(24, 12, 24, 24)
        self.layout.setSpacing(16)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.apply_theme_styles()

        self.title_label = SubtitleLabel(i18n.tr("tab_settings"))
        self._set_title_style()
        self.layout.addWidget(self.title_label)

        self.general_group = SettingCardGroup(i18n.tr("set_general"), self.view)
        self.theme_combo = OptionsSettingCard(
            configItem=qconfig.themeMode,
            icon=FIF.PALETTE,
            title=i18n.tr("set_theme"),
            content=i18n.tr("set_theme_desc"),
            texts=[i18n.tr(THEME_TEXT_KEYS[theme]) for theme in qconfig.themeMode.options],
            parent=self.general_group,
        )
        self.theme_combo.optionChanged.connect(self._on_theme_changed)

        self.lang_combo = OptionsSettingCard(
            configItem=cfg.language,
            icon=FIF.LANGUAGE,
            title=i18n.tr("set_lang"),
            content=i18n.tr("set_lang_desc"),
            texts=[i18n.tr(LANG_OPTIONS[code]) for code in LANG_OPTIONS],
            parent=self.general_group,
        )
        self.lang_combo.setToolTip(i18n.tr("set_lang_tooltip"))
        self.lang_combo.optionChanged.connect(self._on_lang_changed)

        self.folder_switch = SwitchSettingCard(
            icon=FIF.FOLDER,
            title=i18n.tr("set_folder"),
            content=i18n.tr("set_folder_desc"),
            configItem=cfg.open_folder,
            parent=self.general_group,
        )

        self.general_group.addSettingCard(self.theme_combo)
        self.general_group.addSettingCard(self.lang_combo)
        self.general_group.addSettingCard(self.folder_switch)
        self.layout.addWidget(self.general_group)

        self.video_group = SettingCardGroup(i18n.tr("set_video"), self.view)
        self.copy_switch = SwitchSettingCard(
            icon=FIF.SEND,
            title=i18n.tr("set_copy"),
            content=i18n.tr("set_copy_desc"),
            configItem=cfg.stream_copy,
            parent=self.video_group,
        )
        self.gpu_switch = SwitchSettingCard(
            icon=FIF.GAME,
            title=i18n.tr("set_gpu"),
            content=i18n.tr("set_gpu_desc"),
            configItem=cfg.use_gpu,
            parent=self.video_group,
        )
        self.bitrate_combo = OptionsSettingCard(
            configItem=cfg.bitrate,
            icon=FIF.VIDEO,
            title=i18n.tr("set_bitrate"),
            content=i18n.tr("set_bitrate_desc"),
            texts=[i18n.tr("bitrate_6k"), i18n.tr("bitrate_10k"), i18n.tr("bitrate_20k")],
            parent=self.video_group,
        )
        self.video_group.addSettingCard(self.copy_switch)
        self.video_group.addSettingCard(self.gpu_switch)
        self.video_group.addSettingCard(self.bitrate_combo)
        self.layout.addWidget(self.video_group)

        self.update_group = SettingCardGroup(i18n.tr("set_update"), self.view)
        self.update_startup_switch = SwitchSettingCard(
            icon=FIF.SYNC,
            title=i18n.tr("set_update_auto"),
            content=i18n.tr("set_update_auto_desc"),
            configItem=cfg.check_updates_on_startup,
            parent=self.update_group,
        )
        self.update_check_card = PrimaryPushSettingCard(
            i18n.tr("btn_check_update"),
            FIF.UPDATE,
            i18n.tr("set_update_check"),
            i18n.tr("set_update_check_desc", APP_DISPLAY_VERSION),
            parent=self.update_group,
        )
        self.update_check_card.clicked.connect(self._on_check_update_clicked)

        self.release_card = PushSettingCard(
            i18n.tr("btn_open_release"),
            FIF.LINK,
            i18n.tr("set_update_release"),
            i18n.tr("set_update_release_desc"),
            parent=self.update_group,
        )
        self.release_card.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(GITHUB_RELEASES_URL)))
        self.update_group.addSettingCard(self.update_startup_switch)
        self.update_group.addSettingCard(self.update_check_card)
        self.update_group.addSettingCard(self.release_card)
        self.layout.addWidget(self.update_group)

        self.diagnostic_group = SettingCardGroup(i18n.tr("set_diagnostics"), self.view)
        self.diagnostic_card = PushSettingCard(
            i18n.tr("btn_copy_diagnostics"),
            FIF.COPY,
            i18n.tr("set_diagnostics_copy"),
            i18n.tr("set_diagnostics_copy_desc"),
            parent=self.diagnostic_group,
        )
        self.diagnostic_card.clicked.connect(self._on_copy_diagnostics_clicked)
        self.diagnostic_group.addSettingCard(self.diagnostic_card)
        self.layout.addWidget(self.diagnostic_group)

        self.layout.addStretch(1)

    def _setting_value(self, config_item):
        return getattr(config_item, "value", config_item)

    def _on_lang_changed(self, config_item):
        lang_code = self._setting_value(config_item)
        if lang_code == i18n.locale:
            return
        InfoBar.success(
            title=i18n.tr("set_lang_changed"),
            content=i18n.tr("set_lang_restart"),
            duration=5000,
            parent=self,
            position=InfoBarPosition.TOP,
        )

    def _on_theme_changed(self, config_item):
        setTheme(self._setting_value(config_item), save=True)
        window = self.window()
        if hasattr(window, "apply_theme_styles"):
            window.apply_theme_styles()

    def _on_check_update_clicked(self):
        window = self.window()
        if hasattr(window, "check_for_updates"):
            window.check_for_updates(silent=False)

    def _on_copy_diagnostics_clicked(self):
        window = self.window()
        if hasattr(window, "copy_diagnostics"):
            window.copy_diagnostics()

    def apply_theme_styles(self):
        apply_scroll_area_theme(self, self.view)
        if hasattr(self, "title_label"):
            self._set_title_style()

    def _set_title_style(self):
        self.title_label.setStyleSheet(
            color_style("font-size: 26px; font-weight: bold; margin-bottom: 15px;", "text")
        )

    def set_update_status(self, text=None, busy=False):
        if text:
            self.update_check_card.contentLabel.setText(text)
        else:
            self.update_check_card.contentLabel.setText(i18n.tr("set_update_check_desc", APP_DISPLAY_VERSION))
        self.update_check_card.button.setEnabled(not busy)
