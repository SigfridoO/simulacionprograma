import os
import platform
import time
import threading
import sys
from typing import Union
from pathlib import Path
import importlib
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import QMdiArea

from blessed import Terminal

ruta = Path(__file__).resolve().parent.parent
sys.path.append(str(ruta))

term = Terminal()

from Interfaz.Contenido import Contenido
from Interfaz.LeftSidebar import LeftSidebar
from Interfaz.Overlay import Overlay
from Interfaz.RightSidebar import RightSidebar


# from Pantallas.PantallaPrincipal import PantallaPrincipal
from Pantallas.PantallasEnum import PantallasEnum

class MdiArea(QMdiArea):
    def __init__(self):
        super(MdiArea, self).__init__()

        self.leftSidebar = LeftSidebar()
        self.rightSidebar = RightSidebar()
        self.contenido = Contenido(self)
        self.overlay = Overlay(self)

        self.overlay.establecerPantallaContenido(self.contenido)

        self.lista_de_pantallas = list()

        self.addSubWindow(self.leftSidebar)
        self.addSubWindow(self.rightSidebar)
        self.addSubWindow(self.contenido)
        self.addSubWindow(self.overlay)

        self.pantalla_activa = None

        self.agregar_listeners()

    def agregar_listeners(self):
        pass
        #self.pantalla_principal.widget.establecer_sidebar(self.right_sidebar.widget)

    def resizeEvent(self, resizeEvent: QResizeEvent) -> None:
        self.contenido.resize(self.width(), self.height())
        self.overlay.resize(self.width(), self.height())
        self.leftSidebar.resize(270, self.height())

        self.rightSidebar.resize(700, self.height())
        self.rightSidebar.move(self.width() - self.rightSidebar.width(), 0)


        if self.pantalla_activa is not None:
            self.pantalla_activa.resize(self.width(), self.height())

    def mostrar_ventana(self, seleccion: PantallasEnum):

        self.pantalla_activa = None

        for subventana in self.subWindowList():
            subventana.hide()

        nombre_enum = seleccion.name
        pantalla_existente = next((p for p in self.lista_de_pantallas if p.objectName() == nombre_enum), None)

        if pantalla_existente is None:
            try:
                modulo_nombre, clase_nombre = seleccion.clase_pantalla.rsplit(".", 1)
                modulo = importlib.import_module(f"{modulo_nombre}")
                # print(modulo, clase_nombre)
                print(f"Mostrando: {clase_nombre}")
                clase_pantalla = getattr(modulo, clase_nombre)
            except (ImportError, AttributeError) as e:
                print(f"[Error] No se pudo cargar '{seleccion.clase_pantalla}': {e}")
                return

            pantalla_existente = clase_pantalla(self)
            pantalla_existente.setObjectName(nombre_enum)

            self.lista_de_pantallas.append(pantalla_existente)
            self.addSubWindow(pantalla_existente)

        pantalla_existente.resize(self.width(), self.height())
        pantalla_existente.show()
        self.setActiveSubWindow(pantalla_existente)


        self.pantalla_activa = pantalla_existente


        # if hasattr(pantalla_existente, seleccion.metodo):
        #     getattr(pantalla_existente, seleccion.metodo)()
        # else:
        #     print(f"[Advertencia] La clase no contiene el método '{seleccion.metodo}'")



    def cerrar(self):
        self.pantalla_principal.cerrar()
