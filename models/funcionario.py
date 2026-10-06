from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

if TYPE_CHECKING:
    from models.departamento import Departamento


class Funcionario(Base):
    __tablename__ = "funcionario"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email_institucional: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True
    )

    departamento_id: Mapped[int] = mapped_column(
        ForeignKey("departamento.id"),
        nullable=False
    )

    ativo: Mapped[bool] = mapped_column(
        default=True,
        nullable=False
    )

    departamento: Mapped["Departamento"] = relationship(
        back_populates="funcionarios"
    )