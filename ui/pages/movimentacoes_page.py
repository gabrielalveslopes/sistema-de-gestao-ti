
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
    QGroupBox,
    QFormLayout,
)

from config.database import SessionLocal
from models.funcionario import Funcionario
from models.equipamento import Equipamento
from services.movimentacao_service import MovimentacaoService


class MovimentacoesPage(QWidget):

    def __init__(self):
        super().__init__()

        self.criar_interface()
        self.carregar_dados()

    def criar_interface(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(18)

        titulo = QLabel("Movimentações")
        titulo.setObjectName("cabecalho")
        layout.addWidget(titulo)

        descricao = QLabel(
            "Registre entregas, devoluções e consulte os equipamentos em uso."
        )
        layout.addWidget(descricao)

        # Formulário de entrega
        grupo_entrega = QGroupBox("Registrar entrega")
        formulario = QFormLayout(grupo_entrega)

        self.combo_funcionario = QComboBox()
        self.combo_equipamento_entrega = QComboBox()

        formulario.addRow("Funcionário:", self.combo_funcionario)
        formulario.addRow("Equipamento disponível:", self.combo_equipamento_entrega)

        botao_entrega = QPushButton("Registrar entrega")
        botao_entrega.setCursor(Qt.CursorShape.PointingHandCursor)
        botao_entrega.clicked.connect(self.registrar_entrega)

        formulario.addRow(botao_entrega)
        layout.addWidget(grupo_entrega)

        # Formulário de devolução
        grupo_devolucao = QGroupBox("Registrar devolução")
        formulario_devolucao = QFormLayout(grupo_devolucao)

        self.combo_equipamento_devolucao = QComboBox()
        formulario_devolucao.addRow(
            "Equipamento em uso:",
            self.combo_equipamento_devolucao,
        )

        botao_devolucao = QPushButton("Registrar devolução")
        botao_devolucao.setCursor(Qt.CursorShape.PointingHandCursor)
        botao_devolucao.clicked.connect(self.registrar_devolucao)

        formulario_devolucao.addRow(botao_devolucao)
        layout.addWidget(grupo_devolucao)

        # Tabela de responsáveis atuais
        linha_titulo = QHBoxLayout()

        subtitulo = QLabel("Equipamentos e responsáveis atuais")
        subtitulo.setStyleSheet("font-size: 18px; font-weight: bold;")

        botao_atualizar = QPushButton("Atualizar")
        botao_atualizar.setCursor(Qt.CursorShape.PointingHandCursor)
        botao_atualizar.clicked.connect(self.carregar_dados)

        linha_titulo.addWidget(subtitulo)
        linha_titulo.addStretch()
        linha_titulo.addWidget(botao_atualizar)

        layout.addLayout(linha_titulo)

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(5)
        self.tabela.setHorizontalHeaderLabels([
            "Equipamento",
            "Nº de série",
            "Responsável",
            "Departamento",
            "Status",
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

    def carregar_dados(self):
        try:
            with SessionLocal() as session:
                funcionarios = (
                    session.query(Funcionario)
                    .filter(Funcionario.ativo.is_(True))
                    .order_by(Funcionario.nome)
                    .all()
                )

                equipamentos_disponiveis = (
                    session.query(Equipamento)
                    .filter(
                        Equipamento.ativo.is_(True),
                        Equipamento.status == "DISPONIVEL",
                    )
                    .order_by(Equipamento.nome_maquina)
                    .all()
                )

                equipamentos_em_uso = (
                    session.query(Equipamento)
                    .filter(
                        Equipamento.ativo.is_(True),
                        Equipamento.status == "EM_USO",
                    )
                    .order_by(Equipamento.nome_maquina)
                    .all()
                )

                responsaveis = (
                    MovimentacaoService.consultar_responsaveis_atuais(session)
                )

                self.combo_funcionario.clear()
                for funcionario in funcionarios:
                    self.combo_funcionario.addItem(
                        funcionario.nome,
                        funcionario.id,
                    )

                self.combo_equipamento_entrega.clear()
                for equipamento in equipamentos_disponiveis:
                    self.combo_equipamento_entrega.addItem(
                        f"{equipamento.nome_maquina} — {equipamento.numero_serie}",
                        equipamento.id,
                    )

                self.combo_equipamento_devolucao.clear()
                for equipamento in equipamentos_em_uso:
                    self.combo_equipamento_devolucao.addItem(
                        f"{equipamento.nome_maquina} — {equipamento.numero_serie}",
                        equipamento.id,
                    )

            self.tabela.setRowCount(len(responsaveis))

            for linha, item in enumerate(responsaveis):
                valores = [
                    item["equipamento"],
                    item["numero_serie"],
                    item["responsavel"],
                    item["departamento"],
                    item["status"],
                ]

                for coluna, valor in enumerate(valores):
                    celula = QTableWidgetItem(str(valor))
                    celula.setFlags(
                        celula.flags()
                        & ~Qt.ItemFlag.ItemIsEditable
                    )
                    self.tabela.setItem(linha, coluna, celula)

            self.tabela.resizeColumnsToContents()

        except Exception as erro:
            QMessageBox.critical(
                self,
                "Erro ao carregar movimentações",
                str(erro),
            )

    def registrar_entrega(self):
        funcionario_id = self.combo_funcionario.currentData()
        equipamento_id = self.combo_equipamento_entrega.currentData()

        if funcionario_id is None or equipamento_id is None:
            QMessageBox.warning(
                self,
                "Dados incompletos",
                "Cadastre um funcionário ativo e um equipamento disponível antes de registrar a entrega.",
            )
            return

        resposta = QMessageBox.question(
            self,
            "Confirmar entrega",
            "Deseja realmente entregar este equipamento ao funcionário selecionado?",
        )

        if resposta != QMessageBox.StandardButton.Yes:
            return

        try:
            with SessionLocal() as session:
                movimentacao_id = MovimentacaoService.registrar_entrega(
                    session=session,
                    funcionario_id=funcionario_id,
                    equipamento_id=equipamento_id,
                )

            QMessageBox.information(
                self,
                "Entrega registrada",
                f"Entrega registrada com sucesso. Movimentação nº {movimentacao_id}.",
            )

            self.carregar_dados()

        except Exception as erro:
            QMessageBox.critical(
                self,
                "Erro ao registrar entrega",
                str(erro),
            )

    def registrar_devolucao(self):
        equipamento_id = self.combo_equipamento_devolucao.currentData()

        if equipamento_id is None:
            QMessageBox.warning(
                self,
                "Nenhum equipamento",
                "Não há equipamentos em uso para devolver.",
            )
            return

        resposta = QMessageBox.question(
            self,
            "Confirmar devolução",
            "Deseja registrar a devolução do equipamento selecionado?",
        )

        if resposta != QMessageBox.StandardButton.Yes:
            return

        try:
            with SessionLocal() as session:
                movimentacao_id = MovimentacaoService.registrar_devolucao(
                    session=session,
                    equipamento_id=equipamento_id,
                )

            QMessageBox.information(
                self,
                "Devolução registrada",
                f"Devolução registrada com sucesso. Movimentação nº {movimentacao_id}.",
            )

            self.carregar_dados()

        except Exception as erro:
            QMessageBox.critical(
                self,
                "Erro ao registrar devolução",
                str(erro),
            )
