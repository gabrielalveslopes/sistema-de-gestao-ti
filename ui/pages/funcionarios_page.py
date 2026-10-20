
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
from models.departamento import Departamento
from models.funcionario import Funcionario


class CadastroFuncionarioDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Cadastrar funcionário")
        self.setMinimumWidth(420)

        layout = QVBoxLayout(self)
        formulario = QFormLayout()

        self.nome = QLineEdit()
        self.email = QLineEdit()

        self.departamento = QComboBox()
        self.carregar_departamentos()

        formulario.addRow("Nome completo:", self.nome)
        formulario.addRow("E-mail institucional:", self.email)
        formulario.addRow("Departamento:", self.departamento)

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

    def carregar_departamentos(self):
        session = SessionLocal()

        try:
            departamentos = (
                session.query(Departamento)
                .order_by(Departamento.nome)
                .all()
            )

            for departamento in departamentos:
                self.departamento.addItem(
                    departamento.nome,
                    departamento.id,
                )

        except Exception as erro:
            QMessageBox.critical(
                self,
                "Erro",
                f"Não foi possível carregar os departamentos:\n{erro}",
            )

        finally:
            session.close()

    def salvar(self):
        nome = self.nome.text().strip()
        email = self.email.text().strip().lower()
        departamento_id = self.departamento.currentData()

        if not nome or not email:
            QMessageBox.warning(
                self,
                "Campos obrigatórios",
                "Preencha o nome e o e-mail institucional.",
            )
            return

        if "@" not in email or "." not in email.split("@")[-1]:
            QMessageBox.warning(
                self,
                "E-mail inválido",
                "Informe um e-mail válido.",
            )
            return

        if departamento_id is None:
            QMessageBox.warning(
                self,
                "Departamento obrigatório",
                "Cadastre um departamento antes de cadastrar funcionários.",
            )
            return

        session = SessionLocal()

        try:
            email_existente = (
                session.query(Funcionario)
                .filter(Funcionario.email_institucional == email)
                .first()
            )

            if email_existente:
                QMessageBox.warning(
                    self,
                    "E-mail duplicado",
                    "Já existe um funcionário com esse e-mail.",
                )
                return

            funcionario = Funcionario(
                nome=nome,
                email_institucional=email,
                departamento_id=departamento_id,
                ativo=True,
            )

            session.add(funcionario)
            session.commit()

            QMessageBox.information(
                self,
                "Sucesso",
                "Funcionário cadastrado com sucesso!",
            )

            self.accept()

        except Exception as erro:
            session.rollback()

            QMessageBox.critical(
                self,
                "Erro ao cadastrar",
                f"Não foi possível cadastrar o funcionário:\n{erro}",
            )

        finally:
            session.close()


class FuncionariosPage(QWidget):

    def __init__(self):
        super().__init__()

        self.funcionarios = []

        self.criar_interface()
        self.atualizar_tabela()

    def criar_interface(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        cabecalho = QHBoxLayout()

        titulo = QLabel("Funcionários")
        titulo.setObjectName("cabecalho")

        botao_novo = QPushButton("+ Novo funcionário")
        botao_novo.clicked.connect(self.abrir_cadastro)

        cabecalho.addWidget(titulo)
        cabecalho.addStretch()
        cabecalho.addWidget(botao_novo)

        layout.addLayout(cabecalho)

        barra = QHBoxLayout()

        self.pesquisa = QLineEdit()
        self.pesquisa.setPlaceholderText(
            "Pesquisar por nome ou e-mail..."
        )
        self.pesquisa.textChanged.connect(self.filtrar_tabela)

        botao_atualizar = QPushButton("Atualizar")
        botao_atualizar.clicked.connect(self.atualizar_tabela)

        barra.addWidget(self.pesquisa)
        barra.addWidget(botao_atualizar)

        layout.addLayout(barra)

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(5)
        self.tabela.setHorizontalHeaderLabels([
            "ID",
            "Nome",
            "E-mail institucional",
            "Departamento",
            "Situação",
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
            funcionarios = (
                session.query(Funcionario)
                .join(Departamento)
                .order_by(Funcionario.nome)
                .all()
            )

            self.funcionarios = [
                {
                    "id": funcionario.id,
                    "nome": funcionario.nome,
                    "email": funcionario.email_institucional,
                    "departamento": funcionario.departamento.nome,
                    "ativo": funcionario.ativo,
                }
                for funcionario in funcionarios
            ]

            self.filtrar_tabela()

        except Exception as erro:
            QMessageBox.critical(
                self,
                "Erro ao carregar funcionários",
                str(erro),
            )

        finally:
            session.close()

    def filtrar_tabela(self):
        termo = self.pesquisa.text().strip().lower()

        filtrados = [
            funcionario
            for funcionario in self.funcionarios
            if termo in funcionario["nome"].lower()
            or termo in funcionario["email"].lower()
        ]

        self.tabela.setRowCount(len(filtrados))

        for linha, funcionario in enumerate(filtrados):
            valores = [
                funcionario["id"],
                funcionario["nome"],
                funcionario["email"],
                funcionario["departamento"],
                "Ativo" if funcionario["ativo"] else "Inativo",
            ]

            for coluna, valor in enumerate(valores):
                item = QTableWidgetItem(str(valor))

                if coluna == 0:
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignCenter
                    )

                self.tabela.setItem(linha, coluna, item)

    def abrir_cadastro(self):
        dialogo = CadastroFuncionarioDialog(self)

        if dialogo.exec() == QDialog.DialogCode.Accepted:
            self.atualizar_tabela()
