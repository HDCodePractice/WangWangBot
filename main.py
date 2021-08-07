import logging

from aiogram import Bot, Dispatcher, executor, types

from WangWangBot.config import Config
from WangWangBot.set_bot_commands import set_default_commands
from WangWangBot import middlewares, filters, handlers

from WangWangBot.utils.logger import log

from loader import dp


async def on_startup(dispatcher: Dispatcher):
    me = await dp.bot.get_me()
    log.info(f"Starting... ID:{me.id} , Username:{me.full_name}")
    await set_default_commands(dispatcher)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True , on_startup=on_startup)