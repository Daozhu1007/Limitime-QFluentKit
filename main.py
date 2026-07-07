import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from app_config import APP_USER_MODEL_ID
from ui_utils import load_app_icon
from ui_main import MainWindow


if __name__ == "__main__":
    try:
        import ctypes

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_USER_MODEL_ID)
    except Exception:
        pass

    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    app.setWindowIcon(load_app_icon())

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
