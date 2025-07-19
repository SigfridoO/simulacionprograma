import sys

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QFont, QColor
from PyQt6.QtWidgets import QApplication, QSplashScreen, QLabel, QVBoxLayout, QMainWindow, QProgressBar

from Utils.Sistema import abs_path
from Utils.Sistema import escalarImagen

class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__()
        pixmap = QPixmap(abs_path("Imagenes/Avion01Splash.png"))
        pixmap = escalarImagen(pixmap, 0.8)
        self.setPixmap(pixmap)
        self.setWindowFlags(Qt.WindowType.SplashScreen | Qt.WindowType.FramelessWindowHint)

        self.label = QLabel(self)
        self.label.setText("Bienvenido")
        self.label.setFont(QFont("Arial", 20))
        self.label.setStyleSheet("color: black;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter)

        self.progressBar = QProgressBar(self)
        self.progressBar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)
        self.progressBar.setStyleSheet("QProgressBar {color: white;}")

        # self.mensaje2 = QLabel(self)
        # self.mensaje2.setText("Cargando la aplicación...")
        # self.mensaje2.setFont(QFont("Arial", 20))
        # self.mensaje2.setStyleSheet("color: black;")
        # self.mensaje2.setAlignment(Qt.AlignBottom | Qt.AlignCenter)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.progressBar)
        # self.layout.addWidget(self.mensaje2)
        self.layout.setContentsMargins(30, 10, 30, 50)
        self.showMessage("Cargando la aplicación...", Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter)

    def update_progress(self, value):
        self.progressBar.setValue(value)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Application")
        self.setGeometry(100, 100, 800, 600)


def main():
    app = QApplication(sys.argv)

    splash = SplashScreen()
    splash.show()

    def load_application():
        for i in range(101):
            QTimer.singleShot(i * 40, lambda value=i: splash.update_progress(value))
        QTimer.singleShot(4000, splash.close)
        QTimer.singleShot(4000, main_window.show)

    main_window = MainWindow()

    load_application()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
