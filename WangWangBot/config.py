import os
from dotenv import load_dotenv

if os.path.exists("local.env"):
    load_dotenv("local.env")

class Config:
    WORKDIR=os.getcwd()
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "") 