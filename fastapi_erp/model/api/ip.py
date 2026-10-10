from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UtiIpBase(BaseModel):

    category: str | None = None
    code: str | None = None
    name: str | None = None

    people_id: int | None = None
    dependency_id: int | None = None

    position: str | None = None
    active: bool | None = None

    antivirus: str | None = None
    restriction: str | None = None

    remote_server: str | None = None
    remote_pass: str | None = None
    remote_code: str | None = None

    description: str | None = None

    mac_id: str | None = None
    workgroup: str | None = None
    device: str | None = None

    patrimonial_code: str | None = None

    stabilizer: bool | None = None
    stabilizer_code: str | None = None
    stabilizer_description: str | None = None

    printer: bool | None = None
    printer_code: str | None = None
    printer_description: str | None = None
    printer_serie: str | None = None
    printer_model: str | None = None

    canceled: bool | None = None

    user: int | None = None
    type: str | None = None

    siaf: str | None = None
    user_siaf: str | None = None
    clave: str | None = None

    n3: int | None = None
    n4: int | None = None

    device_serie: str | None = None
    device_model: str | None = None

    maintenance_type: str | None = None
    maintenance_date: datetime | None = None

    license_serie: str | None = None
    activation_code: str | None = None
    activation_date: datetime | None = None


class UtiIpCreate(UtiIpBase):
    pass


class UtiIpUpdate(UtiIpBase):
    pass


class UtiIp(UtiIpBase):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    creation: datetime | None = None
    updated: datetime | None = None