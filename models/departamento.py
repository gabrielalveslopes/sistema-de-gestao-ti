from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

if TYPE_CHECKING:
    from models.funcionario import Funcionario


class Departamento(Base):
    __tablename__ = "departamento"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )

    funcionarios: Mapped[list["Funcionario"]] = relationship(
        back_populates="departamento"
    )