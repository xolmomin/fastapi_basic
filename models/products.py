from faker import Faker
from sqlalchemy import String, VARCHAR, Integer
from sqlalchemy.orm import mapped_column, Mapped

from models.database import CreatedBaseModel

fake = Faker()


class Product(CreatedBaseModel):
    name: Mapped[str] = mapped_column(VARCHAR(255))
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    price: Mapped[int] = mapped_column(Integer)
    quantity: Mapped[int] = mapped_column(Integer, server_default="0")

    @classmethod
    async def generate(cls, count: int = 1):
        for _ in range(count):
            await cls.create(
                name=fake.company(),
                description=fake.sentence(),
                price=fake.random_int(min=1, max=100),
                quantity=fake.random_int(min=0, max=50)
            )
