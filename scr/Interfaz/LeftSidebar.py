import os
import platform
import time
import threading
import sys
from typing import Union
from pathlib import Path

from PyQt6.QtCore import Qt, QAbstractListModel, QSize, QRect, QModelIndex, QPersistentModelIndex, QEvent
from PyQt6.QtGui import QPainter, QPaintEvent, QPixmap, QFont, QColor, QMouseEvent, QEnterEvent, QAction
from PyQt6.QtWidgets import QMdiSubWindow, QWidget, QGraphicsDropShadowEffect, QStyleOption, QStyle, QVBoxLayout, \
    QListView, QFrame, QStyledItemDelegate, QStyleOptionViewItem, QLabel

from blessed import Terminal

ruta = Path(__file__).resolve().parent.parent
sys.path.append(str(ruta))

term = Terminal()

from Utils.Caja import Caja
from Utils.Sistema import abs_path

class Delegate(QStyledItemDelegate):
    def __init__(self, height=None):
        super().__init__()
        self._height = height if height is not None else 45

    def paint(self, painter: QPainter, option: QStyleOptionViewItem,
              index: Union[QModelIndex, QPersistentModelIndex]) -> None:
        super().paint(painter, option, index)

        if option.state & QStyle.StateFlag.State_MouseOver:
            painter.fillRect(option.rect, QColor("#F1F1F1"))
        else:
            painter.fillRect(option.rect, Qt.GlobalColor.transparent)

        if option.state & QStyle.StateFlag.State_Selected:
            painter.fillRect(option.rect, QColor("#F1F1F1"))

        icon = QPixmap()
        icon.load(index.data()[1])
        icon = icon.scaled(30, 30, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)

        left = 24
        iconPos = QRect(int(left),
                        int(((self._height - icon.height()) / 2) + option.rect.y()),
                        int(icon.width()),
                        int(icon.height()))
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.drawPixmap(iconPos, icon)

        font = QFont("Roboto Black", 12)
        textPos = QRect(
            (left * 2) + icon.width(),
            option.rect.y(),
            option.rect.width(),
            option.rect.height())

        painter.setPen(Qt.GlobalColor.black)
        painter.drawText(textPos, Qt.AlignmentFlag.AlignVCenter, index.data()[0])

    def sizeHint(self, option: QStyleOptionViewItem, index: Union[QModelIndex, QPersistentModelIndex]) -> QSize:
        return QSize(0, self._height)


class Model(QAbstractListModel):
    def __init__(self, data=None):
        super().__init__()
        self._data = data if data is not None else [
            ("Archivo", "InterfazPySide2/res/img/icons/group.png"),
            ("Editar", "InterfazPySide2/res/img/icons/megaphone.png"),
            ("Simulaci\u00f3n", "InterfazPySide2/res/img/icons/contacts.png"),
            ("Ayuda", "InterfazPySide2/res/img/icons/calls.png")
        ]

    def rowCount(self, index: Union[QModelIndex, QPersistentModelIndex] = ...) -> int:
        return len(self._data)

    def data(self, index: Union[QModelIndex, QPersistentModelIndex], role: int = ...):
        if index.isValid() and role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()]


class LinkLabel(QLabel):
    def __init__(self, parent=None, leave=None, enter=None):
        super().__init__(parent)
        self.leave = leave or "color: rgba(0,0,0, 100%);"
        self.enter = enter or "color: rgba(0,0,0, 100%);"
        self.setStyleSheet(self.leave)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def enterEvent(self, event: QEnterEvent) -> None:
        self.setStyleSheet(f"{self.enter}: text-decoration: underline;")

    def leaveEvent(self, event: QEvent) -> None:
        self.setStyleSheet(f"{self.leave}: text-decoration: none;")


class ListView(QListView):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        if self.indexAt(e.pos()).row() >= 0:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)


class Profile(QWidget):
    def __init__(self, height=None):
        super().__init__()
        self.avatar = None
        self.username = None
        self.setFixedHeight(height or 120)

    def paintAvatar(self):
        image = QPixmap()
        image.load(abs_path("InterfazPySide2/res/img/icons/user.png"))
        image = image.scaled(54, 54, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)

        _margin = 16
        _marginText = 24

        self.avatar = QLabel(self)
        self.avatar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.avatar.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.avatar.setPixmap(image)
        self.avatar.move(self.rect().x() + _margin, self.rect().y() + _margin)

        self.username = QLabel(self)
        self.username.setStyleSheet("color: white;")
        self.username.setFont(QFont("Roboto Black", 12))
        self.username.setCursor(Qt.CursorShape.PointingHandCursor)
        self.username.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.username.setText("correo@correo.com")
        self.username.move(self.rect().x() + _marginText, self.height() - 50)

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)

        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        image = QPixmap()
        image.load(absPath("Imagenes/Boing747_2.jpeg"))
        image = image.scaled(self.width(), self.height(), Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
        p.drawPixmap(self.rect(), image)


class SideMenuWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        self.layout.addWidget(Caja('yellow'))
        self.layout.addWidget(Profile())
        self.layout.addWidget(Caja('green'))

        self.listView = ListView()
        self.listView.setFrameStyle(QFrame.Shape.NoFrame)
        self.listView.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.listView.setModel(Model())
        self.listView.setItemDelegate(Delegate())
        self.layout.addWidget(self.listView)

        self.labels = QWidget()
        self.labels.setFixedHeight(60)
        self.layout.addWidget(self.labels)

        _margins = 16

        self.appName = LinkLabel(self.labels, "color: rgba(0,0,0,60%);", "color: rgba(0,0,0,40%);")
        self.appName.setText("Detector de fallas app")
        self.appName.setFont(QFont("Roboto Black", 12))
        self.appName.move(self.labels.x() + _margins, self.labels.y())

        self.appVer = LinkLabel(self.labels, "color: rgba(0,0,0,60%);", "color: rgba(0,0,0,40%);")
        self.appVer.setText("1.0.0")
        self.appVer.setFont(QFont("Roboto Black", 11))
        self.appVer.move(self.labels.x() + _margins, self.labels.y() + _margins * 2)

        self.lbl = QLabel(self.labels)
        self.lbl.setText("-")
        self.lbl.setStyleSheet("color: rgba(0,0,0,30%)")
        self.lbl.setFont(QFont("Roboto Black", 11))
        self.lbl.move(self.labels.x() + _margins * 4, self.labels.y() + _margins * 2)

        self.appAbout = LinkLabel(self.labels, "color: rgba(0,0,0,60%);", "color: rgba(0,0,0,40%);")
        self.appAbout.setText("")
        self.appAbout.setFont(QFont("Roboto Black", 11))
        self.appAbout.move(self.labels.x() + _margins * 5, self.labels.y() + _margins * 2)

        actionAcerca = QAction("copiar", self)
        self.appAbout.addAction(actionAcerca)
        actionAcerca.triggered.connect(self.mostrarAcercaDe)

        self.setStyleSheet("background: white;")

    def mostrarAcercaDe(self):
        print('Mostrando acerca de')

    def paintEvent(self, event: QPaintEvent) -> None:
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, p, self)


class LeftSidebar(QMdiSubWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(50)
        self.setGraphicsEffect(self.shadow)

        self.widget = SideMenuWidget()
        self.setWidget(self.widget)
        self.hide()
