
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("AssetFlow - Gestão de TI")
        self.resize(1100, 700)

        self.criar_interface()

    def criar_interface(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout_principal = QHBoxLayout(central)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        menu = QWidget()
        menu.setObjectName("menu")
        menu.setFixedWidth(230)

        layout_menu = QVBoxLayout(menu)
        layout_menu.setContentsMargins(16, 24, 16, 16)
        layout_menu.setSpacing(10)

        titulo = QLabel("AssetFlow")
        titulo.setObjectName("titulo")
        layout_menu.addWidget(titulo)

        self.paginas = QStackedWidget()

        secoes = [
            "Dashboard",
            "Equipamentos",
            "Funcionários",
            "Movimentações",
            "Histórico",
        ]

        for indice, nome in enumerate(secoes):
            botao = QPushButton(nome)
            botao.setCursor(Qt.CursorShape.PointingHandCursor)

            botao.clicked.connect(
                lambda checked=False, i=indice: self.paginas.setCurrentIndex(i)
            )

            layout_menu.addWidget(botao)

            pagina = QWidget()
            layout_pagina = QVBoxLayout(pagina)

            cabecalho = QLabel(nome)
            cabecalho.setObjectName("cabecalho")

            descricao = QLabel(
                f"Área de {nome.lower()} do AssetFlow."
            )

            layout_pagina.addWidget(cabecalho)
            layout_pagina.addWidget(descricao)
            layout_pagina.addStretch()

            self.paginas.addWidget(pagina)

        layout_menu.addStretch()

        layout_principal.addWidget(menu)
        layout_principal.addWidget(self.paginas)

        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #10151f;
                color: #e5e7eb;
                font-family: Segoe UI;
                font-size: 14px;
            }

            QWidget#menu {
                background-color: #192230;
            }

            QLabel#titulo {
                font-size: 25px;
                font-weight: bold;
                color: #60a5fa;
                margin-bottom: 20px;
            }

            QLabel#cabecalho {
                font-size: 26px;
                font-weight: bold;
                margin: 20px;
            }

            QPushButton {
                background-color: #263449;
                border: none;
                border-radius: 7px;
                padding: 13px;
                text-align: left;
            }

            QPushButton:hover {
                background-color: #34537a;
            }
        """)
