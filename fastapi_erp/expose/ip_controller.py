from typing import Any

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Response,
)

from fastapi_erp.business.ip_service import IpService
from fastapi_erp.cbv import cbv
from fastapi_erp.model.api.ip import (
    UtiIp,
    UtiIpCreate,
    UtiIpUpdate,
)


router = APIRouter(
    prefix="/ip",
    tags=["IP"],
)


@cbv(router)
class IpController:

    ip_service: IpService = Depends(IpService.instance)

    @router.post("", response_model=dict)
    async def create(self, entity: UtiIpCreate):
        return await self.ip_service.create(entity)

    @router.put("/{ip_id}", response_model=dict)
    async def update(
        self,
        ip_id: int,
        entity: UtiIpUpdate,
    ):
        result = await self.ip_service.update(
            ip_id,
            entity,
        )

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="IP not found",
            )

        return result

    @router.post("/disable", response_model=dict)
    async def disable(self, ids: list[int]):
        await self.ip_service.disable(ids)

        return {
            "message": "IP records disabled successfully"
        }

    @router.delete("/{ip_id}", response_model=dict)
    async def delete(self, ip_id: int):
        result = await self.ip_service.delete(ip_id)

        if not result:
            raise HTTPException(
                status_code=404,
                detail="IP not found",
            )

        return {
            "message": "IP deleted successfully"
        }

    @router.post("/{ip_id}/finish", response_model=dict)
    async def finish(self, ip_id: int):
        result = await self.ip_service.finish(ip_id)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="IP not found",
            )

        return {
            "message": "IP finished successfully"
        }

    @router.get("/prepare", response_model=UtiIp)
    async def prepare(self):
        return self.ip_service.prepare()

    @router.get("/category")
    async def category(self):
        categories = await self.ip_service.get_category_list()

        return [
            {
                "id": category,
                "name": category,
            }
            for category in categories
        ]

    @router.put("/limpiar/{ip_id}", response_model=dict)
    async def clean(self, ip_id: int):
        result = await self.ip_service.clean(ip_id)

        if not result:
            raise HTTPException(
                status_code=404,
                detail="IP not found",
            )

        return {
            "message": "IP cleaned successfully"
        }

    @router.get("/count")
    async def count(self):
        return str(await self.ip_service.count())

    @router.get("/{ip_id}", response_model=UtiIp)
    async def get(self, ip_id: int):
        result = await self.ip_service.get(ip_id)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="IP not found",
            )

        return result

    @router.get("/{skip}/{limit}")
    async def list(
        self,
        skip: int = 0,
        limit: int = 20,
        category: str | None = None,
        code: str | None = None,
        name: str | None = None,
        position: str | None = None,
        device: str | None = None,
        macId: str | None = None,
        filter: str | None = None,
        description: str | None = None,
        empty: str | None = None,
        siaf: str | None = None,
        patrimonialCode: str | None = None,
        userSiaf: str | None = None,
        SORTER: str | None = Query(default=None),
    ):
        params = {}

        if category is not None:
            params["category"] = category

        if code is not None:
            params["code"] = code

        if filter is not None:
            params["filter"] = filter

        if name is not None:
            params["name"] = name

        if macId is not None:
            params["macId"] = macId

        if patrimonialCode is not None:
            params["patrimonialCode"] = patrimonialCode

        if position is not None:
            params["position"] = position

        if device is not None:
            params["device"] = device

        if SORTER is not None:
            params["SORTER"] = SORTER

        if description is not None:
            params["description"] = description

        if siaf is not None:
            params["siaf"] = siaf

        if userSiaf is not None:
            params["userSiaf"] = userSiaf

        try:
            data = await self.ip_service.list(
                skip=skip,
                limit=limit,
                params=params,
            )

            return {
                **params,
                "data": data,
            }

        except Exception as exc:
            return {
                **params,
                "error": str(exc),
            }