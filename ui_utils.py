import os
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QIcon, QPalette, QPixmap
from qfluentwidgets import isDarkTheme


if getattr(sys, "frozen", False):
    data_dir = sys._MEIPASS
else:
    data_dir = os.path.dirname(os.path.abspath(__file__))


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
    for name in ("logo.ico", "logo.png", "logo.jpg"):
        icon = QIcon(resource_path(os.path.join("assets", name)))
        if not icon.isNull():
            return icon
    return QIcon()


def theme_color(role):
    colors = {
        "text": ("#ffffff", "#111827"),
        "muted": ("#a0a0a0", "#5f6b7a"),
        "accent": ("#60cdff", "#007f87"),
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


def optional_pixmap(asset_name):
    if not asset_name:
        return QPixmap()
    return QPixmap(resource_path(os.path.join("assets", asset_name)))
