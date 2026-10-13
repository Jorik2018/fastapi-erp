from sqlalchemy import Column, Integer, String

from fastapi_erp.database import Base


class DependencyType(Base):
    __tablename__ = "org_dep_tipo"

    id = Column(
        "id_dep_tipo",
        Integer,
        primary_key=True,
    )

    name = Column(
        "nombre",
        String(255),
    )