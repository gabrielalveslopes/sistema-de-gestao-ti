from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


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