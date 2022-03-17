import base64
from functools import lru_cache

from fastapi import Depends

from db.mongo_adapter import AbstractDBAdapter, get_mongo
from exceptions import ObjectNotExists
from models.base import (BaseModel, DuplicatesResponseModel,
                         EncodedKeyResponseModel)


class BaseService:

    def __init__(self, db_adapter: AbstractDBAdapter):
        self.db_adapter = db_adapter

    @staticmethod
    def __generate_encoded_key(body: dict) -> str:
        key_value_sum = "".join([key + str(value) for key, value in body.items()])
        encoded_key = (base64.b64encode(key_value_sum.encode('UTF-8')).decode('UTF-8'))
        return encoded_key

    async def get_object_by_encoded_key(self, encoded_key: str) -> BaseModel:
        obj = await self.db_adapter.get_object_from_db(encoded_key=encoded_key)
        if not obj:
            raise ObjectNotExists()
        return obj

    async def add_object(self, body: dict) -> EncodedKeyResponseModel:
        encoded_key = self.__generate_encoded_key(body)
        already_exists_object = await self.db_adapter.get_object_from_db(encoded_key=encoded_key)
        if already_exists_object:
            await self.db_adapter.update_object_from_db(updated_fields={'$inc': {'duplicates_count': 1}},
                                                        encoded_key=encoded_key)

        else:
            obj = BaseModel(encoded_key=encoded_key, body=body)
            await self.db_adapter.add_object_to_db(
                obj.dict()
            )
        return EncodedKeyResponseModel(encoded_key=encoded_key)

    async def delete_object(self, encoded_key: str) -> None:
        exist_obj = await self.db_adapter.get_object_from_db(
            encoded_key=encoded_key
        )
        if not exist_obj:
            raise ObjectNotExists()
        await self.db_adapter.delete_object_from_db(encoded_key=encoded_key)

    async def update_object(self, encoded_key: str, body: dict) -> EncodedKeyResponseModel:
        obj = await self.db_adapter.get_object_from_db(encoded_key=encoded_key)
        if not obj:
            raise ObjectNotExists()
        if obj.body != body:
            obj.encoded_key = self.__generate_encoded_key(body)
            obj.body = body
        await self.db_adapter.update_object_from_db(updated_fields={'$set': {'duplicates_count': 0,
                                                                             'body': obj.body,
                                                                             'encoded_key': obj.encoded_key
                                                                             }
                                                                    },
                                                    encoded_key=encoded_key)
        return EncodedKeyResponseModel(encoded_key=obj.encoded_key)

    async def get_duplicates_statistics(self) -> DuplicatesResponseModel:
        pipeline = [{'$group': {'_id': 0, 'sum': {'$sum': '$duplicates_count'}}}]
        objects_count = await self.db_adapter.get_objects_count()
        duplicates_count = await self.db_adapter.aggregate_objects(pipeline=pipeline)
        duplicates_percentage = (objects_count / duplicates_count['sum']) * 100
        return DuplicatesResponseModel(duplicates_percentage=duplicates_percentage)


@lru_cache()
def get_base_service(
    db_adapter: AbstractDBAdapter = Depends(get_mongo),
) -> BaseService:
    return BaseService(
        db_adapter=db_adapter
    )
