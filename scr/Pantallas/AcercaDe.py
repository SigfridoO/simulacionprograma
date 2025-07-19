__author__ = "Sigfrido"
__date__ = "17-jun-2024 18:00:00"

from abc import abstractmethod

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QPaintEvent, QFont
from PyQt6.QtWidgets import QWidget, QLabel


class AcercaDe(QWidget):

    def __init__(self):
        super(AcercaDe, self).__init__()
        self.resize(400, 300)
        self.setWindowTitle("Acerca de ...")

        self.etiqueta = QLabel(self)
        self.etiqueta.setText("")
        self.etiqueta.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.etiqueta.setFixedSize(520, 40)

        q_font = QFont("Roboto Light", 24)
        q_font.setStretch(QFont.SemiCondensed)
        self.etiqueta.setFont(q_font)
        self.etiqueta.move(200, 20)

    def paintEvent(self, event: QPaintEvent) -> None:
        super(AcercaDe, self).paintEvent(event)

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        self.establecerContenido(p)

        # p.restore()

    @classmethod
    @abstractmethod
    def establecerContenido(self, p: QPainter):
        pass

    def __str__(self):
        pass
