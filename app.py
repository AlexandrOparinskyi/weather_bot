import asyncio
import logging

from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from fluentogram import TranslatorHub
from redis.asyncio import Redis

from I18N import create_translator_hub
from config import load_config, Config
from bot import bot

logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] #%(levelname)-8s %(filename)s:'
               '%(lineno)d - %(name)s - %(message)s'
    )
logger = logging.getLogger(__name__)


async def app() -> None:
    config: Config = load_config()

    translator_hub: TranslatorHub = create_translator_hub()

    redis_client = Redis(
        host=config.redis.host,
        port=config.redis.port,
        db=config.redis.db,
        decode_responses=False
    )
    storage = RedisStorage(
        redis_client,
        key_builder=DefaultKeyBuilder(with_destiny=True)
    )

    await asyncio.gather(bot(
        token=config.tg_bot.token,
        hub=translator_hub,
        #storage=storage,
    ))


if __name__ == '__main__':
    asyncio.run(app())