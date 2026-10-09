from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models.movimentacao import Movimentacao
from repositories.movimentacao_repository import MovimentacaoRepository


class MovimentacaoService:

    @staticmethod
    def registrar_entrega(
        session: Session,
        funcionario_id: int,
        equipamento_id: int
    ) -> int:

        try:
            funcionario = MovimentacaoRepository.buscar_funcionario(
                session=session,
                funcionario_id=funcionario_id
            )

            if funcionario is None:
                raise ValueError("Funcionário não encontrado.")

            if not funcionario.ativo:
                raise ValueError("Funcionário está inativo.")

            equipamento = (
                MovimentacaoRepository.buscar_equipamento_para_atualizacao(
                    session=session,
                    equipamento_id=equipamento_id
                )
            )

            if equipamento is None:
                raise ValueError("Equipamento não encontrado.")

            if not equipamento.ativo:
                raise ValueError("Equipamento está inativo.")

            if equipamento.status != "DISPONIVEL":
                raise ValueError(
                    "Equipamento não está disponível para entrega."
                )

            movimentacao_aberta = (
                MovimentacaoRepository.buscar_movimentacao_aberta(
                    session=session,
                    equipamento_id=equipamento_id
                )
            )

            if movimentacao_aberta is not None:
                raise ValueError(
                    "Este equipamento já possui uma movimentação aberta."
                )

            movimentacao = MovimentacaoRepository.criar_entrega(
                session=session,
                funcionario_id=funcionario_id,
                equipamento_id=equipamento_id
            )

            equipamento.status = "EM_USO"

            session.flush()
            session.refresh(movimentacao)
            session.commit()

            return movimentacao.id

        except (ValueError, SQLAlchemyError):
            session.rollback()
            raise

    @staticmethod
    def registrar_devolucao(
        session: Session,
        equipamento_id: int
    ) -> int:

        try:
            equipamento = (
                MovimentacaoRepository.buscar_equipamento_para_atualizacao(
                    session=session,
                    equipamento_id=equipamento_id
                )
            )

            if equipamento is None:
                raise ValueError("Equipamento não encontrado.")

            movimentacao = (
                MovimentacaoRepository.buscar_movimentacao_aberta(
                    session=session,
                    equipamento_id=equipamento_id
                )
            )

            if movimentacao is None:
                raise ValueError(
                    "Este equipamento não possui uma entrega aberta."
                )

            if equipamento.status != "EM_USO":
                raise ValueError(
                    "O status do equipamento não corresponde à movimentação."
                )

            movimentacao.data_hora_devolucao = session.scalar(
                select(func.now())
            )

            equipamento.status = "DISPONIVEL"

            movimentacao_id = movimentacao.id

            session.commit()

            return movimentacao_id

        except (ValueError, SQLAlchemyError):
            session.rollback()
            raise

    @staticmethod
    def consultar_historico(
        session: Session,
        equipamento_id: int
    ) -> list[dict]:

        equipamento = MovimentacaoRepository.buscar_equipamento(
            session=session,
            equipamento_id=equipamento_id
        )

        if equipamento is None:
            raise ValueError("Equipamento não encontrado.")

        movimentacoes = MovimentacaoRepository.listar_historico(
            session=session,
            equipamento_id=equipamento_id
        )

        historico = []

        for movimentacao in movimentacoes:
            funcionario = movimentacao.funcionario

            historico.append({
                "movimentacao_id": movimentacao.id,
                "equipamento": equipamento.nome_maquina,
                "funcionario": funcionario.nome,
                "departamento": funcionario.departamento.nome,
                "data_entrega": movimentacao.data_hora_entrega,
                "data_devolucao": movimentacao.data_hora_devolucao,
                "situacao": (
                    "EM_USO"
                    if movimentacao.data_hora_devolucao is None
                    else "DEVOLVIDO"
                )
            })

        return historico

    @staticmethod
    def consultar_responsaveis_atuais(
        session: Session
    ) -> list[dict]:

        from models.equipamento import Equipamento

        equipamentos = session.query(Equipamento).all()

        resultado = []

        for equipamento in equipamentos:

            movimentacao = (
                MovimentacaoRepository.buscar_movimentacao_aberta(
                    session=session,
                    equipamento_id=equipamento.id
                )
            )

            if movimentacao is not None:
                responsavel = movimentacao.funcionario.nome
                departamento = movimentacao.funcionario.departamento.nome
            else:
                responsavel = "Departamento de TI"
                departamento = "TI"

            resultado.append({
                "equipamento": equipamento.nome_maquina,
                "numero_serie": equipamento.numero_serie,
                "responsavel": responsavel,
                "departamento": departamento,
                "status": equipamento.status
            })

        return resultado