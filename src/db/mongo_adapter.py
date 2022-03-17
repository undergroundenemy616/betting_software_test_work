from typing import Optional

import backoff
from motor.motor_asyncio import AsyncIOMotorClient
from models.base import BaseModel
from core.config import settings

from db.abstract_adapter import AbstractDBAdapter

mongo_client: Optional[AsyncIOMotorClient] = None


class MongoAdapter(AbstractDBAdapter):
    database_name = settings.MONGO_DB_NAME
    collection_name = settings.MONGO_DB_COLLECTION

    def __init__(self,
                 mongo: AsyncIOMotorClient,
                 model):
        self.mongo_client = mongo
        self.model = model

    @property
    def __collection(self):
        return getattr(self.mongo_client, self.database_name).get_collection(
            self.collection_name
        )

    @backoff.on_exception(backoff.expo, ConnectionError)
    async def get_objects_count(self) -> int:
        return await self.__collection.count_documents({})

    @backoff.on_exception(backoff.expo, ConnectionError)
    async def aggregate_objects(self, pipeline: list) -> dict:
        async for obj in self.__collection.aggregate(pipeline=pipeline):
            return obj

    @backoff.on_exception(backoff.expo, ConnectionError)
    async def get_objects_from_db(
        self, query: dict, skip: int, limit: int
    ) -> list:

        data = []
        async for obj in self.__collection.find(query).skip(skip).limit(limit):
            data.append(self.model(**obj))
        return data

    @backoff.on_exception(backoff.expo, ConnectionError)
    async def get_object_from_db(self, **kwargs):
        collection = getattr(self.mongo_client, self.database_name).get_collection(
            self.collection_name
        )
        obj = await collection.find_one(kwargs)
        if obj:
            return self.model(**obj)
        return None

    @backoff.on_exception(backoff.expo, ConnectionError)
    async def add_object_to_db(self, obj: dict):
        await self.__collection.insert_one(obj)

    @backoff.on_exception(backoff.expo, ConnectionError)
    async def delete_object_from_db(self, **kwargs):
        await self.__collection.delete_one(kwargs)

    @backoff.on_exception(backoff.expo, ConnectionError)
    async def update_object_from_db(
        self, updated_fields: dict, **kwargs
    ):

        await self.__collection.update_one(kwargs, updated_fields)


async def get_mongo() -> MongoAdapter:
    return MongoAdapter(mongo=mongo_client,
                        model=BaseModel)