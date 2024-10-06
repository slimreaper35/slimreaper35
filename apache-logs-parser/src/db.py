from dataclasses import dataclass, field
from typing import Any

from pymongo import MongoClient


@dataclass
class MongoManager:
    host: str
    port: int
    username: str = "root"
    passwrod: str = "example"

    collection: Any = field(init=False)

    def __post_init__(self):
        self.client = MongoClient(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.passwrod,
        )
        self.init_collection()

    def init_collection(self):
        self.collection = self.client["db"]["logs"]

    def count_key_value(self, key: str, value: str):
        return self.collection.count_documents({key: value})

    def count_key(self, key: str):
        return self.collection.count_documents({key: {"$exists": True}})

    def get_unique_values(self, key: str):
        return self.collection.distinct(key)

    def reset_collection(self):
        self.collection.drop()
        self.init_collection()

    def insert(self, data: dict[str, Any]):
        self.collection.insert_one(data)


mongo_manager = MongoManager("mongo", 27017)
