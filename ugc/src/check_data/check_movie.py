import aiohttp
from core.config import Settings

conf = Settings()


async def check_movie(film_id: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://{conf.movie_service_host}:{conf.movie_service_port}/api/v1/films/{film_id}") as response:
            message = await response.json()
            code = response.status
            return message, code
