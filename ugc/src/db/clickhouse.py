from typing import Optional

from clickhouse_driver import Client

clickhouse: Optional[Client] = None


async def get_clickhouse() -> Client:
    return clickhouse
