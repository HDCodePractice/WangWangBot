import os
from environs import Env

env = Env()
env.read_env()

class Config:
    WORKDIR=os.getcwd()
    BOT_TOKEN = env.str('BOT_TOKEN', default='')
    DOCKER_COMPOSE_DIR = env.str('DOCKER_COMPOSE_DIR', default=f"{WORKDIR}/")
    ADMINS = env.list("ADMINS")