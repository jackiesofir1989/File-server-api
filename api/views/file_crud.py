# -*- coding: utf-8 -*-
from typing import NewType
from uuid import UUID

from fastapi_utils.api_model import APIMessage, APIModel
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

# Begin Setup
UserID = NewType("UserID", UUID)
ItemID = NewType("ItemID", UUID)


class ItemCreate(APIModel):
    name: str
    owner: UserID


class ItemInDB(ItemCreate):
    item_id: ItemID


router = InferringRouter()


@cbv(router)
class FileCRUD:

    @router.post("/item")
    def create_item(self, item: ItemCreate) -> ItemInDB:
        item_orm = ItemORM(name=item.name, owner=self.user_id)
        return ItemInDB.from_orm(item_orm)

    @router.get("/item/{item_id}")
    def read_item(self, item_id: ItemID) -> ItemInDB:
        item_orm = get_owned_item(self.user_id, item_id)
        return ItemInDB.from_orm(item_orm)

    @router.put("/item/{item_id}")
    def update_item(self, item_id: ItemID, item: ItemCreate) -> ItemInDB:
        item_orm = get_owned_item(self.user_id, item_id)
        item_orm.name = item.name
        return ItemInDB.from_orm(item_orm)

    @router.delete("/item/{item_id}")
    def delete_item(self, item_id: ItemID) -> APIMessage:
        item = get_owned_item(self.user_id, item_id)
        return APIMessage(detail=f"Deleted item {item_id}")
