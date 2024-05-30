from storage.base import Storage

db_collection = {'Rating': 'RatingCollection',
                 'Bookmarks': 'BookmarksCollection',
                 'Review': 'ReviewCollection'}


class MongoDB(Storage):
    def __init__(self, storage):
        self.storage = storage

    def collection(self, database: str):
        db = self.storage.get_database(database)
        collection = db.get_collection(db_collection[database])
        return collection

    async def get(self, database: str, params: dict, filter_=None) -> list[dict]:
        if filter_ is None:
            filter_ = {}
        collection = self.collection(database)
        cursor = collection.find(params, filter_)
        documents = [document for document in await cursor.to_list(length=100)]
        return documents

    async def get_one(self, database: str, params: dict) -> list[dict]:
        collection = self.collection(database)
        document = await collection.find_one(params)
        return document

    async def send(self, database: str, document: dict) -> None:
        collection = self.collection(database)
        _ = await collection.insert_one(document)

    async def aggregate(self, database: str, params: dict) -> list[dict]:
        collection = self.collection(database)
        cursor = collection.aggregate(params)
        documents = await cursor.to_list(length=100)
        return documents

    async def delete_one(self, database: str, params: dict) -> None:
        collection = self.collection(database)
        _ = await collection.delete_one(params)

    async def update_one(self, database: str, filter_: dict, update_val: dict) -> None:
        collection = self.collection(database)
        _ = await collection.update_one(filter_, update_val)

