import logging

from fastapi import APIRouter, Depends, Request

from exceptions import ObjectNotExists
from models.base import (BaseModel, DuplicatesResponseModel,
                         EncodedKeyResponseModel)
from responses import NO_CONTENT_RESPONSE, NOT_FOUND_RESPONSE
from services.base_service import BaseService, get_base_service

router = APIRouter()

logging.basicConfig(level=logging.INFO)


@router.get(
    '/get',
    response_description='Возвращает телло искомого запроса',
    response_model=BaseModel,
)
async def get_obj(
    key: str,
    base_service: BaseService = Depends(get_base_service)
):
    try:
        obj = await base_service.get_object_by_encoded_key(encoded_key=key)
    except ObjectNotExists:
        return NOT_FOUND_RESPONSE
    return obj


@router.post(
    '/add',
    response_description='Возвращает ключ, по которому'
                         ' можно получить тело запроса',
    response_model=EncodedKeyResponseModel
)
async def add_obj(
    request: Request,
    base_service: BaseService = Depends(get_base_service)
):
    obj = await base_service.add_object(body=await request.json())
    return obj


@router.delete(
    '/remove',
    response_description='Удаляет запрос по ключу',
)
async def delete_obj(
    key: str,
    base_service: BaseService = Depends(get_base_service)
):
    try:
        await base_service.delete_object(encoded_key=key)
    except ObjectNotExists:
        return NOT_FOUND_RESPONSE
    return NO_CONTENT_RESPONSE


@router.put(
    '/update',
    response_description='Изменяет тело запроса и возвращает новый ключ',
    response_model=EncodedKeyResponseModel
)
async def update_obj(
    request: Request,
    key: str,
    base_service: BaseService = Depends(get_base_service)
):
    try:
        obj = await base_service.update_object(encoded_key=key,
                                               body=await request.json())
    except ObjectNotExists:
        return NOT_FOUND_RESPONSE
    return obj


@router.get(
    '/statistic',
    response_description='Возвращает процент дубликатов '
                         'от количества общих запросов',
    response_model=DuplicatesResponseModel
)
async def get_statistics(
    base_service: BaseService = Depends(get_base_service)
):
    duplicates_percentage = await base_service.get_duplicates_statistics()
    return duplicates_percentage
