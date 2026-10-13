from sqlalchemy import Column, Integer, String

from fastapi_erp.database import Base


class People(Base):
    __tablename__ = "drt_personanatural"

    id = Column(
        "id_dir",
        Integer,
        primary_key=True,
    )

    full_name = Column(
        "nombre_completo",
        String(255),
    )