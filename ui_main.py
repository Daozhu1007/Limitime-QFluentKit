import sys

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QLabel, QSizePolicy, QWidget
from qfluentwidgets import (
    FluentIcon as FIF,
    FluentWindow,
    NavigationItemPosition,
    qconfig,
    setTheme,
)

from app_config import APP_NAME, APP_USER_MODEL_ID
from i18n import i18n
from ui_about import AboutInterface
from ui_home import HomeInterface
from ui_settings import SettingsInterface
from ui_utils import (
    color_style,
    load_app_icon,
    resource_path,
    scale_pixmap_to_height,
    theme_color,
    theme_value,
)


class BrandingWidget(QWidget):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(48)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(12, 10, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.icon_label = QLabel(self)
        self.icon_label.setStyleSheet("background: transparent; border: none;")
        self.icon_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        for name in ("logo.png", "logo.jpg"):
            pixmap = QPixmap(resource_path(f"assets/{name}"))
            if not pixmap.isNull():
                self.icon_label.setPixmap(scale_pixmap_to_height(pixmap, 22, self))
                break

        self.title_label = QLabel(APP_NAME, self)
        self.title_label.setWordWrap(False)
        self.title_label.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Preferred,
        )
        self.layout.addWidget(self.icon_label)
        self.layout.addWidget(self.title_label)
        self.update_theme_styles()

    def update_theme_styles(self):
        self.title_label.setStyleSheet(
            "font-size: 15px; font-weight: bold; color: white; "
            "background: transparent; margin-left: 10px;"
        )

    def setSelected(self, selected: bool):
        pass

    def setCompacted(self, compacted: bool):
        pass


class MainWindow(FluentWindow):
    """Application shell with production-proven QFluentWidgets defaults."""

    def __init__(self):
        setTheme(qconfig.themeMode.value)
        super().__init__()

        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(load_app_icon())
        self.resize(1000, 660)
        self.setMinimumSize(900, 600)

        self.navigationInterface.setReturnButtonVisible(False)
        self.navigationInterface.setExpandWidth(207)
        self.navigationInterface.panel.setMinimumExpandWidth(800)

        if hasattr(self.titleBar, "titleLabel"):
            self.titleBar.titleLabel.hide()
        if hasattr(self.titleBar, "iconLabel"):
            self.titleBar.iconLabel.hide()

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

        self.home_interface = HomeInterface(self)
        self.settings_interface = SettingsInterface(self)
        self.about_interface = AboutInterface(self)

        self.addSubInterface(self.home_interface, FIF.HOME, i18n.tr("tab_home"))
        self.addSubInterface(
            self.settings_interface,
            FIF.SETTING,
            i18n.tr("tab_settings"),
            position=NavigationItemPosition.BOTTOM,
        )
        self.addSubInterface(
            self.about_interface,
            FIF.HELP,
            i18n.tr("tab_about"),
            position=NavigationItemPosition.BOTTOM,
        )

        self.navigationInterface.expand(False)
        qconfig.themeChangedFinished.connect(self.apply_theme_styles)
        self.apply_theme_styles()

    def apply_theme_styles(self):
        self._apply_window_theme_styles()
        for widget in (
            self.branding_widget,
            self.home_interface,
            self.settings_interface,
            self.about_interface,
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


if __name__ == "__main__":
    try:
        import ctypes

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_USER_MODEL_ID)
    except Exception:
        pass

    app = QApplication(sys.argv)
    app.setWindowIcon(load_app_icon())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
