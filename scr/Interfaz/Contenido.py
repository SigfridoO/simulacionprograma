import os
import platform
import time
import threading
import sys
from pathlib import Path

from PyQt6.QtCore import Qt, QPropertyAnimation, QSize, QPoint
from PyQt6.QtGui import QPaintEvent, QPainter, QPixmap
from PyQt6.QtWidgets import QMdiSubWindow, QWidget, QPushButton, QStyleOption, QStyle, QTabWidget, QLabel, QVBoxLayout

from blessed import Terminal

ruta = Path(__file__).resolve().parent.parent
sys.path.append(str(ruta))

term = Terminal()


class WidgetContent(QWidget):
    def __init__(self, mdi):
        super().__init__()
        self.subventana = None
        self.caja0 = None
        self.widget = None
        self.animationLeftSidebar = None
        self.animationRightSidebar = None
        self.mdi = mdi
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        # self.menuBtn = QPushButton("Menu")
        # self.menuBtn.clicked.connect(self.showLeftSidebar)
        # self.layout.addWidget(self.menuBtn)

        self.tabs = self.crearPestanias()
        self.layout.addWidget(self.tabs)

    def showLeftSidebar(self):
        self.animationLeftSidebar = QPropertyAnimation(self.mdi.leftSidebar, b"size")
        self.animationLeftSidebar.setDuration(150)
        self.animationLeftSidebar.setStartValue(QSize(0, self.mdi.height()))
        self.animationLeftSidebar.setEndValue(QSize(270, self.mdi.height()))
        self.animationLeftSidebar.start()

        self.mdi.overlay.show()
        self.mdi.leftSidebar.show()

        self.mdi.setActiveSubWindow(self.mdi.overlay)
        self.mdi.setActiveSubWindow(self.mdi.leftSidebar)

    def showRightSidebar(self):
        self.animationRightSidebar = QPropertyAnimation(self.mdi.rightSidebar, b"pos")
        self.animationRightSidebar.setDuration(150)
        self.animationRightSidebar.setEndValue(QPoint(self.width() - self.mdi.rightSidebar.width(), 0))
        self.animationRightSidebar.setStartValue(QPoint(self.width(), 0))
        self.animationRightSidebar.start()

        self.mdi.overlay.show()
        self.mdi.rightSidebar.show()

        self.mdi.setActiveSubWindow(self.mdi.overlay)
        self.mdi.setActiveSubWindow(self.mdi.rightSidebar)

    def hideRightSidebar(self):
        self.animationRightSidebar = QPropertyAnimation(self.mdi.rightSidebar, b"pos")
        self.animationRightSidebar.setDuration(150)
        self.animationRightSidebar.setStartValue(QPoint(self.width() - self.mdi.rightSidebar.width(), 0))
        self.animationRightSidebar.setEndValue(QPoint(self.width(), 0))
        self.animationRightSidebar.start()
        self.animationRightSidebar.finished.connect(self.animationEnd)

    def hideLeftSidebar(self):
        self.animationLeftSidebar = QPropertyAnimation(self.mdi.leftSidebar, b"size")
        self.animationLeftSidebar.setDuration(150)
        self.animationLeftSidebar.setStartValue(QSize(270, self.mdi.height()))
        self.animationLeftSidebar.setEndValue(QSize(0, self.mdi.height()))
        self.animationLeftSidebar.start()
        self.animationLeftSidebar.finished.connect(self.animationEnd)

    def animationEnd(self):
        self.mdi.leftSidebar.hide()
        self.mdi.rightSidebar.hide()

    def crearPestanias(self) -> QWidget:
        tabs = QTabWidget()

        widget = QWidget()
        self.widget = widget

        etiqueta = QLabel('Soy una etiqueta')
        etiqueta.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        imagen = QPixmap()
        imagen.load("Imagenes/Boing747_2.jpeg")

        etiqueta.setPixmap(imagen)
        etiqueta.setScaledContents(True)

        cuadricula2 = QVBoxLayout()
        cuadricula2.addWidget(etiqueta)
        fondoAvion = QWidget()
        fondoAvion.setLayout(cuadricula2)


        tabs.setTabPosition(QTabWidget.TabPosition.East)
        tabs.setMovable(True)
        return tabs

    def paintEvent(self, event: QPaintEvent) -> None:
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, p, self)


class Contenido(QMdiSubWindow):
    def __init__(self, parent):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.widget = WidgetContent(parent)
        self.setWidget(self.widget)
