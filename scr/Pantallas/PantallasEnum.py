from enum import Enum

class PantallasEnum(Enum):
    P100_SIMULADOR = (0, 'Simulación', "Rutas de reparto", "Pantallas.PantallaReparto.PantallaReparto", "mostrar_reparto")
    # P101_CODIGO_BARRAS = (1, 'Diseño', "Generador de Código de Barras", "pantallas.PantallaBarras.PantallaBarras", "mostrar_barras")

    def __init__(self, id_pantalla, grupo_menu, descripcion, clase_pantalla, metodo):
        self.id_pantalla = id_pantalla
        self.grupo_menu = grupo_menu
        self.descripcion = descripcion
        self.clase_pantalla = clase_pantalla
        self.metodo = metodo