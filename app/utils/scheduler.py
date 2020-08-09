from aiogram import Dispatcher
from aiogram.utils.executor import Executor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from app import config
from app.middlewares.i18n import i18n

_ = i18n.gettext
scheduler = AsyncIOScheduler()


async def on_startup(dispatcher: Dispatcher):
    logger.info("Configuring scheduler..")
    jobstores = {"default": SQLAlchemyJobStore(url=config.POSTGRES_URI)}
    job_defaults = {"misfire_grace_time": 300}
    scheduler.configure(
        jobstores=jobstores, job_defaults=job_defaults,
    )

    scheduler.start()


async def on_shutdown(dispatcher: Dispatcher):
    logger.info("Shutting down scheduler..")
    scheduler.shutdown()


def setup(executor: Executor):
    executor.on_startup(on_startup)
    executor.on_shutdown(on_shutdown)
