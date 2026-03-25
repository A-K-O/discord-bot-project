from pydantic import BaseModel, TypeAdapter
from valkey.asyncio import Valkey
from typing import TypeVar, Any, Optional, List, Union, Type, cast, Coroutine
import os

T = TypeVar("T", bound=BaseModel)


class CacheManager:
    def __init__(self, host: str, version: str = "v1"):
        self.host = host or os.getenv("VALKEY_HOST", "localhost")
        self.client = Valkey(host=self.host, port=6379, decode_responses=True)
        self.version = version

    def get_key(self, cache_key: str):
        return f"nba-app:{self.version}:{cache_key.lower()}"

    async def get_model(self, cache_key: str, model: Type[T]) -> Optional[T]:
        key = self.get_key(cache_key)
        json_interface = self.client.json()
        data = await cast(Coroutine[Any, Any, Any], json_interface.get(key))

        if data:
            try:
                return model.model_validate(data[0])
            except Exception:
                await self.client.delete(key)
        return None

    async def get_model_list(self, cache_key: str, model: Type[T]) -> Optional[List[T]]:
        key = self.get_key(cache_key)
        json_interface = self.client.json()
        data = await cast(Coroutine[Any, Any, Any], json_interface.get(key))

        if data and isinstance(data, list):
            try:
                adapter = TypeAdapter(List[model])
                return adapter.validate_python(data[0])
            except Exception:
                await self.client.delete(key)
        return None

    async def set(
        self,
        cache_key: str,
        data: Union[BaseModel, List[BaseModel]],
        expire: int = 86400,
    ):
        key = self.get_key(cache_key)

        if isinstance(data, list):
            serialized_data = [m.model_dump() for m in data]
        else:
            serialized_data = data.model_dump()

        json_interface = self.client.json()

        await cast(
            Coroutine[Any, Any, Any], json_interface.set(key, "$", serialized_data)
        )

        await self.client.expire(key, expire)


VALKEY_HOST = os.getenv("VALKEY_HOST", "valkey")
vache = CacheManager(host=VALKEY_HOST)
