from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap


def abs_path(file):
    return str(Path(__file__).parent.parent.absolute() / file)

def escalarImagen(imagen: QPixmap, relacion_tamanio):
    esime_dimension_x = imagen.rect().width() * relacion_tamanio
    imagen = imagen.scaled(
        int(esime_dimension_x),
        int(imagen.rect().height() * relacion_tamanio),
        Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
    return imagen