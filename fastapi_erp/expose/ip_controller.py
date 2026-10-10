from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
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

    # ---------------------------------------------------------
    # CREATE
    # ---------------------------------------------------------

    @router.post("", response_model=UtiIp)
    async def create(
        self,
        entity: UtiIpCreate,
    ):
        return await self.ip_service.create(entity)

    # ---------------------------------------------------------
    # UPDATE
    # ---------------------------------------------------------

    @router.put("/{ip_id}", response_model=UtiIp)
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

    # ---------------------------------------------------------
    # DISABLE
    # ---------------------------------------------------------

    @router.post("/disable")
    async def disable(
        self,
        ids: list[int],
    ):
        await self.ip_service.disable(ids)

        return {
            "message": "IP records disabled successfully"
        }

    # ---------------------------------------------------------
    # DELETE
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # FINISH
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # PREPARE
    # ---------------------------------------------------------

    @router.get(
        "/prepare",
        response_model=UtiIp,
    )
    async def prepare(self):
        return await self.ip_service.prepare()

    # ---------------------------------------------------------
    # CATEGORIES
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # CLEAN
    # ---------------------------------------------------------

    @router.put("/limpiar/{ip_id}")
    async def clean(
        self,
        ip_id: int,
    ):
        result = await self.ip_service.clean(ip_id)

        if not result:
            raise HTTPException(
                status_code=404,
                detail="IP not found",
            )

        return {
            "message": "IP cleaned successfully"
        }

    # ---------------------------------------------------------
    # COUNT
    # ---------------------------------------------------------

    @router.get("/count")
    async def count(self):
        return await self.ip_service.count()

    # ---------------------------------------------------------
    # GET
    # ---------------------------------------------------------

    @router.get(
        "/{ip_id}",
        response_model=UtiIp,
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

    # ---------------------------------------------------------
    # LIST
    # ---------------------------------------------------------

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