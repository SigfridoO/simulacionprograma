__author__ = "Sigfrido"
__date__ = "7-Jul-2025 21:10:00"

import os
import platform
import time
import threading
import sys
from pathlib import Path

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication
from blessed import Terminal

ruta = Path(__file__).resolve().parent.parent
sys.path.append(str(ruta))

term = Terminal()


from Interfaz.InterfazPantalla import InterfazPantalla
from Splash.Splash import SplashScreen

sistema = platform.system()
plataforma = platform.uname()

if sistema == "Windows":
    print("Estamos en windows")
elif sistema == "Linux":
    print("Estamos en linux")
    if plataforma.node == "raspberrypi":
        print("Es una rapsberry")


class Inicio(InterfazPantalla):
    def __init__(self):
        InterfazPantalla.__init__(self)


def main():
    app = QApplication(sys.argv)

    splash = SplashScreen()

    splash.show()

    def load_application():
        for i in range(101):
            QTimer.singleShot(i * 40, lambda value=i: splash.update_progress(value))
        QTimer.singleShot(4000, splash.close)
        QTimer.singleShot(4000, ventana.show)


    ventana = Inicio()
    load_application()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
