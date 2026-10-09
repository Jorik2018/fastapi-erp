from fastapi import APIRouter, Depends, HTTPException
from fastapi_erp.business.user_service import UserService
from fastapi_erp.business.item_service import ItemService
from fastapi_erp.cbv import cbv
from fastapi_erp.model.api.item import Item, ItemCreate

router = APIRouter(prefix="/item", tags= ["Items"])

userService = UserService()

@cbv(router)
class ItemController:

    item_service: ItemService = Depends(ItemService.instance)

    @router.get("/{item_id}", response_model=Item)
    async def get(self, item_id: int):
        result = await self.item_service.get(item_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return result
    
    @router.get("/{skip}/{limit}", response_model=list[Item])
    def list(self, skip: int = 0, limit: int = 3):
        return self.item_service.list(skip=skip, limit=limit)
    
    @router.put("/{item_id}", response_model=dict)
    async def update(self, item_id: int, new_item: dict):
        return await self.item_service.update(item_id, new_item)

    @router.delete("/{item_id}", response_model=dict)
    async def delete(self, item_id: int):
        if not await self.item_service.delete(item_id):
            raise HTTPException(status_code=404, detail="Item not found")
        return {"message": "Item deleted successfully"}

    @router.post("", response_model=dict)
    async def create(self, item_create: ItemCreate):
        return self.item_service.create(item_create)
