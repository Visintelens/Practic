import asyncio
from asyncio.log import logger

from aiogram import Bot, Dispatcher

import logging
import sqlite3

from aiogram.utils import executor

from tg_bot.config import load_config, Config
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tg_bot.handlers.callback_q import registration_callback
from tg_bot.handlers.echo import register_echo
from tg_bot.handlers.faq import register_faq
from tg_bot.handlers.featured_news import register_featured_news, featured_posts
from tg_bot.handlers.schedule import register_schedule
from tg_bot.handlers.start_user import register_user
from tg_bot.handlers.surveys import register_surveys
from tg_bot.handlers.unwatched_news import register_news, new_post


def register_all_filters(dp):
    dp.filters_factory.bind(...)


def register_all_handlers(dp):
    register_user(dp)
    registration_callback(dp)
    register_faq(dp)
    register_surveys(dp)
    register_featured_news(dp)
    register_news(dp)
    register_schedule(dp)
    register_echo(dp)


async def parsing_popular_news(bot: Bot, config: Config):
    featured_posts()


async def send_message_to_admin(bot: Bot, config: Config):
    for admin_id in config.tg_bot.admin_ids:
        text = new_post()
        if text == "Нет новостей" or text is None:
            pass
        else:
            await bot.send_message(text=str(text), chat_id=admin_id)


def set_scheduled_jobs(scheduler, bot, config, *args, **kwargs):
    scheduler.add_job(send_message_to_admin, "interval", seconds=5, args=(bot, config))
    scheduler.add_job(parsing_popular_news, "interval", seconds=7, args=(bot, config))


async def main():
    logging.basicConfig(level=logging.INFO)
    config = load_config()
    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    scheduler = AsyncIOScheduler()
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS users(user_id INTEGER,name_user TEXT,Role TEXT , block INTEGER,NewsGroup TEXT, NewsAll TEXT,GROUPS TEXT,EMAIL TEXT);""")
    conn.commit()
    bot['config'] = config
    set_scheduled_jobs(scheduler, bot, config)
    register_all_handlers(dp)
    try:
        scheduler.start()
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except(KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
