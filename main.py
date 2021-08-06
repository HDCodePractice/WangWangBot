import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from asyncio.tasks import sleep
from asyncio import sleep

from WangWangBot.config import Config
from WangWangBot.utils.logger import log

bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    msg = await message.reply("汪汪机器人会时刻帮你完成任何好玩的事。")

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    msg = await message.reply("想让我帮忙做什么呢？")
    await sleep(10)
    await msg.delete()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)