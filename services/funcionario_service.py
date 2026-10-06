from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.funcionario import Funcionario
from repositories.departamento_repository import DepartamentoRepository
from repositories.funcionario_repository import FuncionarioRepository


class FuncionarioService:

    @staticmethod
    def criar(
        session: Session,
        nome: str,
        email_institucional: str,
        departamento_id: int
    ) -> Funcionario:

        departamentos = DepartamentoRepository.listar(session)

        departamento_existe = any(
            departamento.id == departamento_id
            for departamento in departamentos
        )

        if not departamento_existe:
            raise ValueError(
                "O departamento informado não existe."
            )

        try:
            funcionario = FuncionarioRepository.criar(
                session=session,
                nome=nome,
                email_institucional=email_institucional,
                departamento_id=departamento_id
            )

            return funcionario

        except IntegrityError:
            session.rollback()

            raise ValueError(
                "Já existe um funcionário com esse e-mail."
            )

    @staticmethod
    def listar(session: Session) -> list[Funcionario]:
        return FuncionarioRepository.listar(session)