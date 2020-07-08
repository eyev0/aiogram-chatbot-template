from typing import Optional

import aioredis
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.utils.executor import Executor
from loguru import logger

from app import config


class BaseRedis:
    def __init__(self, host: str, port: int = 6379, db: int = 0):
        self.host = host
        self.port = port
        self.db = db

        self._redis: Optional[aioredis.Redis] = None

    @property
    def closed(self):
        return not self._redis or self._redis.closed

    async def connect(self):
        if self.closed:
            self._redis = await aioredis.create_redis_pool(
                (self.host, self.port), db=self.db
            )

    async def disconnect(self):
        if not self.closed:
            self._redis.close()
            await self._redis.wait_closed()

    @property
    def redis(self) -> aioredis.Redis:
        if self.closed:
            raise RuntimeError("Redis connection is not opened")
        return self._redis


storage = RedisStorage2(
    host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB
)


async def on_startup(dispatcher: Dispatcher):
    logger.info("Setup Redis2 Storage")
    dispatcher.storage = storage


async def on_shutdown(dispatcher: Dispatcher):
    logger.info("Close Redis Connection")
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


def setup(executor: Executor):
    executor.on_startup(on_startup)
    executor.on_shutdown(on_shutdown)
