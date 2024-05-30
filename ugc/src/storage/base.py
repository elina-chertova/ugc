from abc import abstractmethod


class Storage:
    @abstractmethod
    async def get(self, *args, **kwargs):
        pass
