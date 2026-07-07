from PyQt6.QtWidgets import QVBoxLayout, QWidget
from qfluentwidgets import BodyLabel, CardWidget, ScrollArea, SubtitleLabel

from i18n import i18n
from ui_utils import apply_scroll_area_theme, color_style


class HomeInterface(ScrollArea):
    """Starter home page. Replace this with your first real product view."""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("HomeInterface")
        self.view = QWidget(self)
        self.layout = QVBoxLayout(self.view)
        self.layout.setContentsMargins(24, 24, 24, 24)
        self.layout.setSpacing(16)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.title = SubtitleLabel(i18n.tr("home_title"))
        self.layout.addWidget(self.title)

        card = CardWidget()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(10)

        self.desc = BodyLabel(i18n.tr("home_desc"))
        self.desc.setWordWrap(True)
        card_layout.addWidget(self.desc)

        self.layout.addWidget(card)
        self.layout.addStretch(1)
        self.apply_theme_styles()

    def apply_theme_styles(self):
        apply_scroll_area_theme(self, self.view)
        self.title.setStyleSheet(color_style("font-size: 26px; font-weight: bold;", "text"))
        self.desc.setStyleSheet(color_style("font-size: 14px;", "muted"))
