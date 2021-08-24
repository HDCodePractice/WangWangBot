from aiogram import types, utils
from aiogram.dispatcher.filters.builtin import Regexp
from aiogram.utils.markdown import quote_html
from loader import dp

from WangWangBot.utils.logger import log
from WangWangBot.config import Config
from WangWangBot.utils import docker
from WangWangBot.keyboards.inline.docker import service_list_keyboard, service_keyboard

from compose.config.errors import ComposeFileNotFound
from docker.errors import DockerException

def get_top_services_msg():
    services = docker.check_dir_service_list(Config.DOCKER_COMPOSE_DIR)
    reply_markup = service_list_keyboard()
    msg = "这台服务器上有以下服务可以管理：\n"
    for service in services:
        msg += service.name + '\n'
    msg += "\n可以直接操作整个服务组合，也可以点服务名进入单个服务操作"
    return msg, reply_markup

@dp.message_handler(in_admins=True,commands=['admin'])
async def admin_command(message: types.Message):
    try:
        msg, reply_markup = get_top_services_msg()
        await message.answer(msg,reply_markup=reply_markup)
    except ComposeFileNotFound:
        msg = "没有找到docker-compose.yml文件。请将docker-compose的配置文件放在mount到/data的目录中。"
        await message.answer(msg)
    except DockerException:
        msg = "调用Docker请求出错，请确认您的Docker daemon已经启动。"
        await message.answer(msg)
    

@dp.callback_query_handler(text="servics:back", in_admins=True)
async def back_to_service_list(query: types.CallbackQuery):
    # 处理用户点击回到上一级的按钮
    msg, reply_markup = get_top_services_msg()
    await query.message.edit_text(msg,reply_markup=reply_markup)

@dp.callback_query_handler(Regexp(r'^services:(.+)'), in_admins=True)
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
    if len(str(msg)) > 4096:
        msg = msg[-4000:]
    await query.message.edit_text(f"{answer_data}:{rcode}\n{msg}",reply_markup=reply_markup)

@dp.callback_query_handler(Regexp(r'^services_click:(.+)'), in_admins=True)
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

@dp.callback_query_handler(Regexp(r'^servic:(.+)'), in_admins=True)
async def service_answer_callback_handler(query: types.CallbackQuery):
    # 处理用户点击了service中的一个按钮
    log.info(query.data)
    action = query.data.split(':')[1]
    service = query.data.split(f'servic:{action}:')[1]
    reply_markup = None

    services = docker.check_dir_service_list(Config.DOCKER_COMPOSE_DIR)
    for service_item in services:
        if service_item.name == service:
            if action == 'up':
                msg,rcode = await docker.check_dir_up(Config.DOCKER_COMPOSE_DIR,service_item.name)
            elif action == 'top':
                msg,rcode = await docker.check_dir_top(Config.DOCKER_COMPOSE_DIR,service_item.name)
            elif action == 'logs':
                msg,rcode = await docker.check_dir_logs(Config.DOCKER_COMPOSE_DIR,service_item.name)
            elif action == 'stop':
                msg,rcode = await docker.check_dir_stop(Config.DOCKER_COMPOSE_DIR,service_item.name)
            reply_markup = service_keyboard(service)
    
    if not reply_markup:
        await query.answer(text="未知的服务名",show_alert=True)
        return
    
    if len(str(msg)) > 4096:
        msg = msg[-4000:]

    await query.message.edit_text(
        f"{action}:{rcode}\n{quote_html(msg)}",
        reply_markup=reply_markup,
        parse_mode=types.ParseMode.HTML)