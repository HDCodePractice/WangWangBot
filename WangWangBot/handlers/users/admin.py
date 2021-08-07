from aiogram import types, utils
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp

from WangWangBot.config import Config
from WangWangBot.utils import docker

@dp.message_handler(commands=['admin'])
async def send_welcome(message: types.Message):
    services = docker.check_dir_service_list(Config.DOCKER_COMPOSE_DIR)
    msg = "这台服务器上有以下服务可以管理：\n"
    for service in services:
        msg += service.name + '\n'
    await message.reply(msg)


@dp.message_handler(commands=['up'])
async def send_welcome(message: types.Message):
    msg,rcode = await docker.check_dir_up(Config.DOCKER_COMPOSE_DIR)
    await message.reply(f"{rcode}:{msg}")


@dp.message_handler(commands=['down'])
async def send_welcome(message: types.Message):
    msg,rcode = await docker.check_dir_down(Config.DOCKER_COMPOSE_DIR)
    await message.reply(f"{rcode}:{msg}")

@dp.message_handler(commands=['ps'])
async def send_welcome(message: types.Message):
    msg,rcode = await docker.check_dir_ps(Config.DOCKER_COMPOSE_DIR)
    await message.reply(f"{rcode}:{msg}")

@dp.message_handler(commands=['top'])
async def send_welcome(message: types.Message):
    msg,rcode = await docker.check_dir_top(Config.DOCKER_COMPOSE_DIR)
    await message.reply(f"{rcode}:{msg}")