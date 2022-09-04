# -*- coding: utf-8 -*-
"""
@author: pablo

"""

### MODULES

# From env
import os

from telegram import ParseMode, Update
from telegram.ext import Updater, CallbackContext

from scrapeutils import youtubemp3
from scrapeutils.scraper import scrape_video_ID, scrape_artist_name, scrape_song_name
from utils import const as c, utility
from commands.command_handler import CommandHandler
from django.core.validators import URLValidator


class Botwrapper:

    def __init__(self, token) -> None:
        # Create the Updater and pass it your bot's token.
        self.updater = Updater(token)

        # Get the dispatcher to register handlers
        self.dispatcher = self.updater.dispatcher

        # Top level conversation callbacks

    def start(self, update: Update, context: CallbackContext) -> None:
        """SbaBot greetings message and general commands"""
        """if c.CHAT_ID not in context.user_data:
            context.user_data[c.CHAT_ID] = update.message.chat_id
            print(context.user_data[c.CHAT_ID]) """

        username = update.message.from_user.first_name
        start_msg = self._greetings(username)
        update.message.reply_text(text=start_msg, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        return c.HANDLE_NAME

    def stop_bot(self, update: Update, context: CallbackContext) -> None:
        """Completely end conversation"""
        context.user_data[c.START_OVER] = False
        text = 'Okay, bye.'
        #   self.__sendMessage(context, text)

        return c.END

    def search(self, update: Update, context: CallbackContext) -> None:
        command_handler = CommandHandler()
        name = update.message.text
        chat_id = update.message.chat_id

        if len(update.message.entities) == 0:
            if chat_id < 0:
                return
        try:
            validate = URLValidator()
            validate(name)
            return
        except:
            pass

        filtered_name1 = name.replace('@stopmf_bot ', '')
        try:
            result_dict = utility.parse_options(filtered_name1)
            filtered_name2 = result_dict['filename']

            videoid = ''
            try:
                videoid = scrape_video_ID(filtered_name2)
            except:
                error_msg = 'No suitable results were found 🙁'
                context.bot.send_message(chat_id=chat_id, text=error_msg)

            if any(key in result_dict['commands'] for key in ["vaporise", "vaporise_gif", "vaporise_gif_random", "vaporise_gif_custom"]):
                fileformat = 'wav'
            else:
                fileformat = 'mp3'

            video_info = youtubemp3.getmp3(videoid, fileformat)

            video_info['artist'] = scrape_artist_name(filtered_name2)

            if video_info['artist'] is None:
                video_info['artist'] = filtered_name2

            if video_info['track_name'] is None:
                video_info['track_name'] = scrape_song_name(filtered_name2, video_info['artist'])

            if video_info['track_name'] is None:
                video_info['track_name'] = filtered_name2

            filename = video_info["filename"]

            if any(key in result_dict['commands'] for key in ["vaporise", "vaporise_gif", "vaporise_gif_random", "vaporise_gif_custom"]):
                audiofile = filename + '.wav'
            else:
                audiofile = filename + '.mp3'

            needs_dict = command_handler.needsDictBuilder(result_dict, video_info)
            command_handler.set_active_commands(result_dict["commands"])
            command_handler.execute_commands(needs_dict, update, context, chat_id)
            context.bot.send_audio(chat_id=chat_id, audio=open(audiofile, 'rb'))
            os.remove(audiofile)
        except Exception as e:
            print(str(e))
            pass

    @classmethod
    def _greetings(cls, username: str) -> str:
        str1 = "*Hi {} 👋*\n".format(username)
        return str1

    @classmethod
    def _sendMessage(cls, context: CallbackContext, text, keyboard=None) -> None:
        sent_message = context.bot.send_message(chat_id=context.user_data[c.CHAT_ID], text=text, reply_markup=keyboard)
        context.user_data[c.MSG_ID] = sent_message.message_id

    @classmethod
    def _editMessage(cls, update: Update, text, keyboard=None) -> None:
        update.callback_query.answer()
        update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
