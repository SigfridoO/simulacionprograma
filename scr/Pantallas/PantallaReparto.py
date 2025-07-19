import sys
from enum import Enum
from pathlib import Path

import qtawesome as qta
from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QPropertyAnimation, QPoint, QSize
from PyQt6.QtGui import QPaintEvent, QPainter, QFont
from PyQt6.QtWidgets import QMdiSubWindow, QWidget, QStyleOption, QStyle, QPushButton,  \
    QHBoxLayout, QVBoxLayout, QGridLayout, QSpinBox, \
    QSizePolicy, QScrollArea, QLabel, QLineEdit, QFileDialog, QMessageBox, QTextEdit


from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from Utils.Caja import Caja

# from Reparto.Reparto import Reparto
from scr.Reparto.Reparto2 import Reparto2 as Reparto
from Interfaz.MdiArea import MdiArea
from random import randint

ruta = Path(__file__).resolve().parent
sys.path.extend([str(ruta), str(ruta.parent), str(ruta.parent.parent), str(ruta.parent.parent.parent)])

class MatplotlibCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)

class Contenido(QWidget):
    def __init__(self, mdi: 'MdiArea'):
        super(Contenido, self).__init__()
        self.mdi = mdi
        gridLayout = QGridLayout()
        self.setLayout(gridLayout)

        etiqueta_titulo = QLabel('Rutas de reparto')
        etiqueta_titulo.setFixedHeight(50)
        etiqueta_titulo.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        fuente = etiqueta_titulo.font()
        fuente.setPointSize(20)
        etiqueta_titulo.setFont(fuente)

        self.visualizador = MatplotlibCanvas(self, width=5, height=4, dpi=100)

        # --- Controles ---
        controles = QWidget()
        controles_layout = QVBoxLayout()
        controles.setLayout(controles_layout)

        # Etiqueta + QSpinBox horizontal
        destinos_layout = QHBoxLayout()
        label_destinos = QLabel("Número de destinos:")
        self.input_destinos = QSpinBox()
        self.input_destinos.setMinimum(1)
        self.input_destinos.setMaximum(20)
        self.input_destinos.setValue(4)
        destinos_layout.addWidget(label_destinos)
        destinos_layout.addWidget(self.input_destinos)

        # Botón
        boton_simular = QPushButton("Ejecutar simulación")
        boton_simular.clicked.connect(self.ejecutar_simulacion)

        # Área de resultados con scroll
        self.detalle_resultado = QTextEdit()
        self.detalle_resultado.setReadOnly(True)
        self.detalle_resultado.setStyleSheet("font-family: monospace; font-size: 10pt;")
        self.detalle_resultado.setMinimumHeight(120)

        # Agregar al layout de controles
        controles_layout.addLayout(destinos_layout)
        controles_layout.addWidget(boton_simular)
        controles_layout.addWidget(self.detalle_resultado)

        # Agregar al layout general
        gridLayout.addWidget(etiqueta_titulo, 0, 0, 1, 6)
        gridLayout.addWidget(controles, 1, 0, 1, 2)
        gridLayout.addWidget(self.visualizador, 1, 2, 4, 4)

        self.reparto = None

    def ejecutar_simulacion(self):
        num = self.input_destinos.value()
        semilla = randint(1, 99999)

        self.reparto = Reparto(num_destinos=num, semilla=semilla)
        self.reparto.generar_nodos()
        self.reparto.calcular_arbol_optimo()
        self.reparto.visualizar(self.visualizador.ax)
        self.visualizador.draw()

        detalle = f"Semilla utilizada: {semilla}\n"
        detalle += "Aristas seleccionadas en el árbol óptimo:\n"
        suma = 0.0
        for u, v, peso in self.reparto.aristas_optimas:
            detalle += f" - N{u} <-> N{v} : {peso:.2f}\n"
            suma += peso
        detalle += f"\nCosto total: {suma:.2f}"

        self.detalle_resultado.setText(detalle)

class PantallaReparto(QMdiSubWindow):
    def __init__(self, parent):
        super(PantallaReparto, self).__init__()
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.widget = Contenido(parent)
        self.setWidget(self.widget)

    # def cerrar(self):
    #     self.widget.cerrar()
    #

