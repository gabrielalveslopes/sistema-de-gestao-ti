from sqlalchemy.orm import Session

from models.equipamento import Equipamento


class EquipamentoRepository:

    @staticmethod
    def criar(
        session: Session,
        numero_serie: str,
        nome_maquina: str,
        fabricante: str | None,
        modelo: str | None,
        tipo_aquisicao: str,
        fornecedor: str | None
    ) -> Equipamento:

        equipamento = Equipamento(
            numero_serie=numero_serie,
            nome_maquina=nome_maquina,
            fabricante=fabricante,
            modelo=modelo,
            tipo_aquisicao=tipo_aquisicao,
            fornecedor=fornecedor
        )

        session.add(equipamento)
        session.commit()
        session.refresh(equipamento)

        return equipamento

    @staticmethod
    def listar(session: Session) -> list[Equipamento]:
        return session.query(Equipamento).all()