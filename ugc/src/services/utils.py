from abc import abstractmethod


class BaseViews:
    @property
    @abstractmethod
    def topic(self) -> str:
        pass

    @abstractmethod
    async def send_view_info(self, timing: int, user_id: str, movie_id: str, movie_time: int):
        pass

    @abstractmethod
    async def get_history(self, user_id: str, page: int, page_size: int):
        pass


class BaseUser:
    @property
    @abstractmethod
    def database(self) -> str:
        pass

    @abstractmethod
    async def send(self, *args, **kwargs) -> str:
        pass

    @abstractmethod
    async def get(self, *args, **kwargs):
        pass



