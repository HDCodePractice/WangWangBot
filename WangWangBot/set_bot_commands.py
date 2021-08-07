from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("help", "帮助"),
            types.BotCommand("admin", "管理"),
        ]
    )