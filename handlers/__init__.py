""" Пакет роутеров fastapi. """

from handlers.channels import router as channels
from handlers.accounts import router as accounts
from handlers.logic_app import router as logic_app

routers = [
    channels,
    accounts,
    logic_app,
    ]