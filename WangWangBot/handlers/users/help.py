from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = (
        "这个Bot的作用就是帮你做些汪汪常做的事",
        "记得在使用前要在服务器上设置好你的yaml文件和相关环境变量"
    )
    await message.answer("\n".join(text))