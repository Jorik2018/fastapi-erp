from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from fastapi_erp.database import Base


class Item(Base):

    __tablename__ = "items"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    title = Column(
        String(255),
        index=True,
    )

    description = Column(
        Text,
    )

    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
    )

    owner = relationship(
        "User",
        back_populates="items",
    )