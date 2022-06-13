__all__ = 'es_fake_data_loader'

import asyncio
import json
from typing import Dict

import aiofiles as aiofiles
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

FILE_PATH_DATA = "es_data/fake_es_data/data"
FILE_PATH_INDEX = "es_data/fake_es_data/index"


def generate_data(index: str, data: Dict) -> Dict:
    for item in data:
        yield dict(_index=index, _id=item["uuid"], _source=item)


async def load_json_data(file_path: str, index: str, ) -> Dict[str, any]:
    async with aiofiles.open(f"{file_path}/{index}.json") as file:
        data = await file.read()
    result = json.loads(data)
    return result


async def load_fake_data(
        elastic_client: AsyncElasticsearch, index: str
):
    result = await load_json_data(file_path=FILE_PATH_DATA, index=index)
    await async_bulk(elastic_client, generate_data(index, result))


async def create_es_index(
        elastic_client: AsyncElasticsearch, index: str
):
    if not await elastic_client.indices.exists(index=index):
        loaded_index = await load_json_data(file_path=FILE_PATH_INDEX, index=index)
        await elastic_client.indices.create(index=index,
                                            body=loaded_index,
                                            )
    await asyncio.sleep(0.5)


async def es_fake_data_loader(settings, es_client: AsyncElasticsearch) -> None:
    for index in settings.es_indexes:
        await create_es_index(elastic_client=es_client, index=index)
        await load_fake_data(elastic_client=es_client, index=index)
