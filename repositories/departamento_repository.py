from sqlalchemy.orm import Session

from models.departamento import Departamento


class DepartamentoRepository:

    @staticmethod
    def criar(session: Session, nome: str) -> Departamento:
        departamento = Departamento(nome=nome)

        session.add(departamento)
        session.commit()
        session.refresh(departamento)

        return departamento

    @staticmethod
    def listar(session: Session) -> list[Departamento]:
        return session.query(Departamento).all()