from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)

from fastapi_erp.business.ip_service import IpService
from fastapi_erp.cbv import cbv

# Entidad SQLAlchemy
from fastapi_erp.model.base.ip import UtiIp

# DTOs Pydantic
from fastapi_erp.model.api.ip import (
    UtiIpCreate,
    UtiIpResponse,
    UtiIpUpdate,
)

# Mapper DTO -> Entity
from fastapi_erp.utils.mapper import ListResponse, to_entity


router = APIRouter(
    prefix="/ip",
    tags=["IP"],
)


@cbv(router)
class IpController:

    ip_service: IpService = Depends(IpService.instance)


    @router.get(
        "/{ip_id}",
        response_model=UtiIpResponse,
    )
    async def get(
        self,
        ip_id: int,
    ):
        result = await self.ip_service.get(ip_id)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="IP not found",
            )

        return result


    @router.get(
        "/prepare",
        response_model=UtiIpResponse,
    )
    async def prepare(self):
        return await self.ip_service.prepare()

    @router.post("", response_model=UtiIpResponse)
    async def create(
        self,
        dto: UtiIpCreate,
    ):
        return await self.ip_service.edit(
            to_entity(dto, UtiIp)
        )

    @router.put("/{ip_id}", response_model=UtiIpResponse)
    async def update(
        self,
        ip_id: int,
        entity: UtiIpUpdate,
    ):
        result = await self.ip_service.update(
            ip_id,
            entity.model_dump(exclude_unset=True),
        )

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="IP not found",
            )

        return result

    @router.post("/disable")
    async def disable(
        self,
        ids: list[int],
    ):
        self.ip_service.disable(ids)

        return {
            "message": "IP records disabled successfully"
        }

    @router.delete("/{ip_id}")
    async def delete(
        self,
        ip_id: int,
    ):
        result = await self.ip_service.delete(ip_id)

        if not result:
            raise HTTPException(
                status_code=404,
                detail="IP not found",
            )

        return {
            "message": "IP deleted successfully"
        }

    @router.post("/{ip_id}/finish")
    async def finish(
        self,
        ip_id: int,
    ):
        result = await self.ip_service.finish(ip_id)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="IP not found",
            )

        return {
            "message": "IP finished successfully"
        }

    @router.get("/category")
    async def category(self):

        categories = (
            await self.ip_service.get_category_list()
        )

        return [
            {
                "id": category,
                "name": category,
            }
            for category in categories
        ]

    @router.put("/clear/{id}")
    async def clean(
        self,
        id: int,
    ):
        result = await self.ip_service.clear(id)

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
        return await self.ip_service.count()

    # ---------------------------------------------------------
    # GET
    # ---------------------------------------------------------

    @router.get("/{skip}/{limit}",
                response_model=ListResponse[UtiIpResponse])
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
        dependency: str | None = None,
        SORTER: str | None = Query(default=None),
    ):
        params = {
            key: value
            for key, value in {
                "category": category,
                "code": code,
                "name": name,
                "position": position,
                "device": device,
                "macId": macId,
                "filter": filter,
                "description": description,
                "empty": empty,
                "siaf": siaf,
                "patrimonialCode": patrimonialCode,
                "userSiaf": userSiaf,
                "dependency": dependency,
                "SORTER": SORTER,
            }.items()
            if value is not None
        }

        data = self.ip_service.load(
            first=skip,
            page_size=limit,
            filters=params,
        )

        return {
            **params,
            "data": data,
        }