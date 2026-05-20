import sys
import os

if getattr(sys, 'frozen', False):
    data_dir = sys._MEIPASS
else:
    data_dir = os.path.dirname(os.path.abspath(__file__))

from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
from qfluentwidgets import (FluentWindow, FluentIcon as FIF,
                            NavigationItemPosition, Theme, setTheme, qconfig)

from i18n import i18n
from ui_home import HomeInterface
from ui_settings import SettingsInterface
from ui_about import AboutInterface


# ---------------------------------------------------------------------------
# BrandingWidget — logo + title in the navigation sidebar
# ---------------------------------------------------------------------------

class BrandingWidget(QWidget):
    """A clickable branding badge that lives at the top of the nav sidebar.

    Key layout constraints (DO NOT REMOVE):
      - icon_label: Fixed size policy    → logo never resizes
      - title_label: Minimum horizontal  → text never clips below its natural width
      - setWordWrap(False)              → no multi-line fallback
    """

    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(48)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(16, 12, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # Icon — fixed size, never resize
        self.icon_label = QLabel(self)
        self.icon_label.setStyleSheet(
            "background-color: rgba(255, 255, 255, 0.85); border-radius: 4px; padding: 2px;"
        )
        self.icon_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        logo_path = os.path.join(data_dir, "assets", "logo.png")
        if not os.path.exists(logo_path):
            logo_path = os.path.join(data_dir, "assets", "logo.jpg")

        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            dpr = self.devicePixelRatioF()
            scaled_pixmap = pixmap.scaledToHeight(
                int(22 * dpr), Qt.TransformationMode.SmoothTransformation
            )
            scaled_pixmap.setDevicePixelRatio(dpr)
            self.icon_label.setPixmap(scaled_pixmap)

        # Title — minimum width = natural text width, no wrapping
        self.title_label = QLabel("YourApp", self)
        self.title_label.setStyleSheet(
            "font-size: 15px; font-weight: bold; color: white; background: transparent; margin-left: 10px;"
        )
        self.title_label.setWordWrap(False)
        self.title_label.setSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred
        )

        self.layout.addWidget(self.icon_label)
        self.layout.addWidget(self.title_label)

    def setSelected(self, selected: bool):
        pass

    def setCompacted(self, compacted: bool):
        pass


# ---------------------------------------------------------------------------
# MainWindow — the application shell
# ---------------------------------------------------------------------------

class MainWindow(FluentWindow):
    """Pre-configured FluentWindow with sidebar squeeze protection.

    Critical settings (DO NOT REMOVE without understanding the consequences):

    1. setMinimumSize(900, 650)
       Prevents the window from shrinking below a safe size where content
       would be unusable.

    2. navigationInterface.setExpandWidth(207)
       Sidebar width in expanded mode. Adjust to fit your branding text.

    3. navigationInterface.panel.setMinimumExpandWidth(800)
       *** THIS IS THE KEY FIX ***
       NavigationPanel has TWO independent collapse thresholds:
         - expand() method:   minimumExpandWidth + expandWidth - 322
         - eventFilter(Resize): minimumExpandWidth directly (default 1008!)
       The Resize handler fires on every window resize. Without this fix,
       any window width < 1008px triggers automatic sidebar collapse.
       Setting minimumExpandWidth below our setMinimumSize(900) prevents
       the auto-collapse entirely.

    4. menuButton removal
       Prevents users from manually toggling the sidebar into compact mode.

    5. Title bar icon/label hidden
       The BrandingWidget already shows logo + title — avoid duplication.
    """

    def __init__(self):
        super().__init__()

        # ---- Theme ----
        setTheme(Theme.DARK)
        qconfig.set(qconfig.themeMode, Theme.DARK)

        # ---- Window geometry ----
        self.setWindowTitle("YourApp")
        self.setWindowIcon(QIcon(os.path.join(data_dir, "assets", "logo.ico")))
        self.resize(1000, 650)
        self.setMinimumSize(900, 650)

        # ---- Navigation sidebar ----
        self.navigationInterface.setReturnButtonVisible(False)
        self.navigationInterface.setExpandWidth(207)

        # ---- Hide default title bar decorations ----
        if hasattr(self.titleBar, 'titleLabel'):
            self.titleBar.titleLabel.hide()
        if hasattr(self.titleBar, 'iconLabel'):
            self.titleBar.iconLabel.hide()

        # ---- Remove menu button (prevent manual collapse) ----
        try:
            nav_panel = self.navigationInterface.panel
            nav_panel.vBoxLayout.removeWidget(nav_panel.menuButton)
            nav_panel.menuButton.hide()
            nav_panel.menuButton.setParent(None)
        except Exception:
            pass

        # ---- Prevent auto-collapse on window resize ----
        self.navigationInterface.panel.setMinimumExpandWidth(800)

        # ---- Branding widget (logo + title in sidebar) ----
        self.branding_widget = BrandingWidget(self)
        self.navigationInterface.addWidget(
            routeKey='branding',
            widget=self.branding_widget,
            onClick=None,
            position=NavigationItemPosition.TOP
        )

        # ---- Create interface instances ----
        self.home_interface = HomeInterface(self)
        self.settings_interface = SettingsInterface(self)
        self.about_interface = AboutInterface(self)

        # ---- Register navigation routes ----
        self.addSubInterface(self.home_interface, FIF.HOME, i18n.tr("tab_home"))
        self.addSubInterface(
            self.settings_interface, FIF.SETTING, i18n.tr("tab_settings"),
            position=NavigationItemPosition.BOTTOM
        )
        self.addSubInterface(
            self.about_interface, FIF.HELP, i18n.tr("tab_about"),
            position=NavigationItemPosition.BOTTOM
        )

        # ---- Expand sidebar (must be last) ----
        self.navigationInterface.expand()


# ---------------------------------------------------------------------------
# Entry point (use main.py instead for production)
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    import ctypes

    try:
        appid = 'yourcompany.yourapp.v1'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)
    except Exception:
        pass

    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(data_dir, "assets", "logo.ico")))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
