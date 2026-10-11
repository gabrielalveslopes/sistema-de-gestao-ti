
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QPushButton,
    QMessageBox,
)

from config.database import SessionLocal
from services.dashboard_service import DashboardService


class DashboardPage(QWidget):

    def __init__(self):
        super().__init__()

        self.criar_interface()
        self.atualizar_dados()

    def criar_card(self, titulo: str, valor: QLabel) -> QFrame:
        card = QFrame()
        card.setObjectName("card")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        titulo_label = QLabel(titulo)
        titulo_label.setObjectName("cardTitulo")

        valor.setObjectName("cardValor")
        valor.setAlignment(Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(titulo_label)
        layout.addWidget(valor)

        return card

    def criar_interface(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(24)

        cabecalho = QHBoxLayout()

        titulo = QLabel("Dashboard")
        titulo.setObjectName("cabecalho")

        botao_atualizar = QPushButton("Atualizar dados")
        botao_atualizar.clicked.connect(self.atualizar_dados)

        cabecalho.addWidget(titulo)
        cabecalho.addStretch()
        cabecalho.addWidget(botao_atualizar)

        layout.addLayout(cabecalho)

        self.valor_total = QLabel("0")
        self.valor_disponiveis = QLabel("0")
        self.valor_em_uso = QLabel("0")
        self.valor_manutencao = QLabel("0")

        cards = QHBoxLayout()
        cards.setSpacing(15)

        cards.addWidget(
            self.criar_card("Total de equipamentos", self.valor_total)
        )

        cards.addWidget(
            self.criar_card("Disponíveis", self.valor_disponiveis)
        )

        cards.addWidget(
            self.criar_card("Em uso", self.valor_em_uso)
        )

        cards.addWidget(
            self.criar_card("Em manutenção", self.valor_manutencao)
        )

        layout.addLayout(cards)
        layout.addStretch()

        self.setStyleSheet("""
            QFrame#card {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 12px;
            }

            QLabel#cardTitulo {
                color: #94a3b8;
                font-size: 13px;
            }

            QLabel#cardValor {
                color: #f8fafc;
                font-size: 30px;
                font-weight: bold;
            }
        """)

    def atualizar_dados(self):
        session = SessionLocal()

        try:
            resumo = DashboardService.obter_resumo(session)

            self.valor_total.setText(str(resumo["total"]))
            self.valor_disponiveis.setText(
                str(resumo["disponiveis"])
            )
            self.valor_em_uso.setText(str(resumo["em_uso"]))
            self.valor_manutencao.setText(
                str(resumo["manutencao"])
            )

        except Exception as erro:
            QMessageBox.critical(
                self,
                "Erro ao carregar Dashboard",
                f"Não foi possível consultar o banco:\n{erro}"
            )

        finally:
            session.close()
