from aiogram import Dispatcher

from loader import dp
from . import admin

dp.filters_factory.bind(admin.AdminFilter)