from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from fastapi_erp.database import Base
from fastapi_erp.model.base.dependency_type import DependencyType


class Dependency(Base):
    __tablename__ = "org_dependencia"

    id = Column(
        "id_dep",
        Integer,
        primary_key=True
    )

    name = Column(
        "nombre_dep",
        String(150),
        nullable=False
    )

    type_id = Column(
        "id_dep_tipo",
        Integer,
        ForeignKey("org_dependencia_tipo.id_dep_tipo"),
        nullable=False
    )

    type = relationship(
        DependencyType,
        lazy="joined"
    )