from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    Text,
)

from fastapi_erp.database import Base


class UtiIp(Base):

    __tablename__ = "uti_ip"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )

    category = Column(String(145))
    code = Column(String(145), nullable=False)
    name = Column(String(145))

    people_id = Column(Integer)
    dependency_id = Column(Integer)

    position = Column(String(145))
    active = Column(Boolean, nullable=False, default=False)

    antivirus = Column(String(145))
    restriction = Column(String(145))

    remote_server = Column(String(255))
    remote_pass = Column(String(255))
    remote_code = Column(String(255))

    description = Column(Text)

    mac_id = Column(String(145))
    workgroup = Column(String(145))
    device = Column(String(145))

    patrimonial_code = Column(String(145))

    creation = Column(DateTime)
    updated = Column(DateTime)


    stabilizer = Column(Boolean, nullable=False, default=False)
    stabilizer_code = Column(String(145))
    stabilizer_description = Column(String(145))



    printer = Column(Boolean, nullable=False, default=False)
    printer_code = Column(String(145))
    printer_description = Column(String(145))
    printer_serie = Column(String(145))
    printer_model = Column(String(145))





    canceled = Column(Boolean, nullable=False, default=False)

    user = Column(Integer)

    type = Column(String(1))

    siaf = Column(String(255))
    user_siaf = Column(String(255))
    clave = Column(String(255))

    n3 = Column(Integer)
    n4 = Column(Integer)

    device_serie = Column(String(100))
    device_model = Column(String(100))

    maintenance_type = Column(String(1))
    maintenance_date = Column(DateTime)

    license_serie = Column(String(100))
    activation_code = Column(String(100))
    activation_date = Column(DateTime)

    ext = None