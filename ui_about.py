from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QPixmap, QIcon, QDesktopServices
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from qfluentwidgets import (SubtitleLabel, BodyLabel, CardWidget,
                            PushButton, FluentIcon as FIF, ScrollArea)

from i18n import i18n
import os, sys

if getattr(sys, 'frozen', False):
    data_dir = sys._MEIPASS
else:
    data_dir = os.path.dirname(os.path.abspath(__file__))


def _scale_pixmap_to_height(pixmap, target_height, widget):
    """Scale a QPixmap to a target logical height, accounting for DPR."""
    dpr = widget.devicePixelRatioF()
    scaled = pixmap.scaledToHeight(
        int(target_height * dpr), Qt.TransformationMode.SmoothTransformation
    )
    scaled.setDevicePixelRatio(dpr)
    return scaled


class AboutInterface(ScrollArea):
    """Generic About page — customize the URLs, text keys, and assets."""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("AboutInterface")
        self.view = QWidget(self)
        self.layout = QVBoxLayout(self.view)
        self.layout.setContentsMargins(24, 24, 24, 24)
        self.layout.setSpacing(20)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setStyleSheet("QScrollArea{background: transparent; border: none}")

        # ---- Top card: logo + name + version + links ----
        top_card = CardWidget()
        top_layout = QHBoxLayout(top_card)
        top_layout.setContentsMargins(20, 20, 20, 20)
        top_layout.setSpacing(15)

        logo_label = QLabel()
        logo_label.setStyleSheet("background: transparent;")
        logo_path = os.path.join(data_dir, "assets", "logo.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            if not pixmap.isNull():
                logo_label.setPixmap(
                    _scale_pixmap_to_height(pixmap, 60, self)
                )
        top_layout.addWidget(logo_label)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)
        name_lbl = SubtitleLabel("YourApp")
        name_lbl.setStyleSheet("font-size: 20px; font-weight: bold;")
        ver_lbl = BodyLabel(i18n.tr("about_ver"))
        ver_lbl.setStyleSheet("color: #a0a0a0;")
        info_layout.addWidget(name_lbl)
        info_layout.addWidget(ver_lbl)
        info_layout.addStretch(1)
        top_layout.addLayout(info_layout)
        top_layout.addStretch(1)

        def _make_brand_btn(icon_name, text_key, fallback_icon, url):
            btn = PushButton(i18n.tr(text_key))
            icon_path = os.path.join(data_dir, "assets", icon_name)
            if os.path.exists(icon_path):
                pix = QPixmap(icon_path)
                if not pix.isNull():
                    btn.setIcon(QIcon(_scale_pixmap_to_height(pix, 18, self)))
                else:
                    btn.setIcon(fallback_icon)
            else:
                btn.setIcon(fallback_icon)
            btn.clicked.connect(lambda u=url: QDesktopServices.openUrl(QUrl(u)))
            return btn

        btn_github = _make_brand_btn("github.png", "btn_github", FIF.SHARE,
                                     "https://github.com/yourusername/yourproject")
        btn_bilibili = _make_brand_btn("bilibili.png", "btn_bilibili", FIF.SHARE,
                                       "https://space.bilibili.com/")
        btn_qq = _make_brand_btn("", "btn_qq", FIF.CHAT,
                                 "https://qm.qq.com/your-group-link")
        btn_donate = _make_brand_btn("", "btn_donate", FIF.HEART,
                                     "https://afdian.com/a/yourname")

        top_layout.addWidget(btn_github)
        top_layout.addWidget(btn_bilibili)
        top_layout.addWidget(btn_qq)
        top_layout.addWidget(btn_donate)
        self.layout.addWidget(top_card)

        # ---- Author card ----
        author_title = SubtitleLabel(i18n.tr("about_author_title"))
        author_title.setStyleSheet("font-size: 22px; font-weight: bold; margin-top: 10px;")
        self.layout.addWidget(author_title)

        author_card = CardWidget()
        author_layout = QVBoxLayout(author_card)
        author_layout.setContentsMargins(20, 20, 20, 20)
        author_layout.setSpacing(10)

        intro_lbl = BodyLabel(i18n.tr("about_author"))
        intro_lbl.setStyleSheet("font-size: 16px; font-weight: bold;")
        desc_lbl = BodyLabel(i18n.tr("about_desc"))
        desc_lbl.setStyleSheet("color: #a0a0a0; font-size: 14px;")
        email_lbl = BodyLabel(i18n.tr("about_email"))
        qq_lbl = BodyLabel(i18n.tr("about_qq"))

        author_layout.addWidget(intro_lbl)
        author_layout.addWidget(desc_lbl)
        author_layout.addSpacing(10)
        author_layout.addWidget(email_lbl)
        author_layout.addWidget(qq_lbl)
        self.layout.addWidget(author_card)

        # ---- Copyright card ----
        copyright_title = SubtitleLabel(i18n.tr("about_cr_title"))
        copyright_title.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 10px;")
        self.layout.addWidget(copyright_title)

        copyright_card = CardWidget()
        copyright_layout = QVBoxLayout(copyright_card)
        copyright_layout.setContentsMargins(20, 20, 20, 20)
        copyright_layout.setSpacing(10)

        for key in ("about_ack1", "about_ack2", "about_ack3"):
            lbl = BodyLabel(i18n.tr(key))
            if key == "about_ack3":
                lbl.setStyleSheet("color: #a0a0a0; font-size: 12px;")
            lbl.setWordWrap(True)
            copyright_layout.addWidget(lbl)
        self.layout.addWidget(copyright_card)

        self.layout.addStretch(1)

        # ---- Warnings ----
        warn_container = QVBoxLayout()
        warn_container.setSpacing(6)
        warn_container.setContentsMargins(0, 0, 0, 0)

        for key in ("about_warn1", "about_warn2"):
            warn = BodyLabel(i18n.tr(key))
            warn.setStyleSheet("color: #ff5252; font-weight: bold; font-size: 14px;")
            warn.setWordWrap(True)
            warn_container.addWidget(warn)
        self.layout.addLayout(warn_container)
