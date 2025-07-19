__author__ = "Sigfrido"
__date__ = "17-jun-2024 18:00:00"

import sys
from enum import Enum
from pathlib import Path

import qtawesome as qta
from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QPropertyAnimation, QPoint, QSize
from PyQt6.QtGui import QPaintEvent, QPainter, QFont
from PyQt6.QtWidgets import QMdiSubWindow, QWidget, QStyleOption, QStyle, QPushButton, QGridLayout, QHBoxLayout, \
    QSizePolicy, QVBoxLayout, QScrollArea, QLabel

from Utils.Caja import Caja
from Interfaz.RightSidebar import RightSidebarWidget

ruta = Path(__file__).resolve().parent
sys.path.extend([str(ruta), str(ruta.parent), str(ruta.parent.parent), str(ruta.parent.parent.parent)])


class Contenido(QWidget):

    def __init__(self, mdi):
        super(Contenido, self).__init__()

        self.scroll_area = None
        self.layout_barra_botones = None
        self.layout_conexiones_establecidas = None
        self.panel_conexiones_establecidas = None
        self.mdi = mdi

        # Contenido de la ventana
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        # Elementos gráficos de la interfaz
        self.panel_camara_propia = None
        self.panel_camara_remota = None
        self.boton_hamburgesa: QPushButton = None
        self.boton_llamar: QPushButton = None
        self.boton_colgar: QPushButton = None
        self.boton_silenciar: QPushButton = None
        self.boton_contestar: QPushButton = None

        self.panelInformacion = None
        self.etiquetaLlamadaEntrante = None

        # Referencia para la clase principal
        self.sidebar: RightSidebarWidget = None
        self.animation_rightsidebar = None
        self.animation_leftsidebar = None

        self.inicio = None

        # Creando la interfaz
        self.ventana_principal = self.crear_ventana_principal()
        self.layout.addWidget(self.ventana_principal)

        # Manejo de las tareas
        # self.threadPool = QThreadPool()
        #
        # self.tarea0 = VideoThread()
        # self.tarea0.change_pixmap_signal.connect(self.update_image)
        # self.tarea0.start()
        #
        # self.tarea1 = Worker()
        # self.tarea1.signals.llamadaEntrante.connect(self.mostrar_etiqueta_llamada_entrante)
        # self.threadPool.start(self.tarea1)

    def establecer_sidebar(self, sidebar):
        self.sidebar = sidebar

    def crear_ventana_principal(self) -> QWidget:
        ventana_principal = QWidget()

        cuadricula = QGridLayout()
        ventana_principal.setLayout(cuadricula)

        top_bar_layout = QHBoxLayout()

        self.boton_hamburgesa = QPushButton()
        self.boton_hamburgesa.setIcon(qta.icon('fa5s.bars'))
        self.boton_hamburgesa.setMaximumSize(40, 40)
        self.boton_hamburgesa.setFixedHeight(40)
        top_bar_layout.addWidget(self.boton_hamburgesa)

        self.panelInformacion = Caja('gray')
        self.panelInformacion.setMaximumHeight(40)
        self.panelInformacion.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        top_bar_layout.addWidget(self.panelInformacion)

        cuadricula.addLayout(top_bar_layout, 0, 0, 1, 4)
        self.panel_camara_remota = Caja('black')
        cuadricula.addWidget(self.panel_camara_remota, 2, 0, 3, 3)
        self.panel_camara_propia = Caja('black')
        #
        # self.panel_camara_propia.setMaximumSize(self.TAMANIO_PANEL_CAMARA_PROPIA_ANCHO,
        #                                         self.TAMANIO_PANEL_CAMARA_PROPIA_ALTO)
        cuadricula.addWidget(self.panel_camara_propia, 2, 3, 1, 1)

        # self.panel_conexiones_establecidas = Caja("#345678")
        self.panel_conexiones_establecidas = QWidget()
        self.layout_conexiones_establecidas = QVBoxLayout()
        self.layout_conexiones_establecidas.setContentsMargins(5, 5, 5, 5)
        self.panel_conexiones_establecidas.setLayout(self.layout_conexiones_establecidas)
        self.scroll_area = QScrollArea()

        self.scroll_area.setWidgetResizable(True)
        # self.scroll_area.setFixedWidth(self.TAMANIO_PANEL_CAMARA_PROPIA_ANCHO)
        self.scroll_area.setWidget(self.panel_conexiones_establecidas)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        cuadricula.addWidget(self.scroll_area, 3, 3, 2, 1)
        # barraBotones = QWidget()
        # barraBotones.setFixedHeight(55)
        # barraBotones.setStyleSheet("background-color:white")

        self.layout_barra_botones = QGridLayout()
        cuadricula.addLayout(self.layout_barra_botones, 5, 0, 1, 4)

        cuadricula3 = QGridLayout()
        cuadricula3.setContentsMargins(0, 0, 0, 0)
        self.panelInformacion.setLayout(cuadricula3)

        self.etiquetaLlamadaEntrante = QLabel('Llamada entrante')
        self.etiquetaLlamadaEntrante.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.etiquetaLlamadaEntrante.setStyleSheet(f'background-color: rgb(250, 64, 64)')

        self.etiquetaLlamadaEntrante.setHidden(True)
        cuadricula3.addWidget(self.etiquetaLlamadaEntrante, 0, 0, 1, 1)

        fuente1 = QFont("Helvetica")
        fuente1.setBold(True)
        fuente1.setCapitalization(QtGui.QFont.AllUppercase)

        # Agregando los nombres de las camaras
        cuadricula4 = QVBoxLayout()
        self.panel_camara_propia.setLayout(cuadricula4)
        etiqueta_nombre_propio = QLabel("Propia")
        etiqueta_nombre_propio.setStyleSheet(f'background-color: rgba(255, 0, 0, 0); color: black;')
        etiqueta_nombre_propio.setAlignment(Qt.AlignBottom | Qt.AlignLeft)
        etiqueta_nombre_propio.setFont(fuente1)
        cuadricula4.addStretch()
        cuadricula4.addWidget(etiqueta_nombre_propio)

        cuadricula5 = QVBoxLayout()
        self.panel_camara_remota.setLayout(cuadricula5)
        etiqueta_nombre_camara_remota = QLabel("Remota")
        etiqueta_nombre_camara_remota.setStyleSheet(f'background-color: rgba(255, 0, 0, 0); color: black;')
        etiqueta_nombre_camara_remota.setAlignment(Qt.AlignBottom | Qt.AlignLeft)
        etiqueta_nombre_camara_remota.setFont(fuente1)
        cuadricula5.addStretch()
        cuadricula5.addWidget(etiqueta_nombre_camara_remota)

        self.boton_hamburgesa.clicked.connect(self.show_right_sidebar)

        return ventana_principal

    def cerrar(self):
        pass

    def show_left_sidebar(self):
        print('Dentro de mostrar RightSidebar')
        self.animation_leftsidebar = QPropertyAnimation(self.mdi.left_sidebar, b"size")
        self.animation_leftsidebar.setDuration(150)
        self.animation_leftsidebar.setStartValue(QSize(0, self.mdi.height()))
        self.animation_leftsidebar.setEndValue(QSize(270, self.mdi.height()))
        self.animation_leftsidebar.start()

        self.mdi.overlay.show()
        self.mdi.left_sidebar.show()

        self.mdi.setActiveSubWindow(self.mdi.overlay)
        self.mdi.setActiveSubWindow(self.mdi.left_sidebar)

    def show_right_sidebar(self):
        print('Dentro de mostrar RightSidebar')
        self.animation_rightsidebar = QPropertyAnimation(self.mdi.right_sidebar, b"pos")
        self.animation_rightsidebar.setDuration(150)
        self.animation_rightsidebar.setEndValue(QPoint(self.width() - self.mdi.right_sidebar.width(), 0))
        self.animation_rightsidebar.setStartValue(QPoint(self.width(), 0))

        self.animation_rightsidebar.start()

        self.mdi.overlay.show()
        self.mdi.right_sidebar.show()

        self.mdi.setActiveSubWindow(self.mdi.overlay)
        self.mdi.setActiveSubWindow(self.mdi.right_sidebar)

    def hide_right_sidebar(self):
        self.animation_rightsidebar = QPropertyAnimation(self.mdi.right_sidebar, b"pos")
        self.animation_rightsidebar.setDuration(150)
        self.animation_rightsidebar.setStartValue(QPoint(self.width() - self.mdi.right_sidebar.width(), 0))
        self.animation_rightsidebar.setEndValue(QPoint(self.width(), 0))
        self.animation_rightsidebar.start()
        self.animation_rightsidebar.finished.connect(self.animation_end)

    def hide_left_sidebar(self):
        self.animation_leftsidebar = QPropertyAnimation(self.mdi.left_sidebar, b"size")
        self.animation_leftsidebar.setDuration(150)
        self.animation_leftsidebar.setStartValue(QSize(270, self.mdi.height()))
        self.animation_leftsidebar.setEndValue(QSize(0, self.mdi.height()))
        self.animation_leftsidebar.start()
        self.animation_leftsidebar.finished.connect(self.animation_end)

    def animation_end(self):
        self.mdi.left_sidebar.hide()
        self.mdi.left_sidebar.hide()

    def paintEvent(self, event: QPaintEvent) -> None:
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, p, self)


class PantallaPrincipal(QMdiSubWindow):
    def __init__(self, parent):
        super(PantallaPrincipal, self).__init__()
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.widget = Contenido(parent)
        self.setWidget(self.widget)

    def cerrar(self):
        self.widget.cerrar()
