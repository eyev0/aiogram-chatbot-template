import aiohttp
from aiogram import Bot, Dispatcher, types
from loguru import logger

from app import config

proxy_auth = aiohttp.BasicAuth(
    login=config.PROXY_USERNAME, password=config.PROXY_PASSWORD
)

bot = Bot(
    token=config.BOT_TOKEN,
    proxy=config.PROXY_URL,
    proxy_auth=proxy_auth,
    parse_mode=types.ParseMode.HTML,
)
dp = Dispatcher(bot)


def setup():
    from app import filters, middlewares
    from app.utils import executor

    middlewares.setup(dp)
    filters.setup(dp)
    executor.setup()

    logger.info("Register handlers...")
    # noinspection PyUnresolvedReferences
    import app.handlers
