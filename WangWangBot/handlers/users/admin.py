from aiogram import types, utils
from aiogram.dispatcher.filters.builtin import CommandHelp, Regexp

from loader import dp

from WangWangBot.utils.logger import log
from WangWangBot.config import Config
from WangWangBot.utils import docker
from WangWangBot.keyboards.inline.docker import service_list_keyboard, service_keyboard


def get_top_services_msg():
    services = docker.check_dir_service_list(Config.DOCKER_COMPOSE_DIR)
    reply_markup = service_list_keyboard()
    msg = "这台服务器上有以下服务可以管理：\n"
    for service in services:
        msg += service.name + '\n'
    msg += "\n可以直接操作整个服务组合，也可以点服务名进入单个服务操作"
    return msg, reply_markup

@dp.message_handler(commands=['admin'])
async def admin_command(message: types.Message):
    msg, reply_markup = get_top_services_msg()
    await message.answer(msg,reply_markup=reply_markup)

@dp.callback_query_handler(text="servics:back")
async def back_to_service_list(query: types.CallbackQuery):
    # 处理用户点击回到上一级的按钮
    msg, reply_markup = get_top_services_msg()
    await query.message.edit_text(msg,reply_markup=reply_markup)

@dp.callback_query_handler(Regexp(r'^services:(.+)'))
async def services_answer_callback_handler(query: types.CallbackQuery):
    # 处理所有的services的命令
    log.info(f"{query.data}")
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

@dp.callback_query_handler(Regexp(r'^services_click:(.+)'))
async def services_click_answer_callback_handler(query: types.CallbackQuery):
    # 处理用户点击了一个服务名的处理 services_click:service_name
    answer_data = query.data.split('services_click:')[1]
    reply_markup = None

    services = docker.check_dir_service_list(Config.DOCKER_COMPOSE_DIR)
    for service in services:
        if service.name == answer_data:
            reply_markup = service_keyboard(answer_data)

    if not reply_markup:
        await query.answer(text="未知的服务名",show_alert=True)
        return

    await query.message.edit_text(f"请选择对 {answer_data} 的操作",reply_markup=reply_markup)

@dp.callback_query_handler(Regexp(r'^servic:(.+)'))
async def service_answer_callback_handler(query: types.CallbackQuery):
    # 处理用户点击了service中的一个按钮
    log.info(query.data)
    action = query.data.split(':')[1]
    log.info(action)
    service = query.data.split(f'servic:{action}:')[1]
    reply_markup = None

    services = docker.check_dir_service_list(Config.DOCKER_COMPOSE_DIR)
    for service_item in services:
        if service_item.name == service:
            if action == 'up':
                msg,rcode = await docker.check_dir_up(Config.DOCKER_COMPOSE_DIR,service_item.name)
            reply_markup = service_keyboard(service)

    if not reply_markup:
        await query.answer(text="未知的服务名",show_alert=True)
        return

    await query.message.edit_text(f"{action}:{rcode}\n{msg}",reply_markup=reply_markup)