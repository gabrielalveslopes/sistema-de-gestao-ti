from sqlalchemy.orm import Session

from models.funcionario import Funcionario


class FuncionarioRepository:

    @staticmethod
    def criar(
        session: Session,
        nome: str,
        email_institucional: str,
        departamento_id: int
    ) -> Funcionario:

        funcionario = Funcionario(
            nome=nome,
            email_institucional=email_institucional,
            departamento_id=departamento_id
        )

        session.add(funcionario)
        session.commit()
        session.refresh(funcionario)

        return funcionario

    @staticmethod
    def listar(session: Session) -> list[Funcionario]:
        return session.query(Funcionario).all()