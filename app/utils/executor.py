import asyncio
from contextlib import suppress

from aiogram import Dispatcher
from aiogram.utils.exceptions import TelegramAPIError
from aiogram.utils.executor import Executor
from loguru import logger
from sqlalchemy import or_

from app import config
from app.misc import dp
from app.models import db
from app.models.user import User
from app.utils import redis, scheduler

runner = Executor(dp)


async def on_startup_webhook(dispatcher: Dispatcher):
    logger.info("Configure Web-Hook URL to: {url}", url=config.WEBHOOK_URL)
    await dispatcher.bot.set_webhook(config.WEBHOOK_URL)


async def on_startup_notify(dispatcher: Dispatcher):
    for user in await User.query.where(
        or_(User.is_superuser == True, User.id.in_(config.BOT_SU))  # NOQA
    ).gino.all():
        with suppress(TelegramAPIError):
            await dispatcher.bot.send_message(
                chat_id=user.id, text="Bot started", disable_notification=True
            )
            logger.info("Notified superuser {user} about bot is started.", user=user.id)
        await asyncio.sleep(0.2)


def setup():
    logger.info("Configure executor...")
    db.setup(runner)
    redis.setup(runner)
    scheduler.setup(runner)
    runner.on_startup(on_startup_webhook, webhook=True, polling=False)
    if config.SUPERUSER_STARTUP_NOTIFIER:
        runner.on_startup(on_startup_notify)
