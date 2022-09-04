# -*- coding: utf-8 -*-
"""
@author: pablo

"""

# From env

from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters
import logging

from utils import const as c
from botwrapper import Botwrapper

# Enable logging
logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)

logger = logging.getLogger(__name__)


def main():
    # Create the Updater and pass it your bot's token.
    TOKEN = "2008917266:AAEllxW_5K7fLUDL1b1vOJjG4fZKG8P8PEg"

    bot = Botwrapper(TOKEN)

    conv_handler = ConversationHandler(
            entry_points = [MessageHandler(Filters.text & ~Filters.command, bot.search),
                            CommandHandler('start', bot.start)],

            states = {
                c.HANDLE_NAME: [MessageHandler(Filters.text & ~Filters.command, bot.search)],
            },

            fallbacks = [CommandHandler('stop', bot.stop_bot)]
    )

    bot.dispatcher.add_handler(conv_handler)
    bot.updater.start_polling()
    bot.updater.idle()


if __name__ == '__main__':
    main()
