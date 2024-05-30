from typing import Optional

from pymongo import MongoClient

mongodb: Optional[MongoClient] = None


async def get_mongodb() -> Optional[MongoClient]:
    return mongodb
