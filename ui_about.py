from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices, QIcon, QPixmap
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QLabel, QVBoxLayout, QWidget
from qfluentwidgets import (
    BodyLabel,
    CardWidget,
    FluentIcon as FIF,
    InfoBar,
    InfoBarPosition,
    PushButton,
    ScrollArea,
    SubtitleLabel,
)

from app_config import (
    APP_DISPLAY_VERSION,
    APP_NAME,
    BILIBILI_URL,
    DONATE_URL,
    GITHUB_HOME_URL,
    QQ_GROUP_ID,
)
from i18n import i18n
from ui_common import (
    apply_scroll_area_theme,
    color_style,
    resource_path,
    scale_pixmap_to_height,
)


class AboutInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("AboutInterface")
        self.view = QWidget(self)
        self.layout = QVBoxLayout(self.view)
        self.layout.setContentsMargins(24, 24, 24, 24)
        self.layout.setSpacing(20)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.apply_theme_styles()

        top_card = CardWidget()
        top_layout = QVBoxLayout(top_card)
        top_layout.setContentsMargins(20, 20, 20, 20)
        top_layout.setSpacing(14)

        identity_layout = QHBoxLayout()
        identity_layout.setSpacing(15)

        logo_label = QLabel()
        logo_label.setStyleSheet("background: transparent;")
        pixmap = QPixmap(resource_path("assets/logo.png"))
        if not pixmap.isNull():
            logo_label.setPixmap(scale_pixmap_to_height(pixmap, 60, self))
        identity_layout.addWidget(logo_label)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)
        self.name_lbl = SubtitleLabel(APP_NAME)
        self.ver_lbl = BodyLabel(APP_DISPLAY_VERSION)
        info_layout.addWidget(self.name_lbl)
        info_layout.addWidget(self.ver_lbl)
        info_layout.addStretch(1)
        identity_layout.addLayout(info_layout)
        identity_layout.addStretch(1)
        top_layout.addLayout(identity_layout)

        btn_github = self._branding_button(resource_path("assets/github.png"), "GitHub", FIF.SHARE)
        btn_bilibili = self._branding_button(resource_path("assets/bilibili.png"), "Bilibili", FIF.SHARE)
        btn_qq = PushButton(FIF.CHAT, i18n.tr("btn_qq"))
        btn_donate = PushButton(FIF.HEART, i18n.tr("btn_donate"))
        btn_github.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(GITHUB_HOME_URL)))
        btn_bilibili.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(BILIBILI_URL)))
        btn_qq.clicked.connect(self.copy_qq_group)
        btn_donate.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(DONATE_URL)))

        link_layout = QHBoxLayout()
        link_layout.setSpacing(12)
        link_layout.addWidget(btn_github)
        link_layout.addWidget(btn_bilibili)
        link_layout.addWidget(btn_qq)
        link_layout.addWidget(btn_donate)
        link_layout.addStretch(1)
        top_layout.addLayout(link_layout)
        self.layout.addWidget(top_card)

        self.author_title = SubtitleLabel(i18n.tr("about_author_title"))
        self.layout.addWidget(self.author_title)

        author_card = CardWidget()
        author_layout = QVBoxLayout(author_card)
        author_layout.setContentsMargins(20, 20, 20, 20)
        author_layout.setSpacing(10)
        self.intro_lbl = BodyLabel(i18n.tr("about_author"))
        self.desc_lbl = BodyLabel(i18n.tr("about_desc"))
        self.desc_lbl.setWordWrap(True)
        email_lbl = BodyLabel(i18n.tr("about_email"))
        qq_lbl = BodyLabel(i18n.tr("about_qq"))
        author_layout.addWidget(self.intro_lbl)
        author_layout.addWidget(self.desc_lbl)
        author_layout.addSpacing(10)
        author_layout.addWidget(email_lbl)
        author_layout.addWidget(qq_lbl)
        self.layout.addWidget(author_card)

        self.copyright_title = SubtitleLabel(i18n.tr("about_cr_title"))
        self.layout.addWidget(self.copyright_title)

        copyright_card = CardWidget()
        copyright_layout = QVBoxLayout(copyright_card)
        copyright_layout.setContentsMargins(20, 20, 20, 20)
        copyright_layout.setSpacing(10)
        ack_labels = []
        for key in ("about_ack1", "about_ack2", "about_ack3"):
            label = BodyLabel(i18n.tr(key))
            label.setWordWrap(True)
            copyright_layout.addWidget(label)
            ack_labels.append(label)
        self.ack3 = ack_labels[-1]
        self.layout.addWidget(copyright_card)

        self.layout.addStretch(1)

        warn_container = QVBoxLayout()
        warn_container.setSpacing(6)
        warn_container.setContentsMargins(0, 0, 0, 0)
        self.warn1 = BodyLabel(i18n.tr("about_warn1"))
        self.warn2 = BodyLabel(i18n.tr("about_warn2"))
        self.warn1.setWordWrap(True)
        self.warn2.setWordWrap(True)
        warn_container.addWidget(self.warn1)
        warn_container.addWidget(self.warn2)
        self.layout.addLayout(warn_container)
        self.apply_theme_styles()

    def _branding_button(self, icon_path, text, fallback_icon):
        btn = PushButton(text)
        if icon_path and QPixmap(icon_path).isNull() is False:
            pixmap = QPixmap(icon_path)
            btn.setIcon(QIcon(scale_pixmap_to_height(pixmap, 18, self)))
        else:
            btn.setIcon(fallback_icon)
        return btn

    def apply_theme_styles(self):
        apply_scroll_area_theme(self, self.view)
        if not hasattr(self, "name_lbl"):
            return
        self.name_lbl.setStyleSheet(color_style("font-size: 20px; font-weight: bold;", "text"))
        self.ver_lbl.setStyleSheet(color_style("", "muted"))
        self.author_title.setStyleSheet(color_style("font-size: 22px; font-weight: bold; margin-top: 10px;", "text"))
        self.intro_lbl.setStyleSheet(color_style("font-size: 16px; font-weight: bold;", "text"))
        self.desc_lbl.setStyleSheet(color_style("font-size: 14px;", "muted"))
        self.copyright_title.setStyleSheet(color_style("font-size: 18px; font-weight: bold; margin-top: 10px;", "text"))
        self.ack3.setStyleSheet(color_style("font-size: 12px;", "muted"))
        warning_style = color_style("font-weight: bold; font-size: 14px;", "danger")
        self.warn1.setStyleSheet(warning_style)
        self.warn2.setStyleSheet(warning_style)

    def copy_qq_group(self):
        QApplication.clipboard().setText(QQ_GROUP_ID)
        InfoBar.success(
            title=i18n.tr("msg_success"),
            content=i18n.tr("msg_qq_group_copied", QQ_GROUP_ID),
            parent=self,
            position=InfoBarPosition.TOP,
            duration=2500,
        )
