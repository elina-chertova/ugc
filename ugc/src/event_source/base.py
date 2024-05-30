from abc import abstractmethod


class EventSource:
    @abstractmethod
    async def send(self, *args, **kwargs) -> None:
        pass
