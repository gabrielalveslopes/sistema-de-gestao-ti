from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class Movimentacao(Base):
    __tablename__ = "movimentacao"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    funcionario_id: Mapped[int] = mapped_column(
        ForeignKey("funcionario.id"),
        nullable=False
    )

    equipamento_id: Mapped[int] = mapped_column(
        ForeignKey("equipamento.id"),
        nullable=False
    )

    data_hora_entrega: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    data_hora_devolucao: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    funcionario = relationship("Funcionario")

    equipamento = relationship("Equipamento")