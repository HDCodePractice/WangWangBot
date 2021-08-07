from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp

@dp.message_handler(CommandStart())
async def send_welcome(message: types.Message):
    msg = await message.reply("汪汪机器人会时刻帮你完成任何好玩的事。")