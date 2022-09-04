import os
from abc import ABC, abstractmethod
import random
from typing import Union

from telegram import Update
from telegram.ext import CallbackContext
from scrapeutils import scraper, giphy
from vapor import vaporiser
import time


class Command(ABC):

    @abstractmethod
    def executeCommand(self, update: Update, context: CallbackContext, chat_id: Union[int, str],
                       needed_string: str = '',
                       options_list = None) -> None:
        pass


class IMG_Command(Command):

    def executeCommand(self, update: Update, context: CallbackContext, chat_id: Union[int, str],
                       needed_string: str = '',
                       options_list = None) -> None:
        try:
            context.bot.send_photo(chat_id = chat_id, photo = open(needed_string, 'rb'))
            os.remove(needed_string)
        except:
            context.bot.send_message(chat_id = chat_id, text = 'Unable to retrieve thumbnail 🙁')


class LYRICS_Command(Command):

    def executeCommand(self, update: Update, context: CallbackContext, chat_id: Union[int, str],
                       needed_string: str = '',
                       options_list = None) -> None:
        try:
            words = needed_string.split('///')
            song_info = {
                "artist": words[0],
                "title":  words[1]
            }
            lyrics = scraper.scrape_lyrics(song_info)
            context.bot.send_message(chat_id = chat_id, text = lyrics)
        except:
            context.bot.send_message(chat_id = chat_id, text = 'Unable to retrieve lyrics 🙁')


class INFO_Command(Command):

    def executeCommand(self, update: Update, context: CallbackContext, chat_id: Union[int, str],
                       needed_string: str = '',
                       options_list = None) -> None:
        try:
            info = scraper.scrape_info(needed_string)
            context.bot.send_message(chat_id = chat_id, text = info)
        except:
            try:
                info = scraper.scrape_general_info("who is " + needed_string)
                context.bot.send_message(chat_id = chat_id, text = info)
            except:
                context.bot.send_message(chat_id = chat_id, text = "Unable to retrieve info 🙁")


class VAPORAUDIO_Command(Command):

    def executeCommand(self, update: Update, context: CallbackContext, chat_id: Union[int, str],
                       needed_string: str = '',
                       options_list = None) -> None:
        audiofile = needed_string + '.wav'
        vaporised_audiofile = needed_string + "-vaporised" + ".mp3"
        argsString = "--audio" + " " + audiofile + " " + "--output" + " " + vaporised_audiofile + " "

        for opt in options_list:
            argsString = argsString + opt

        vaporiser.edit(argsString)
        context.bot.send_audio(chat_id = chat_id, audio = open(vaporised_audiofile, 'rb'))
        os.remove(vaporised_audiofile)


class VAPORGIF_Command(Command):
    def executeCommand(self, update: Update, context: CallbackContext, chat_id: Union[int, str],
                       needed_string: str = '',
                       options_list = None) -> None:
        try:
            words = needed_string.split('///')
            song_info = {
                "artist":   words[0],
                "filename": words[1]
            }
            vaporised_videofile = song_info['filename'] + "-vaporised" + ".mp4"
            artist_name = song_info["artist"]
            try:
                gif_filename = giphy.get_gif(artist_name, 0, 0)
            except IndexError:
                gif_filename = giphy.get_gif("vaporwave")

            audiofile = song_info['filename'] + '.wav'
            argsString = "--audio" + " " + audiofile + " " + "--gif" + " " + gif_filename + " " + "--output" + " " + vaporised_videofile
            vaporiser.edit(argsString)
            time.sleep(5)
            context.bot.send_video(chat_id = chat_id, video = open(vaporised_videofile, 'rb'),
                                   supports_streaming = True)
            os.remove(vaporised_videofile)

        except:
            context.bot.send_message(chat_id = chat_id, text = "Unable to generate vaporised video, no sad vibes🙁")


class VAPORGIF_RANDOM_Command(Command):
    def executeCommand(self, update: Update, context: CallbackContext, chat_id: Union[int, str],
                       needed_string: str = '',
                       options_list = None) -> None:
        try:

            words = needed_string.split('///')
            song_info = {
                "artist":   words[0],
                "filename": words[1]
            }
            vaporised_videofile = song_info['filename'] + "-vaporised" + ".mp4"
            artist_name = song_info["artist"]
            selection = ['vaporwave', 'sad simpson', artist_name]
            selected = random.choice(selection)
            if selected == "sad simpson":
                gif_filename = "sad_simpson.gif"
                scraper.scrape_gif("https://i.giphy.com/media/dACqNmvAfY12M/giphy.webp", gif_filename)
            else:
                gif_filename = giphy.get_gif("vaporwave")

            audiofile = song_info['filename'] + '.wav'
            argsString = "--audio" + " " + audiofile + " " + "--gif" + " " + gif_filename + " " + "--output" + " " + vaporised_videofile
            vaporiser.edit(argsString)
            time.sleep(5)
            context.bot.send_video(chat_id = chat_id, video = open(vaporised_videofile, 'rb'),
                                   supports_streaming = True)
            os.remove(vaporised_videofile)

        except:
            context.bot.send_message(chat_id = chat_id, text = "Unable to generate vaporised video, no sad vibes🙁")


class VAPORGIF_CUSTOM_Command(Command):

    def executeCommand(self, update: Update, context: CallbackContext, chat_id, needed_string = '',
                       options_list = None) -> None:
        try:
            words = needed_string.split('///')
            song_info = {
                "filename":        words[0],
                'custom_gif_name': words[1]
            }
            vaporised_videofile = song_info['filename'] + "-vaporised" + ".mp4"
            try:
                gif_filename = giphy.get_gif(song_info['custom_gif_name'], 0, 0)
            except IndexError:
                gif_filename = giphy.get_gif("vaporwave")

            audiofile = song_info['filename'] + '.wav'
            argsString = "--audio" + " " + audiofile + " " + "--gif" + " " + gif_filename + " " + "--output" + " " + vaporised_videofile
            vaporiser.edit(argsString)
            time.sleep(5)
            context.bot.send_video(chat_id = chat_id, video = open(vaporised_videofile, 'rb'),
                                   supports_streaming = True)
            os.remove(vaporised_videofile)

        except:
            context.bot.send_message(chat_id = chat_id, text = "Unable to generate vaporised video, no sad vibes🙁")
