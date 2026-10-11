
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from models.equipamento import Equipamento


class DashboardService:

    @staticmethod
    def obter_resumo(session: Session) -> dict:

        consulta = select(
            func.count(Equipamento.id).label("total"),
            func.count(Equipamento.id).filter(
                Equipamento.status == "DISPONIVEL"
            ).label("disponiveis"),
            func.count(Equipamento.id).filter(
                Equipamento.status == "EM_USO"
            ).label("em_uso"),
            func.count(Equipamento.id).filter(
                Equipamento.status == "MANUTENCAO"
            ).label("manutencao"),
        ).where(Equipamento.ativo.is_(True))

        resultado = session.execute(consulta).one()

        return {
            "total": resultado.total,
            "disponiveis": resultado.disponiveis,
            "em_uso": resultado.em_uso,
            "manutencao": resultado.manutencao,
        }
