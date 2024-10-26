from sqlalchemy import String, VARCHAR, Integer
from sqlalchemy.orm import mapped_column, Mapped

from models.database import CreatedBaseModel


class Product(CreatedBaseModel):
    name: Mapped[str] = mapped_column(VARCHAR(255))
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    price: Mapped[int] = mapped_column(Integer)
    quantity: Mapped[int] = mapped_column(Integer, server_default="0")
