from fastapi_erp.utils.pydantic import to_pydantic
from fastapi_erp.model.base.ip import UtiIp

UtiIpCreate = to_pydantic(
    UtiIp,
    name="UtiIpCreate",
    optional={'id'},
)

UtiIpUpdate = to_pydantic(
    UtiIp,
    name="UtiIpUpdate",
)

UtiIpResponse = to_pydantic(
    UtiIp,
    name="UtiIpResponse",
    all_optional=True,
)