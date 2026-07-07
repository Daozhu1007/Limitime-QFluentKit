from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices, QIcon
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget
from qfluentwidgets import (
    BodyLabel,
    CardWidget,
    FluentIcon as FIF,
    PushButton,
    ScrollArea,
    SubtitleLabel,
)

from app_config import (
    APP_AUTHOR,
    APP_DISPLAY_VERSION,
    APP_EMAIL,
    APP_NAME,
    BILIBILI_URL,
    COMMUNITY_URL,
    GITHUB_URL,
    SPONSOR_URL,
)
from i18n import i18n
from ui_utils import (
    apply_scroll_area_theme,
    color_style,
    optional_pixmap,
    resource_path,
    scale_pixmap_to_height,
)


class AboutInterface(ScrollArea):
    """Generic About page with safe layout for optional project links."""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("AboutInterface")
        self.view = QWidget(self)
        self.layout = QVBoxLayout(self.view)
        self.layout.setContentsMargins(24, 24, 24, 24)
        self.layout.setSpacing(20)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        top_card = CardWidget()
        top_layout = QVBoxLayout(top_card)
        top_layout.setContentsMargins(20, 20, 20, 20)
        top_layout.setSpacing(14)

        identity_layout = QHBoxLayout()
        identity_layout.setSpacing(15)
        logo_label = QLabel()
        logo_label.setStyleSheet("background: transparent;")
        logo = optional_pixmap("logo.png")
        if not logo.isNull():
            logo_label.setPixmap(scale_pixmap_to_height(logo, 60, self))
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

        link_layout = QHBoxLayout()
        link_layout.setSpacing(12)
        link_layout.addWidget(
            self._link_button("github.png", "btn_github", FIF.SHARE, GITHUB_URL)
        )
        link_layout.addWidget(
            self._link_button("bilibili.png", "btn_bilibili", FIF.SHARE, BILIBILI_URL)
        )
        link_layout.addWidget(
            self._link_button("", "btn_community", FIF.CHAT, COMMUNITY_URL)
        )
        link_layout.addWidget(
            self._link_button("", "btn_donate", FIF.HEART, SPONSOR_URL)
        )
        link_layout.addStretch(1)
        top_layout.addLayout(link_layout)
        self.layout.addWidget(top_card)

        self.author_title = SubtitleLabel(i18n.tr("about_author_title"))
        self.layout.addWidget(self.author_title)

        author_card = CardWidget()
        author_layout = QVBoxLayout(author_card)
        author_layout.setContentsMargins(20, 20, 20, 20)
        author_layout.setSpacing(10)
        self.author_lbl = BodyLabel(i18n.tr("about_author", APP_AUTHOR))
        self.author_lbl.setWordWrap(True)
        self.desc_lbl = BodyLabel(i18n.tr("about_desc"))
        self.desc_lbl.setWordWrap(True)
        self.email_lbl = BodyLabel(i18n.tr("about_email", APP_EMAIL))
        self.email_lbl.setWordWrap(True)
        author_layout.addWidget(self.author_lbl)
        author_layout.addWidget(self.desc_lbl)
        author_layout.addSpacing(10)
        author_layout.addWidget(self.email_lbl)
        self.layout.addWidget(author_card)

        self.warning_1 = BodyLabel(i18n.tr("about_warn1"))
        self.warning_2 = BodyLabel(i18n.tr("about_warn2"))
        self.warning_1.setWordWrap(True)
        self.warning_2.setWordWrap(True)
        self.layout.addStretch(1)
        self.layout.addWidget(self.warning_1)
        self.layout.addWidget(self.warning_2)
        self.apply_theme_styles()

    def _link_button(self, icon_name, text_key, fallback_icon, url):
        btn = PushButton(i18n.tr(text_key))
        pixmap = optional_pixmap(icon_name)
        if not pixmap.isNull():
            btn.setIcon(QIcon(scale_pixmap_to_height(pixmap, 18, self)))
        else:
            btn.setIcon(fallback_icon)
        btn.clicked.connect(lambda checked, link=url: QDesktopServices.openUrl(QUrl(link)))
        return btn

    def apply_theme_styles(self):
        apply_scroll_area_theme(self, self.view)
        self.name_lbl.setStyleSheet(color_style("font-size: 20px; font-weight: bold;", "text"))
        self.ver_lbl.setStyleSheet(color_style("", "muted"))
        self.author_title.setStyleSheet(
            color_style("font-size: 22px; font-weight: bold; margin-top: 10px;", "text")
        )
        self.author_lbl.setStyleSheet(color_style("font-size: 16px; font-weight: bold;", "text"))
        self.desc_lbl.setStyleSheet(color_style("font-size: 14px;", "muted"))
        self.email_lbl.setStyleSheet(color_style("", "text"))
        warning_style = color_style("font-weight: bold; font-size: 14px;", "danger")
        self.warning_1.setStyleSheet(warning_style)
        self.warning_2.setStyleSheet(warning_style)
