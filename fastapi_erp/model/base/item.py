from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from fastapi_erp.database import Base

class Item(Base):

    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")

    def dict(self):
        return self.__dict__
