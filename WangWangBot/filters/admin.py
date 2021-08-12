from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from typing import Union

from ..config import Config

ADMINS = Config.ADMINS

class AdminFilter(BoundFilter):
    key = 'in_admins'

    def __init__(self, in_admins: bool):
        self.in_admins = in_admins

    async def check(self, message: Union[types.Message,types.CallbackQuery]) -> bool:
        if message.from_user.id in ADMINS:
            return True
        else:
            if isinstance(message, types.Message):
                await message.reply('你不是管理员，小心他发现你在搞小动作')
            elif isinstance(message, types.CallbackQuery):
                await message.answer('你不是管理员，小心他发现你在搞小动作',show_alert=True)
            return False
