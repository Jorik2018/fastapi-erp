from sqlalchemy import Column, Integer, String, Text

from fastapi_erp.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(
        Integer,
        primary_key=True,
    )

    title = Column(
        String(255),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )