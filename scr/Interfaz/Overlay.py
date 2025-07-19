from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QMdiSubWindow

from Interfaz.Contenido import Contenido


class Overlay(QMdiSubWindow):
    def __init__(self, parent):
        super(Overlay, self).__init__()
        self.contenido: Contenido = None
        self.animationLeftSidebar = None
        self.animationRightSidebar = None
        self.parent = parent
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)

        self.setStyleSheet("background: rgba(0,0,0,15%);")
        self.hide()

    def mousePressEvent(self, mouseEvent: QMouseEvent) -> None:
        if self.contenido:
            self.contenido.widget.hideLeftSidebar()
            self.contenido.widget.hideRightSidebar()

        self.hide()

    def establecerPantallaContenido(self, contenido: Contenido):
        self.contenido = contenido
