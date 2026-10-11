
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QDialog,
    QDialogButtonBox,
    QMessageBox,
)

from config.database import SessionLocal
from services.equipamento_service import EquipamentoService


class CadastroEquipamentoDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Cadastrar equipamento")
        self.setMinimumWidth(440)

        layout = QVBoxLayout(self)
        formulario = QFormLayout()

        self.numero_serie = QLineEdit()
        self.nome_maquina = QLineEdit()
        self.fabricante = QLineEdit()
        self.modelo = QLineEdit()

        self.tipo_aquisicao = QComboBox()
        self.tipo_aquisicao.addItem("Próprio", "PROPRIO")
        self.tipo_aquisicao.addItem("Alugado", "ALUGADO")

        self.fornecedor = QLineEdit()
        self.fornecedor.setEnabled(False)

        self.tipo_aquisicao.currentIndexChanged.connect(
            self.atualizar_fornecedor
        )

        formulario.addRow("Número de série:", self.numero_serie)
        formulario.addRow("Nome da máquina:", self.nome_maquina)
        formulario.addRow("Fabricante:", self.fabricante)
        formulario.addRow("Modelo:", self.modelo)
        formulario.addRow("Tipo de aquisição:", self.tipo_aquisicao)
        formulario.addRow("Fornecedor:", self.fornecedor)

        layout.addLayout(formulario)

        botoes = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )

        botoes.button(
            QDialogButtonBox.StandardButton.Save
        ).setText("Salvar")

        botoes.button(
            QDialogButtonBox.StandardButton.Cancel
        ).setText("Cancelar")

        botoes.accepted.connect(self.salvar)
        botoes.rejected.connect(self.reject)

        layout.addWidget(botoes)

    def atualizar_fornecedor(self):
        alugado = self.tipo_aquisicao.currentData() == "ALUGADO"

        self.fornecedor.setEnabled(alugado)

        if not alugado:
            self.fornecedor.clear()

    def salvar(self):
        session = SessionLocal()

        try:
            EquipamentoService.criar(
                session=session,
                numero_serie=self.numero_serie.text(),
                nome_maquina=self.nome_maquina.text(),
                fabricante=self.fabricante.text() or None,
                modelo=self.modelo.text() or None,
                tipo_aquisicao=self.tipo_aquisicao.currentData(),
                fornecedor=self.fornecedor.text() or None,
            )

            QMessageBox.information(
                self,
                "Sucesso",
                "Equipamento cadastrado com sucesso!"
            )

            self.accept()

        except ValueError as erro:
            QMessageBox.warning(
                self,
                "Dados inválidos",
                str(erro)
            )

        except Exception as erro:
            session.rollback()
            QMessageBox.critical(
                self,
                "Erro",
                f"Não foi possível cadastrar o equipamento:\n{erro}"
            )

        finally:
            session.close()


class EquipamentosPage(QWidget):

    def __init__(self):
        super().__init__()

        self.equipamentos = []

        self.criar_interface()
        self.atualizar_tabela()

    def criar_interface(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        cabecalho = QHBoxLayout()

        titulo = QLabel("Equipamentos")
        titulo.setObjectName("cabecalho")

        botao_novo = QPushButton("+ Novo equipamento")
        botao_novo.clicked.connect(self.abrir_cadastro)

        cabecalho.addWidget(titulo)
        cabecalho.addStretch()
        cabecalho.addWidget(botao_novo)

        layout.addLayout(cabecalho)

        barra = QHBoxLayout()

        self.pesquisa = QLineEdit()
        self.pesquisa.setPlaceholderText(
            "Pesquisar por nome ou número de série..."
        )

        self.pesquisa.textChanged.connect(self.filtrar_tabela)

        botao_atualizar = QPushButton("Atualizar")
        botao_atualizar.clicked.connect(self.atualizar_tabela)

        barra.addWidget(self.pesquisa)
        barra.addWidget(botao_atualizar)

        layout.addLayout(barra)

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(7)

        self.tabela.setHorizontalHeaderLabels([
            "ID",
            "Número de série",
            "Nome da máquina",
            "Fabricante",
            "Modelo",
            "Aquisição",
            "Status",
        ])

        self.tabela.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.tabela.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.tabela.setAlternatingRowColors(True)

        self.tabela.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        layout.addWidget(self.tabela)

        self.setStyleSheet("""
            QLineEdit, QComboBox {
                background-color: #1e293b;
                border: 1px solid #475569;
                border-radius: 6px;
                padding: 9px;
                color: #f8fafc;
            }

            QTableWidget {
                background-color: #111827;
                alternate-background-color: #1e293b;
                color: #f8fafc;
                gridline-color: #334155;
                border: 1px solid #334155;
            }

            QHeaderView::section {
                background-color: #263449;
                color: #f8fafc;
                padding: 9px;
                border: none;
            }
        """)

    def atualizar_tabela(self):
        session = SessionLocal()

        try:
            equipamentos = EquipamentoService.listar(session)

            self.equipamentos = [
                {
                    "id": equipamento.id,
                    "numero_serie": equipamento.numero_serie,
                    "nome_maquina": equipamento.nome_maquina,
                    "fabricante": equipamento.fabricante or "-",
                    "modelo": equipamento.modelo or "-",
                    "tipo_aquisicao": equipamento.tipo_aquisicao,
                    "status": equipamento.status,
                }
                for equipamento in equipamentos
            ]

            self.filtrar_tabela()

        except Exception as erro:
            QMessageBox.critical(
                self,
                "Erro ao carregar equipamentos",
                str(erro)
            )

        finally:
            session.close()

    def filtrar_tabela(self):
        termo = self.pesquisa.text().strip().lower()

        filtrados = [
            equipamento
            for equipamento in self.equipamentos
            if termo in equipamento["nome_maquina"].lower()
            or termo in equipamento["numero_serie"].lower()
        ]

        self.tabela.setRowCount(len(filtrados))

        for linha, equipamento in enumerate(filtrados):
            valores = [
                equipamento["id"],
                equipamento["numero_serie"],
                equipamento["nome_maquina"],
                equipamento["fabricante"],
                equipamento["modelo"],
                equipamento["tipo_aquisicao"],
                equipamento["status"],
            ]

            for coluna, valor in enumerate(valores):
                item = QTableWidgetItem(str(valor))

                if coluna == 0:
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignCenter
                    )

                self.tabela.setItem(linha, coluna, item)

    def abrir_cadastro(self):
        dialogo = CadastroEquipamentoDialog(self)

        if dialogo.exec() == QDialog.DialogCode.Accepted:
            self.atualizar_tabela()
