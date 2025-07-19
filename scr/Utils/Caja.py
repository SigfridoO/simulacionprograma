from PyQt6.QtWidgets import QLabel

class Caja(QLabel):
    def __init__(self, color):
        super().__init__()
        self.setStyleSheet(f'background-color: {color}')