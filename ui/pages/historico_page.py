
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
)

from config.database import SessionLocal
from models.equipamento import Equipamento
from services.movimentacao_service import MovimentacaoService


class HistoricoPage(QWidget):

    def __init__(self):
        super().__init__()
        self.criar_interface()
        self.carregar_equipamentos()
        self.carregar_historico()

    def criar_interface(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        titulo = QLabel("Histórico de movimentações")
        titulo.setObjectName("cabecalho")
        layout.addWidget(titulo)

        descricao = QLabel(
            "Consulte as entregas e devoluções registradas no sistema."
        )
        layout.addWidget(descricao)

        filtros = QHBoxLayout()

        self.combo_equipamento = QComboBox()
        self.combo_equipamento.setMinimumWidth(280)
        self.combo_equipamento.currentIndexChanged.connect(
            self.carregar_historico
        )

        botao_atualizar = QPushButton("Atualizar")
        botao_atualizar.setCursor(Qt.CursorShape.PointingHandCursor)
        botao_atualizar.clicked.connect(self.carregar_historico)

        filtros.addWidget(QLabel("Equipamento:"))
        filtros.addWidget(self.combo_equipamento)
        filtros.addWidget(botao_atualizar)
        filtros.addStretch()

        layout.addLayout(filtros)

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(6)
        self.tabela.setHorizontalHeaderLabels([
            "ID",
            "Equipamento",
            "Funcionário",
            "Departamento",
            "Entrega",
            "Devolução",
        ])

        self.tabela.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.tabela.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.tabela.setAlternatingRowColors(True)
        self.tabela.horizontalHeader().setStretchLastSection(True)

        layout.addWidget(self.tabela)

        self.resumo = QLabel("Selecione um equipamento para consultar.")
        layout.addWidget(self.resumo)

    def carregar_equipamentos(self):
        try:
            with SessionLocal() as session:
                equipamentos = (
                    session.query(Equipamento)
                    .order_by(Equipamento.nome_maquina)
                    .all()
                )

                self.combo_equipamento.blockSignals(True)
                self.combo_equipamento.clear()
                self.combo_equipamento.addItem("Todos os equipamentos", None)

                for equipamento in equipamentos:
                    texto = (
                        f"{equipamento.nome_maquina} "
                        f"— {equipamento.numero_serie}"
                    )
                    self.combo_equipamento.addItem(
                        texto,
                        equipamento.id,
                    )

                self.combo_equipamento.blockSignals(False)

        except Exception as erro:
            self.combo_equipamento.blockSignals(False)
            QMessageBox.critical(
                self,
                "Erro ao carregar equipamentos",
                str(erro),
            )

    @staticmethod
    def formatar_data(data):
        if data is None:
            return "—"

        return data.strftime("%d/%m/%Y %H:%M")

    def carregar_historico(self, *_):
        equipamento_id = self.combo_equipamento.currentData()

        try:
            with SessionLocal() as session:
                if equipamento_id is not None:
                    historico = MovimentacaoService.consultar_historico(
                        session=session,
                        equipamento_id=equipamento_id,
                    )
                else:
                    equipamentos = (
                        session.query(Equipamento)
                        .order_by(Equipamento.nome_maquina)
                        .all()
                    )

                    historico = []

                    for equipamento in equipamentos:
                        historico.extend(
                            MovimentacaoService.consultar_historico(
                                session=session,
                                equipamento_id=equipamento.id,
                            )
                        )

            # Mais recentes primeiro
            historico.sort(
                key=lambda item: item["data_entrega"],
                reverse=True,
            )

            self.tabela.setRowCount(len(historico))

            abertas = 0

            for linha, item in enumerate(historico):
                data_devolucao = item["data_devolucao"]

                if data_devolucao is None:
                    abertas += 1

                valores = [
                    item["movimentacao_id"],
                    item["equipamento"],
                    item["funcionario"],
                    item["departamento"],
                    self.formatar_data(item["data_entrega"]),
                    self.formatar_data(data_devolucao),
                ]

                for coluna, valor in enumerate(valores):
                    celula = QTableWidgetItem(str(valor))
                    celula.setFlags(
                        celula.flags()
                        & ~Qt.ItemFlag.ItemIsEditable
                    )
                    self.tabela.setItem(linha, coluna, celula)

            self.tabela.resizeColumnsToContents()

            self.resumo.setText(
                f"Total de movimentações: {len(historico)} | "
                f"Em aberto: {abertas} | "
                f"Finalizadas: {len(historico) - abertas}"
            )

        except Exception as erro:
            QMessageBox.critical(
                self,
                "Erro ao carregar histórico",
                str(erro),
            )
