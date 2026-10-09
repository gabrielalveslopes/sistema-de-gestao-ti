from sqlalchemy import select
from sqlalchemy.orm import Session

from models.funcionario import Funcionario
from models.equipamento import Equipamento
from models.movimentacao import Movimentacao


class MovimentacaoRepository:

    @staticmethod
    def buscar_funcionario(
        session: Session,
        funcionario_id: int
    ) -> Funcionario | None:

        return session.get(Funcionario, funcionario_id)

    @staticmethod
    def buscar_equipamento_para_atualizacao(
        session: Session,
        equipamento_id: int
    ) -> Equipamento | None:

        comando = (
            select(Equipamento)
            .where(Equipamento.id == equipamento_id)
            .with_for_update()
        )

        return session.scalar(comando)

    @staticmethod
    def buscar_equipamento(
        session: Session,
        equipamento_id: int
    ) -> Equipamento | None:

        return session.get(Equipamento, equipamento_id)

    

    @staticmethod
    def buscar_movimentacao_aberta(
        session: Session,
        equipamento_id: int
    ) -> Movimentacao | None:

        comando = select(Movimentacao).where(
            Movimentacao.equipamento_id == equipamento_id,
            Movimentacao.data_hora_devolucao.is_(None)
        )

        return session.scalar(comando)

    @staticmethod
    def criar_entrega(
        session: Session,
        funcionario_id: int,
        equipamento_id: int
    ) -> Movimentacao:

        movimentacao = Movimentacao(
            funcionario_id=funcionario_id,
            equipamento_id=equipamento_id
        )

        session.add(movimentacao)

        return movimentacao

    @staticmethod
    def listar_historico(
        session: Session,
        equipamento_id: int
    ) -> list[Movimentacao]:

        comando = (
            select(Movimentacao)
            .where(Movimentacao.equipamento_id == equipamento_id)
            .order_by(Movimentacao.data_hora_entrega.desc())
        )

        return list(session.scalars(comando).all())


    @staticmethod
    def listar_historico(
        session: Session,
        equipamento_id: int
    ) -> list[Movimentacao]:

        comando = (
            select(Movimentacao)
            .where(Movimentacao.equipamento_id == equipamento_id)
            .order_by(Movimentacao.data_hora_entrega.desc())
        )

        return list(session.scalars(comando).all())

    @staticmethod
    def listar_equipamentos_em_uso(
        session: Session
    ) -> list[Movimentacao]:

        comando = (
            select(Movimentacao)
            .where(Movimentacao.data_hora_devolucao.is_(None))
            .order_by(Movimentacao.data_hora_entrega.desc())
        )

        return list(session.scalars(comando).all())