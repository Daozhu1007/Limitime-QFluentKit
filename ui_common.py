import os
import sys
import time

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QFont, QIcon, QPalette, QPixmap
from PyQt6.QtWidgets import QFileDialog, QHBoxLayout, QLabel
from qfluentwidgets import (
    BodyLabel,
    CardWidget,
    IndeterminateProgressBar,
    InfoBar,
    InfoBarPosition,
    LineEdit,
    ProgressBar,
    PushButton,
    ScrollArea,
    TextEdit,
    isDarkTheme,
)

from i18n import i18n


if getattr(sys, "frozen", False):
    data_dir = sys._MEIPASS
else:
    data_dir = os.path.dirname(os.path.abspath(__file__))


VIDEO_EXTENSIONS = {".mp4", ".mkv", ".mov", ".avi", ".flv", ".wmv", ".webm", ".ts"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg", ".wma"}
INDETERMINATE_PROGRESS = -1


def resource_path(relative_path):
    return os.path.join(data_dir, relative_path)


def scale_pixmap_to_height(pixmap, target_height, widget):
    dpr = widget.devicePixelRatioF()
    scaled = pixmap.scaledToHeight(
        int(target_height * dpr),
        Qt.TransformationMode.SmoothTransformation,
    )
    scaled.setDevicePixelRatio(dpr)
    return scaled


def load_app_icon():
    icon = QIcon(resource_path("assets/logo.ico"))
    if icon.isNull():
        icon = QIcon(resource_path("assets/logo.png"))
    return icon


def log_text_font():
    font = QFont("Consolas")
    font.setStyleHint(QFont.StyleHint.Monospace)
    return font


def media_kind(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in VIDEO_EXTENSIONS:
        return "video"
    if ext in AUDIO_EXTENSIONS:
        return "audio"
    return None


def event_file_paths(event):
    mime = event.mimeData()
    if not mime.hasUrls():
        return []
    return [url.toLocalFile() for url in mime.urls() if url.isLocalFile()]


def theme_color(role):
    colors = {
        "text": ("#ffffff", "#111827"),
        "muted": ("#a0a0a0", "#5f6b7a"),
        "accent": ("#60cdff", "#007f87"),
        "success": ("#2ecc71", "#107c41"),
        "danger": ("#ff6b6b", "#d13438"),
        "page": ("#202020", "#f0f4f9"),
        "stacked": ("#202020", "#f7f9fc"),
    }
    dark_color, light_color = colors[role]
    return dark_color if isDarkTheme() else light_color


def theme_value(dark_value, light_value):
    return dark_value if isDarkTheme() else light_value


def color_style(base_style, role):
    return f"{base_style} color: {theme_color(role)};"


def apply_scroll_area_theme(scroll_area, view):
    area_name = scroll_area.objectName() or scroll_area.__class__.__name__
    viewport = scroll_area.viewport()
    bg = theme_color("page")

    for widget in (view, viewport):
        palette = widget.palette()
        color = QColor(bg)
        palette.setColor(QPalette.ColorRole.Window, color)
        palette.setColor(QPalette.ColorRole.Base, color)
        widget.setPalette(palette)
        widget.setAutoFillBackground(True)
        widget.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, False)

    scroll_area.setStyleSheet(f"""
        QScrollArea#{area_name} {{
            background: transparent;
            border: none;
        }}
        QScrollArea#{area_name} QLabel {{
            background: transparent;
        }}
    """)
    viewport.setStyleSheet("")
    view.setStyleSheet("")


def format_elapsed(started_at):
    elapsed = max(0, int(time.monotonic() - started_at))
    minutes, seconds = divmod(elapsed, 60)
    return f"{minutes:02d}:{seconds:02d}"


class BaseMediaInterface(ScrollArea):
    """Shared media-page UI helpers. Backend integration hooks stay in subclasses."""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setAcceptDrops(True)
        self._busy_started_at = None
        self._busy_timer = QTimer(self)
        self._busy_timer.setInterval(1000)
        self._busy_timer.timeout.connect(self._refresh_busy_label)

    def apply_theme_styles(self):
        if hasattr(self, "view"):
            apply_scroll_area_theme(self, self.view)

    def create_file_row(self, layout, label_text):
        row = QHBoxLayout()
        row.setSpacing(12)
        label = BodyLabel(label_text)
        label.setMinimumWidth(96)
        input_box = LineEdit()
        input_box.setPlaceholderText(i18n.tr("placeholder_file"))
        input_box.setReadOnly(True)
        input_box.setAcceptDrops(False)
        btn = PushButton(i18n.tr("btn_browse"))
        row.addWidget(label)
        row.addWidget(input_box, 1)
        row.addWidget(btn)
        layout.addLayout(row)
        return input_box, btn

    def can_accept_dropped_media(self, paths):
        return any(os.path.isfile(path) and media_kind(path) for path in paths)

    def dragEnterEvent(self, event):
        if self.can_accept_dropped_media(event_file_paths(event)):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        self.dragEnterEvent(event)

    def dropEvent(self, event):
        if self.apply_dropped_media(event_file_paths(event)):
            event.acceptProposedAction()
        else:
            event.ignore()

    def apply_dropped_media(self, paths, show_feedback=True):
        if not hasattr(self, "video_input") or not hasattr(self, "music_input"):
            return False

        dropped_video = None
        dropped_audio = None
        for path in paths:
            if not os.path.isfile(path):
                continue
            kind = media_kind(path)
            if kind == "video" and dropped_video is None:
                dropped_video = path
            elif kind == "audio" and dropped_audio is None:
                dropped_audio = path

        updates = []
        if dropped_video:
            self.video_input.setText(dropped_video)
            updates.append(f"{i18n.tr('lbl_video').rstrip(':：')} {os.path.basename(dropped_video)}")
        if dropped_audio:
            self.music_input.setText(dropped_audio)
            updates.append(f"{i18n.tr('lbl_music').rstrip(':：')} {os.path.basename(dropped_audio)}")

        if not updates:
            if show_feedback:
                InfoBar.warning(
                    title=i18n.tr("msg_error"),
                    content=i18n.tr("drop_files_unsupported"),
                    parent=self,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                )
            return False

        if show_feedback:
            InfoBar.success(
                title=i18n.tr("msg_success"),
                content=i18n.tr("drop_files_ready", "; ".join(updates)),
                parent=self,
                position=InfoBarPosition.TOP,
                duration=2500,
            )
        return True

    def select_file(self, line_edit, filt):
        path, _ = QFileDialog.getOpenFileName(self, i18n.tr("dialog_open"), "", filt)
        if path:
            line_edit.setText(path)

    def require_media_files(self):
        video_path = self.video_input.text().strip()
        music_path = self.music_input.text().strip()
        if os.path.isfile(video_path) and os.path.isfile(music_path):
            return video_path, music_path

        InfoBar.error(
            title=i18n.tr("msg_error"),
            content=i18n.tr("err_select_files"),
            parent=self,
            position=InfoBarPosition.TOP,
        )
        return None, None

    def log(self, msg, state="normal"):
        prefix = "> "
        if state == "error":
            prefix = i18n.tr("log_prefix_err")
        elif state == "success":
            prefix = i18n.tr("log_prefix_ok")
        elif msg.startswith("-"):
            prefix = ""
        self.log_box.append(f"{prefix}{msg}")

    def create_progress_row(self, waiting_text):
        prog_layout = QHBoxLayout()
        prog_layout.setSpacing(12)
        self.prog_lbl = BodyLabel(waiting_text)
        self.prog_lbl.setMinimumWidth(220)
        self.prog_bar = ProgressBar()
        self.busy_prog_bar = IndeterminateProgressBar(start=False)
        self.busy_prog_bar.hide()
        prog_layout.addWidget(self.prog_lbl)
        prog_layout.addWidget(self.prog_bar)
        prog_layout.addWidget(self.busy_prog_bar)
        prog_layout.setStretchFactor(self.prog_bar, 1)
        prog_layout.setStretchFactor(self.busy_prog_bar, 1)
        return prog_layout

    def _refresh_busy_label(self):
        if self._busy_started_at is None:
            return
        self.prog_lbl.setText(
            i18n.tr("msg_progress_busy", self._busy_task, format_elapsed(self._busy_started_at))
        )

    def set_progress_busy(self, busy, task=None):
        if busy:
            self.prog_bar.hide()
            self.busy_prog_bar.show()
            if not self.busy_prog_bar.isStarted():
                self.busy_prog_bar.start()
            self._busy_task = task or i18n.tr("status_backend_ready")
            self._busy_started_at = time.monotonic()
            self._busy_timer.start()
            self._refresh_busy_label()
            return

        self._busy_timer.stop()
        self._busy_started_at = None
        if self.busy_prog_bar.isStarted():
            self.busy_prog_bar.stop()
        self.busy_prog_bar.hide()
        self.prog_bar.show()

    def update_progress(self, task, pct, eta="--:--"):
        if pct == INDETERMINATE_PROGRESS:
            self.set_progress_busy(True, task)
            return

        self.set_progress_busy(False)
        self.prog_lbl.setText(i18n.tr("msg_progress", task, pct, eta))
        self.prog_bar.setValue(int(pct))


def create_log_box():
    log_box = TextEdit()
    log_box.setReadOnly(True)
    log_box.setFont(log_text_font())
    return log_box


def create_card_layout(card=None, margins=(16, 16, 16, 16), spacing=10):
    card = card or CardWidget()
    from PyQt6.QtWidgets import QVBoxLayout

    layout = QVBoxLayout(card)
    layout.setContentsMargins(*margins)
    layout.setSpacing(spacing)
    return card, layout
