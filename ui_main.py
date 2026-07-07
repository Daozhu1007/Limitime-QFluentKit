import os
import sys

from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QLabel, QSizePolicy, QWidget
from qfluentwidgets import (
    FluentIcon as FIF,
    FluentWindow,
    InfoBar,
    InfoBarPosition,
    NavigationItemPosition,
    qconfig,
    setTheme,
)

from app_config import (
    APP_DISPLAY_VERSION,
    APP_NAME,
    APP_PUBLISHER,
    APP_TITLE,
    WINDOWS_APP_USER_MODEL_ID,
    cfg,
)
from i18n import i18n
from ui_about import AboutInterface
from ui_analyze import AnalyzeInterface
from ui_common import (
    BaseMediaInterface,
    color_style,
    event_file_paths,
    load_app_icon,
    resource_path,
    scale_pixmap_to_height,
    theme_color,
    theme_value,
)
from ui_settings import SettingsInterface
from ui_sync import SyncInterface


class BrandingWidget(QWidget):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(48)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(12, 10, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.icon_label = QLabel(self)
        self.icon_label.setStyleSheet("background: transparent;")
        self.icon_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        pixmap = QPixmap(resource_path("assets/logo.png"))
        if not pixmap.isNull():
            self.icon_label.setPixmap(scale_pixmap_to_height(pixmap, 20, self))

        self.title_label = QLabel(APP_TITLE, self)
        self.title_label.setWordWrap(False)
        self.title_label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        self.update_theme_styles()

        self.layout.addWidget(self.icon_label)
        self.layout.addWidget(self.title_label)

    def update_theme_styles(self):
        self.title_label.setStyleSheet(
            color_style(
                "font-size: 14px; font-weight: normal; background: transparent; margin-left: 8px;",
                "text",
            )
        )

    def setSelected(self, selected: bool):
        pass

    def setCompacted(self, compacted: bool):
        pass


class MainWindow(FluentWindow):
    def __init__(self):
        setTheme(qconfig.themeMode.value)
        super().__init__()
        self.setAcceptDrops(True)

        self.setWindowTitle(APP_TITLE)
        self.setWindowIcon(load_app_icon())
        self.resize(1050, 720)
        self.setMinimumSize(1024, 550)

        self.navigationInterface.setReturnButtonVisible(False)
        self.navigationInterface.setExpandWidth(210)
        self.navigationInterface.panel.setMinimumExpandWidth(820)

        if hasattr(self, "titleBar"):
            if hasattr(self.titleBar, "iconLabel"):
                self.titleBar.iconLabel.hide()
            if hasattr(self.titleBar, "titleLabel"):
                self.titleBar.titleLabel.hide()

        try:
            nav_panel = self.navigationInterface.panel
            nav_panel.vBoxLayout.removeWidget(nav_panel.menuButton)
            nav_panel.menuButton.hide()
            nav_panel.menuButton.setParent(None)
        except Exception:
            pass

        self.branding_widget = BrandingWidget(self)
        self.navigationInterface.addWidget(
            routeKey="branding",
            widget=self.branding_widget,
            onClick=None,
            position=NavigationItemPosition.TOP,
        )

        self.sync_interface = SyncInterface(self)
        self.analyze_interface = AnalyzeInterface(self)
        self.about_interface = AboutInterface(self)
        self.setting_interface = SettingsInterface(self)

        self.addSubInterface(self.sync_interface, FIF.PLAY, i18n.tr("tab_sync"))
        self.addSubInterface(self.analyze_interface, FIF.SEARCH, i18n.tr("tab_analyze"))
        self.addSubInterface(
            self.about_interface,
            FIF.HELP,
            i18n.tr("tab_about"),
            position=NavigationItemPosition.BOTTOM,
        )
        self.addSubInterface(
            self.setting_interface,
            FIF.SETTING,
            i18n.tr("tab_settings"),
            position=NavigationItemPosition.BOTTOM,
        )

        self.navigationInterface.expand(False)
        qconfig.themeChangedFinished.connect(self.apply_theme_styles)
        self.apply_theme_styles()

        if cfg.check_updates_on_startup.value:
            QTimer.singleShot(2500, lambda: self.check_for_updates(silent=True))

    def apply_theme_styles(self):
        self._apply_window_theme_styles()
        for widget in (
            self.branding_widget,
            self.sync_interface,
            self.analyze_interface,
            self.about_interface,
            self.setting_interface,
        ):
            if hasattr(widget, "apply_theme_styles"):
                widget.apply_theme_styles()
            elif hasattr(widget, "update_theme_styles"):
                widget.update_theme_styles()

    def _apply_window_theme_styles(self):
        self.setCustomBackgroundColor("#f0f4f9", "#202020")
        stacked_bg = theme_color("stacked")
        border_color = theme_value("rgba(255, 255, 255, 0.08)", "rgba(0, 0, 0, 0.08)")

        self.stackedWidget.setStyleSheet(f"""
            StackedWidget {{
                border: 1px solid {border_color};
                border-right: none;
                border-bottom: none;
                border-top-left-radius: 10px;
                background-color: {stacked_bg};
            }}
            StackedWidget[isTransparent=true] {{
                background-color: {stacked_bg};
                border: none;
            }}
        """)
        self.stackedWidget.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.stackedWidget.view.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.stackedWidget.view.setStyleSheet(f"background-color: {stacked_bg}; border: none;")

    def _current_media_interface(self):
        current = self.stackedWidget.currentWidget()
        return current if isinstance(current, BaseMediaInterface) else None

    def dragEnterEvent(self, event):
        interface = self._current_media_interface()
        if interface and interface.can_accept_dropped_media(event_file_paths(event)):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        self.dragEnterEvent(event)

    def dropEvent(self, event):
        interface = self._current_media_interface()
        if interface and interface.apply_dropped_media(event_file_paths(event)):
            event.acceptProposedAction()
        else:
            event.ignore()

    def check_for_updates(self, silent=False):
        if hasattr(self.setting_interface, "set_update_status"):
            self.setting_interface.set_update_status(i18n.tr("update_checking_desc"), busy=True)
        QTimer.singleShot(700, lambda: self._finish_update_placeholder(silent))

    def _finish_update_placeholder(self, silent):
        if hasattr(self.setting_interface, "set_update_status"):
            self.setting_interface.set_update_status(i18n.tr("update_stub_status"), busy=False)
        if not silent:
            InfoBar.info(
                title=i18n.tr("backend_pending_title"),
                content=i18n.tr("backend_pending_update"),
                parent=self,
                position=InfoBarPosition.TOP,
                duration=4500,
            )

    def copy_diagnostics(self):
        report = "\n".join(
            [
                f"App: {APP_NAME} {APP_DISPLAY_VERSION}",
                f"Publisher: {APP_PUBLISHER}",
                f"Theme: {qconfig.themeMode.value}",
                f"Language: {cfg.language.value}",
                f"StreamCopy: {cfg.stream_copy.value}",
                f"UseGPU: {cfg.use_gpu.value}",
                f"Bitrate: {cfg.bitrate.value}",
                "Backend: not connected in QFluentKit UI template",
            ]
        )
        QApplication.clipboard().setText(report)
        InfoBar.success(
            title=i18n.tr("diagnostics_copied_title"),
            content=i18n.tr("diagnostics_copied_desc"),
            parent=self,
            position=InfoBarPosition.TOP,
            duration=3500,
        )


if __name__ == "__main__":
    try:
        import ctypes

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(WINDOWS_APP_USER_MODEL_ID)
    except Exception:
        pass

    app = QApplication(sys.argv)
    app.setWindowIcon(load_app_icon())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
