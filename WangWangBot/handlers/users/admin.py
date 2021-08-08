import logging
from aiogram import types, utils
from aiogram.dispatcher.filters.builtin import CommandHelp, Regexp

from loader import dp

from WangWangBot.config import Config
from WangWangBot.utils import docker
from WangWangBot.keyboards.inline.docker import service_list_keyboard

@dp.message_handler(commands=['admin'])
async def send_welcome(message: types.Message):
    services = docker.check_dir_service_list(Config.DOCKER_COMPOSE_DIR)
    reply_markup = service_list_keyboard()
    msg = "这台服务器上有以下服务可以管理：\n"
    for service in services:
        msg += service.name + '\n'
    msg += "\n可以直接操作整个服务组合，也可以点服务名进入单个服务操作"
    await message.answer(msg,reply_markup=reply_markup)

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

async def send_welcome(message: types.Message):
    msg,rcode = await docker.check_dir_top(Config.DOCKER_COMPOSE_DIR)
    await message.reply(f"{rcode}:{msg}")

@dp.callback_query_handler(Regexp(r'^services:(.+)'))
async def services_answer_callback_handler(query: types.CallbackQuery):
    logging.info(f"{query.data}")
    answer_data = query.data.split('services:')[1]
    if answer_data == 'up':
        msg,rcode = await docker.check_dir_up(Config.DOCKER_COMPOSE_DIR)
    elif answer_data == 'down':
        msg,rcode = await docker.check_dir_down(Config.DOCKER_COMPOSE_DIR)
    elif answer_data == 'ps':
        msg,rcode = await docker.check_dir_ps(Config.DOCKER_COMPOSE_DIR)
    elif answer_data == 'top':
        msg,rcode = await docker.check_dir_top(Config.DOCKER_COMPOSE_DIR)
    elif answer_data == 'pull':
        msg,rcode = await docker.check_dir_pull(Config.DOCKER_COMPOSE_DIR)
    else:
        msg,rcode = '不知道您要做啥',1
    reply_markup = service_list_keyboard()
    if len(str(msg)) > 2048:
        msg = msg[-2000:]
    await query.message.edit_text(f"{answer_data}:{rcode}\n{msg}",reply_markup=reply_markup)