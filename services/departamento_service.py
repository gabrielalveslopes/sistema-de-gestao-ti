from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.departamento import Departamento
from repositories.departamento_repository import DepartamentoRepository


class DepartamentoService:

    @staticmethod
    def criar(session: Session, nome: str) -> Departamento:
        try:
            departamento = DepartamentoRepository.criar(
                session=session,
                nome=nome
            )

            return departamento

        except IntegrityError:
            session.rollback()

            raise ValueError(
                "Já existe um departamento com esse nome."
            )

    @staticmethod
    def listar(session: Session) -> list[Departamento]:
        return DepartamentoRepository.listar(session)