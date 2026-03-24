from pydantic import BaseModel, TypeAdapter
from valkey import Valkey
from typing import TypeVar, Any, Optional, List, Union, Type
import os

T = TypeVar("T", bound=BaseModel)


class CacheManager:
    def __init__(self, host: str, version: str = "v1"):
        self.host = host or os.getenv("VALKEY_HOST", "localhost")
        self.client = Valkey(host=self.host, port=6379, decode_responses=True)
        self.version = version

    def get_key(self, cache_key: str):
        return f"nba-app:{self.version}:{cache_key.lower()}"

    def get_model(self, cache_key: str, model: Type[T]) -> Optional[T]:
        data = self.client.json().get(self.get_key(cache_key))

        if data:
            try:
                return model.model_validate(data)
            except Exception:
                self.client.delete(self.get_key(cache_key))
        return None

    def get_model_list(self, cache_key: str, model: Type[T]) -> Optional[List[T]]:
        data = self.client.json().get(self.get_key(cache_key))

        if data:
            try:
                adapter = TypeAdapter(List[model])
                return adapter.validate_python(data)
            except Exception:
                self.client.delete(self.get_key(cache_key))
        return None

    def set(
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

        self.client.json().set(key, "$", serialized_data)
        self.client.expire(key, expire)
