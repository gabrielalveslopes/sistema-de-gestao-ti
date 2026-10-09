from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from repositories.movimentacao_repository import MovimentacaoRepository


class MovimentacaoService:

    @staticmethod
    def registrar_entrega(
        session: Session,
        funcionario_id: int,
        equipamento_id: int
    ):

        try:
            funcionario = MovimentacaoRepository.buscar_funcionario(
                session=session,
                funcionario_id=funcionario_id
            )

            if funcionario is None:
                raise ValueError(
                    "Funcionário não encontrado."
                )

            if not funcionario.ativo:
                raise ValueError(
                    "Funcionário está inativo."
                )

            equipamento = (
                MovimentacaoRepository.buscar_equipamento_para_atualizacao(
                    session=session,
                    equipamento_id=equipamento_id
                )
            )

            if equipamento is None:
                raise ValueError(
                    "Equipamento não encontrado."
                )

            if not equipamento.ativo:
                raise ValueError(
                    "Equipamento está inativo."
                )

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