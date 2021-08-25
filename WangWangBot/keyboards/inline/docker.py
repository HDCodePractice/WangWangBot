import logging

from aiogram import types

from WangWangBot.utils import docker

from WangWangBot.config import Config
from WangWangBot.utils import docker

def services_button() -> tuple:
    """
    所有服务的按钮

    :return: tuple of buttons
    """
    text_and_data = (
        ("up", "services:up"),
        ("down", "services:down"),
        ("ps", "services:ps"),
        ("top", "services:top"),
        ("pull", "services:pull")
    )    
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
    return row_btns


def service_keyboard(service_name:str) -> types.InlineKeyboardMarkup:
    """
    单个服务的按钮

    return: InlineKeyboardMarkup
    """
    text_and_data = (
        ("up", f"servic:up:{service_name}"),
        ("top", f"servic:top:{service_name}"),
        ("logs", f"servic:logs:{service_name}"),
        ("stop", f"servic:stop:{service_name}"),
        ("返回", f"servics:back")
    )
    keyboard_markup = types.InlineKeyboardMarkup()
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
    keyboard_markup.add(*row_btns)
    return keyboard_markup

def service_list_keyboard() -> types.InlineKeyboardMarkup:
    """
    得到所有service的InlineKeyboardMarkup

    return: InlineKeyboardMarkup
    """
    service_list = docker.check_dir_service_list(Config.DOCKER_COMPOSE_DIR)
    keyboard_markup = types.InlineKeyboardMarkup()
    keyboard_markup.add(*services_button())
    row_btns = (types.InlineKeyboardButton(service.name, callback_data=f"services_click:{service.name}") for service in service_list)
    keyboard_markup.add(*row_btns)
    return keyboard_markup