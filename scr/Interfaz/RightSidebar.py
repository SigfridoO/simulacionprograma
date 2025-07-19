from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPaintEvent, QColor
from PyQt6.QtWidgets import QMdiSubWindow, QWidget, QStyleOption, QStyle, QVBoxLayout, QTextEdit

from Utils.Fuentes import Fuente


class RightSidebarWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        text_edit = QTextEdit(self)
        font = Fuente.fuente_normal_10
        text_edit.setFont(font)

        self.document = text_edit.document()
        self.layout.addWidget(text_edit)

    def paintEvent(self, event: QPaintEvent) -> None:
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, p, self)


class RightSidebar(QMdiSubWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.widget = RightSidebarWidget()
        self.widget.setStyleSheet('background-color: white')
        self.setWidget(self.widget)

    def establecer_texto(self, texto: str) -> None:
        if self.widget:
            self.widget.document.setHtml(texto)
