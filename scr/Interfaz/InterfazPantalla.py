import os
import platform
import time
import threading
import sys
from pathlib import Path
from abc import abstractmethod

from PyQt6.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal as Signal
from PyQt6.QtGui import QFontDatabase, QCloseEvent, QIcon, QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout
from blessed import Terminal

ruta = Path(__file__).resolve().parent.parent
sys.path.append(str(ruta))

term = Terminal()

from Interfaz.MdiArea import MdiArea
from Pantallas.AcercaDe import AcercaDe
from Pantallas.PantallasEnum import PantallasEnum
from Utils.Sistema import abs_path


class WorkerSignals(QObject):
    luzRoja = Signal(bool)
    luzAmarilla = Signal(bool)
    luzVerde = Signal(bool)

    variableDigital = Signal(bool)
    variableAnalogica = Signal(str)


class Worker(QRunnable):

    def __init__(self):
        super().__init__()
        self.signals: WorkerSignals = WorkerSignals()

    def run(self):
        pass

    def senal_luz_roja(self, estado: bool = False):
        try:
            self.signals.luzRoja.emit(estado)
        except Exception as error:
            print(error)

    def senal_luz_amarilla(self, estado: bool = False):
        try:
            self.signals.luzAmarilla.emit(estado)
        except Exception as error:
            print(error)

    def senal_luz_verde(self, estado: bool = False):
        try:
            self.signals.luzVerde.emit(estado)
        except Exception as error:
            print(error)

    def actualizar_variable_digital(self, estado: bool = False):
        try:
            self.signals.variableDigital.emit(estado)
        except Exception as error:
            print(error)

    def actualizar_variable_analogica(self, valor: str = ''):
        try:
            self.signals.variableAnalogica.emit(valor)
        except Exception as error:
            print(error)


class Subventana(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.resize(240, 120)
        self.setWindowTitle("Subventana")
        etiqueta = QLabel("Soy una subventana_calefaccion")
        layout = QVBoxLayout()
        layout.addWidget(etiqueta)
        self.setLayout(layout)


class InterfazPantalla(QMainWindow):

    def __init__(self):
        super(InterfazPantalla, self).__init__()
        QFontDatabase.addApplicationFont(abs_path("Resources/fonts/Roboto-Black.ttf"))
        # self.setStyleSheet("background-color: #FFFFFF; color: #000000;")
        self.cargar_qss("Resources/qss/QDark.qss")
        # self.cargar_qss("InterfazPySide2/qss/Ubuntu.qss")
        # self.cargar_qss("InterfazPySide2/qss/ConsoleStyle.qss")
        self.mdi = MdiArea()
        self.setCentralWidget(self.mdi)

        self.resize(1100, 700)
        self.crear_menu()
        self.simulador = None


        # Todo: Para Trabajar con Hilos
        self.threadpool = QThreadPool()
        self.worker = Worker()
        # self.worker.signals.luzRoja.connect(self.actualizar_luz_roja)
        # self.worker.signals.luzAmarilla.connect(selimport platformf.actualizar_luz_amarilla)
        # self.worker.signals.luzVerde.connect(self.actualizar_luz_verde)
        # self.worker.signals.variableDigital.connect(self.actualizar_variable_digital)
        # self.worker.signals.variableAnalogica.connect(self.actualizar_variable_analogica)

        # Iniciamos el trabajador en la pool de hilos
        self.threadpool.start(self.worker)

        self.acercaDe = None

        self.setWindowIcon(QIcon(abs_path("Imagenes/avion_icono_01.png")))
        self.setWindowTitle("Simulación")

    def cargar_qss(self, archivo: str):
        path = abs_path(archivo)
        try:
            # print("intentando abrir", path)
            with open(path) as styles:
                self.setStyleSheet(styles.read())
        except:
            print("Error al abrir el archivo de estilos", path)

    def closeEvent(self, event: QCloseEvent) -> None:
        print('Se ha presionado el botón cerrar')
        # event.accept()
        # self.cerrarAplicacion()
        if self.simulador:
            self.simulador.detener()

    def obtener_worker(self):
        return self.worker

    def establecer_simulador(self, simulador=None):
        self.simulador = simulador
        self.simulador.establecer_worker(self)

    def crear_menu(self):
        # ------------- Menu Archivo

        menu = self.menuBar()
        menuArchivo = menu.addMenu('&Archivo')

        actionSalir = QAction("&Salir", self)
        actionSalir.setIcon(QIcon(abs_path("../Imagenes/exit.png")))
        actionSalir.setShortcut("Ctrl+Q")
        actionSalir.triggered.connect(self.close)
        self.actionSalir = actionSalir

        # menuArchivo.addAction('&Abrir')
        menuArchivo.addSeparator()
        menuArchivo.addAction(actionSalir)

        # ------------- Menús dinámicos desde PantallasEnum
        menus_por_grupo = {}

        for opcion in PantallasEnum:
            grupo = opcion.grupo_menu# if hasattr(opcion,'grupo_menu') else opcion.nombre
            if grupo not in menus_por_grupo:
                menus_por_grupo[grupo] = menu.addMenu(f"&{grupo}")

            texto_menu = opcion.descripcion
            accion = QAction(texto_menu, self)
            accion.setShortcut(f"Ctrl+{opcion.id_pantalla}")
            accion.triggered.connect(lambda _, opt=opcion: self.mostrar_ventana(opt))
            menus_por_grupo[grupo].addAction(accion)


        # ------------- Menu Ayuda
        menuAyuda = menu.addMenu('Ay&uda')

        actionInformacion = QAction('&Informacion', self)
        # actionInformacion.setIcon(QIcon(abs_path("../Imagenes/info.png")))
        actionInformacion.setShortcut('Ctrl+I')
        actionInformacion.triggered.connect(self.mostrar_info)
        actionInformacion.setStatusTip('Muestra información irrelevante')

        self.actionInformacion = actionInformacion

        menuAyuda.addAction(actionInformacion)


    def mostrar_info(self):
        if not self.acercaDe:
            self.acercaDe = AcercaDe()
        self.acercaDe.show()
        # QMessageBox.about(self, "Información", "Esto es informativo")

        # if (self.programa is not None):
        #     self.programa.cerrarPrograma()

    def mostrar_ventana(self, opcion):
        if self.mdi:
            self.mdi.mostrar_ventana(opcion)

    def mostrarResultados(self):
        if not self.subventana:
            self.subventana = Subventana()
        self.subventana.show()

    @abstractmethod
    def cerrarAplicacion(self):
        print('No se ha implementando el método')
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont(abs_path("res/fonts/Roboto-Black.ttf"))
    window = InterfazPantalla()
    window.show()
    sys.exit(app.exec())
