from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.equipamento import Equipamento
from repositories.equipamento_repository import EquipamentoRepository


class EquipamentoService:

    @staticmethod
    def criar(
        session: Session,
        numero_serie: str,
        nome_maquina: str,
        fabricante: str | None,
        modelo: str | None,
        tipo_aquisicao: str,
        fornecedor: str | None = None
    ) -> Equipamento:

        numero_serie = numero_serie.strip()
        nome_maquina = nome_maquina.strip()
        tipo_aquisicao = tipo_aquisicao.strip().upper()

        if fabricante:
            fabricante = fabricante.strip()

        if modelo:
            modelo = modelo.strip()

        if fornecedor:
            fornecedor = fornecedor.strip()

        if not numero_serie:
            raise ValueError(
                "O número de série é obrigatório."
            )

        if not nome_maquina:
            raise ValueError(
                "O nome da máquina é obrigatório."
            )

        if tipo_aquisicao not in ["PROPRIO", "ALUGADO"]:
            raise ValueError(
                "O tipo de aquisição deve ser PROPRIO ou ALUGADO."
            )

        if tipo_aquisicao == "ALUGADO" and not fornecedor:
            raise ValueError(
                "Equipamentos alugados precisam de um fornecedor."
            )

        if tipo_aquisicao == "PROPRIO":
            fornecedor = None

        try:
            equipamento = EquipamentoRepository.criar(
                session=session,
                numero_serie=numero_serie,
                nome_maquina=nome_maquina,
                fabricante=fabricante,
                modelo=modelo,
                tipo_aquisicao=tipo_aquisicao,
                fornecedor=fornecedor
            )

            return equipamento

        except IntegrityError:
            session.rollback()

            raise ValueError(
                "Já existe um equipamento com esse número de série."
            )

    @staticmethod
    def listar(session: Session) -> list[Equipamento]:
        return EquipamentoRepository.listar(session)