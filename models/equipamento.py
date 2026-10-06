from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class Equipamento(Base):
    __tablename__ = "equipamento"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    numero_serie: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )

    nome_maquina: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    fabricante: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    modelo: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    tipo_aquisicao: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    fornecedor: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="DISPONIVEL"
    )

    ativo: Mapped[bool] = mapped_column(
        nullable=False,
        default=True
    )