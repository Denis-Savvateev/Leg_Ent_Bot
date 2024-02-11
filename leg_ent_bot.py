import logging
import os
import sys

from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv
from telegram.ext import CommandHandler, MessageHandler, Updater

from api_egrul import get_data_from_api_with_inn

load_dotenv()

TELEGRAM_TOKEN: str = os.getenv('TOKEN')
TELEGRAM_CHAT_ID: str = os.getenv('MY_CHAT_ID')

def wakeup():
    ...


def new_leg_ent():
    ...


def main ():
    updater = Updater(token=TELEGRAM_TOKEN)
    updater.dispatcher.add_handler(CommandHandler('start', wakeup))


if __name__ == '__main__':
    main()