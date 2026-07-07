import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget
from qfluentwidgets import (
    BodyLabel,
    CardWidget,
    FluentIcon as FIF,
    InfoBar,
    InfoBarPosition,
    PushButton,
    SubtitleLabel,
    TitleLabel,
)

from i18n import i18n
from ui_common import BaseMediaInterface, color_style, create_log_box


class AnalyzeInterface(BaseMediaInterface):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("AnalyzeInterface")
        self.view = QWidget(self)
        self.layout = QVBoxLayout(self.view)
        self.layout.setContentsMargins(24, 12, 24, 24)
        self.layout.setSpacing(12)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.apply_theme_styles()
        self.setup_ui()

    def setup_ui(self):
        top_layout = QHBoxLayout()
        self.title_label = SubtitleLabel(i18n.tr("tab_analyze"))
        self._set_title_style()
        top_layout.addWidget(self.title_label)
        top_layout.addStretch(1)

        self.btn_analyze = PushButton(FIF.SEARCH, i18n.tr("btn_calc"))
        top_layout.addWidget(self.btn_analyze)
        self.layout.addLayout(top_layout)

        card1 = CardWidget()
        card1_layout = QVBoxLayout(card1)
        card1_layout.setContentsMargins(20, 20, 20, 20)
        card1_layout.setSpacing(15)
        self.video_input, self.btn_vid = self.create_file_row(card1_layout, i18n.tr("lbl_video"))
        self.music_input, self.btn_mus = self.create_file_row(card1_layout, i18n.tr("lbl_music"))
        self.layout.addWidget(card1)
        self.layout.addSpacing(15)

        self.result_card = CardWidget()
        result_layout = QVBoxLayout(self.result_card)
        result_layout.setContentsMargins(20, 40, 20, 40)
        result_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.result_title = SubtitleLabel(i18n.tr("res_title"))
        self.result_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        result_layout.addWidget(self.result_title)

        self.result_display = TitleLabel(i18n.tr("res_placeholder"))
        self.result_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._set_result_display_style("accent")
        result_layout.addWidget(self.result_display)

        self.result_hint = BodyLabel(i18n.tr("res_hint"))
        self.result_hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._set_result_hint_style("muted")
        result_layout.addWidget(self.result_hint)
        self.layout.addWidget(self.result_card)

        self.layout.addLayout(self.create_progress_row(i18n.tr("status_analyzing")))

        self.log_box = create_log_box()
        self.layout.addWidget(self.log_box, 1)

        self.btn_vid.clicked.connect(lambda: self.select_file(self.video_input, i18n.tr("filter_video")))
        self.btn_mus.clicked.connect(lambda: self.select_file(self.music_input, i18n.tr("filter_audio")))
        self.btn_analyze.clicked.connect(self.start_analysis)

    def _set_title_style(self):
        self.title_label.setStyleSheet(color_style("font-size: 26px; font-weight: bold;", "text"))

    def _set_result_display_style(self, role):
        self.result_display_role = role
        self.result_display.setStyleSheet(
            color_style("font-size: 60px; font-weight: bold; margin: 20px 0;", role)
        )

    def _set_result_hint_style(self, role, size=14, bold=False):
        self.result_hint_role = role
        self.result_hint_size = size
        self.result_hint_bold = bold
        weight = " font-weight: bold;" if bold else ""
        self.result_hint.setStyleSheet(color_style(f"font-size: {size}px;{weight}", role))

    def apply_theme_styles(self):
        super().apply_theme_styles()
        if hasattr(self, "title_label"):
            self._set_title_style()
        if hasattr(self, "result_display"):
            self._set_result_display_style(getattr(self, "result_display_role", "accent"))
        if hasattr(self, "result_hint"):
            self._set_result_hint_style(
                getattr(self, "result_hint_role", "muted"),
                getattr(self, "result_hint_size", 14),
                getattr(self, "result_hint_bold", False),
            )

    def start_analysis(self):
        video_path, music_path = self.require_media_files()
        if not video_path or not music_path:
            return

        self.btn_analyze.setEnabled(False)
        self.result_display.setText(i18n.tr("analyze_pending"))
        self._set_result_display_style("muted")
        self.result_hint.setText(i18n.tr("hint_backend_pending"))
        self._set_result_hint_style("muted")
        self.log(i18n.tr("log_backend_analyze_params", os.path.basename(video_path), os.path.basename(music_path)))
        self.log(i18n.tr("log_backend_stub"))
        self.update_progress(i18n.tr("status_backend_ready"), 8, "--:--")

        if not self.run_analyze_backend(video_path, music_path):
            InfoBar.warning(
                title=i18n.tr("backend_pending_title"),
                content=i18n.tr("backend_pending_analysis"),
                parent=self,
                position=InfoBarPosition.TOP,
                duration=5000,
            )
            self.update_progress(i18n.tr("status_analyzing"), 0, "--:--")
            self.btn_analyze.setEnabled(True)

    def run_analyze_backend(self, video_path, music_path):
        # Hook for RhythmAlign's future AnalyzeWorker/find_offset integration.
        return False
