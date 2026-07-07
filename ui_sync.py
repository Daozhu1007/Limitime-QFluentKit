import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog, QHBoxLayout, QVBoxLayout, QWidget
from qfluentwidgets import (
    BodyLabel,
    CardWidget,
    FluentIcon as FIF,
    InfoBar,
    InfoBarPosition,
    PushButton,
    Slider,
    SubtitleLabel,
)

from app_config import cfg
from i18n import i18n
from ui_common import (
    BaseMediaInterface,
    color_style,
    create_log_box,
    INDETERMINATE_PROGRESS,
)


class SyncInterface(BaseMediaInterface):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("SyncInterface")
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
        self.title_label = SubtitleLabel(i18n.tr("sync_title"))
        self._set_title_style()
        top_layout.addWidget(self.title_label)
        top_layout.addStretch(1)

        self.btn_start = PushButton(FIF.PLAY, i18n.tr("btn_export"))
        top_layout.addWidget(self.btn_start)
        self.layout.addLayout(top_layout)

        card1 = CardWidget()
        card1_layout = QVBoxLayout(card1)
        card1_layout.setContentsMargins(16, 16, 16, 16)
        card1_layout.setSpacing(10)
        self.video_input, self.btn_vid = self.create_file_row(card1_layout, i18n.tr("lbl_video"))
        self.music_input, self.btn_mus = self.create_file_row(card1_layout, i18n.tr("lbl_music"))
        self.layout.addWidget(card1)
        self.layout.addSpacing(15)

        card2 = CardWidget()
        card2_layout = QVBoxLayout(card2)
        card2_layout.setContentsMargins(16, 20, 16, 20)
        card2_layout.setSpacing(24)

        preset_layout = QHBoxLayout()
        preset_layout.setSpacing(12)
        preset_layout.addWidget(BodyLabel(i18n.tr("lbl_preset")))
        for name, orig, music in (
            (i18n.tr("preset_arcade"), 1.2, 0.7),
            (i18n.tr("preset_mobile"), 2.0, 0.5),
            (i18n.tr("preset_desktop"), 1.0, 0.9),
        ):
            btn = PushButton(name)
            btn.clicked.connect(lambda checked, o=orig, m=music: self.apply_preset(o, m))
            preset_layout.addWidget(btn)
        preset_layout.addStretch(1)
        card2_layout.addLayout(preset_layout)

        self.orig_slider, self.orig_lbl = self.create_slider_row(
            card2_layout, i18n.tr("lbl_orig_vol"), 0, 200, 120, "%"
        )
        self.music_slider, self.music_lbl = self.create_slider_row(
            card2_layout, i18n.tr("lbl_music_vol"), 0, 200, 60, "%"
        )
        self.offset_slider, self.offset_lbl = self.create_slider_row(
            card2_layout, i18n.tr("lbl_offset"), -500, 500, 0, "ms"
        )
        self.layout.addWidget(card2)

        self.layout.addLayout(self.create_progress_row(i18n.tr("status_waiting")))

        self.log_box = create_log_box()
        self.layout.addWidget(self.log_box, 1)

        self.btn_vid.clicked.connect(lambda: self.select_file(self.video_input, i18n.tr("filter_video")))
        self.btn_mus.clicked.connect(lambda: self.select_file(self.music_input, i18n.tr("filter_audio")))
        self.btn_start.clicked.connect(self.start_task)

    def _set_title_style(self):
        self.title_label.setStyleSheet(color_style("font-size: 26px; font-weight: bold;", "text"))

    def apply_theme_styles(self):
        super().apply_theme_styles()
        if hasattr(self, "title_label"):
            self._set_title_style()

    def create_slider_row(self, layout, name, min_val, max_val, default, unit):
        row = QHBoxLayout()
        row.setSpacing(16)
        lbl = BodyLabel(f"{name}: {default}{unit}")
        lbl.setMinimumWidth(170)
        slider = Slider(Qt.Orientation.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(default)
        slider.valueChanged.connect(lambda value: lbl.setText(f"{name}: {value}{unit}"))
        row.addWidget(lbl)
        row.addWidget(slider, 1)
        layout.addLayout(row)
        return slider, lbl

    def apply_preset(self, orig, music):
        self.orig_slider.setValue(int(orig * 100))
        self.music_slider.setValue(int(music * 100))
        self.offset_slider.setValue(0)

    def start_task(self):
        video_path, music_path = self.require_media_files()
        if not video_path or not music_path:
            return

        base_name, ext = os.path.splitext(video_path)
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            i18n.tr("dialog_save"),
            f"{base_name}_synced{ext}",
            "MP4 Video (*.mp4)",
        )
        if not save_path:
            return

        params = {
            "v_path": video_path,
            "m_path": music_path,
            "save_path": save_path,
            "orig_vol": self.orig_slider.value() / 100.0,
            "music_vol": self.music_slider.value() / 100.0,
            "manual_offset": self.offset_slider.value() / 1000.0,
            "use_gpu": cfg.use_gpu.value,
            "bitrate": cfg.bitrate.value,
            "open_folder": cfg.open_folder.value,
            "stream_copy": cfg.stream_copy.value,
        }

        self.btn_start.setEnabled(False)
        self.log(i18n.tr("log_backend_sync_params", os.path.basename(video_path), os.path.basename(music_path)))
        self.log(i18n.tr("log_backend_stub"))
        self.update_progress(i18n.tr("status_backend_ready"), 8, "--:--")
        if not self.run_sync_backend(params):
            self.update_progress(i18n.tr("status_waiting"), 0, "--:--")
            InfoBar.warning(
                title=i18n.tr("backend_pending_title"),
                content=i18n.tr("backend_pending_sync"),
                parent=self,
                position=InfoBarPosition.TOP,
                duration=5000,
            )
            self.btn_start.setEnabled(True)

    def run_sync_backend(self, params):
        # Hook for RhythmAlign's future SyncWorker/mix_and_export integration.
        return False
