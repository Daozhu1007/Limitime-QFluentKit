from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import SubtitleLabel, BodyLabel, CardWidget

from i18n import i18n


class HomeInterface(QWidget):
    """Placeholder home page — replace with your own content."""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("HomeInterface")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 32, 24, 24)
        self.layout.setSpacing(16)

        title = SubtitleLabel(i18n.tr("home_title"))
        title.setStyleSheet("font-size: 26px; font-weight: bold;")
        self.layout.addWidget(title)

        card = CardWidget()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(10)

        desc = BodyLabel(i18n.tr("home_desc"))
        desc.setStyleSheet("color: #a0a0a0; font-size: 14px;")
        card_layout.addWidget(desc)

        self.layout.addWidget(card)
        self.layout.addStretch(1)
