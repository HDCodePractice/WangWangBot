from email.policy import default
import os
from environs import Env
from io import StringIO
from dotenv import load_dotenv

import requests
from base64 import b64encode


def get_doppler_env(token):
    token_b64 = b64encode(f"{token}:".encode()).decode()

    url = "https://api.doppler.com/v3/configs/config/secrets/download"

    querystring = {"format":"env"}

    headers = {
        "Accept": "application/json",
        "Authorization": f"Basic {token_b64}"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.text
    return ""

env = Env()
env.read_env(f"{os.getcwd()}/local.env")

e = os.environ

def set_env_by_doppler():
    pass

doppler_token = env.str('DOPPLER_TOKEN', default='')

if len(doppler_token) > 0 :
    response = get_doppler_env(doppler_token)
    if len(response) > 0:
        config = StringIO(response)
        load_dotenv(stream=config)

class Config:
    WORKDIR=os.getcwd()
    BOT_TOKEN = env.str('BOT_TOKEN', default='')
    DOCKER_COMPOSE_DIR = env.str('DOCKER_COMPOSE_DIR', default=f"{WORKDIR}/")
    ADMINS = env.list("ADMINS")