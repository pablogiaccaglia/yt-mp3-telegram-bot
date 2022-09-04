from telegram import Update
from telegram.ext import CallbackContext
from commands import command


class CommandHandler:

    def __init__(self):

        self._commands = {
            "img": command.IMG_Command(),
            "lyrics": command.LYRICS_Command(),
            "info": command.INFO_Command(),
            "vaporise": command.VAPORAUDIO_Command(),
            "vaporise_gif": command.VAPORGIF_Command(),
            "vaporise_gif_custom": command.VAPORGIF_CUSTOM_Command(),
            "vaporise_gif_random": command.VAPORGIF_RANDOM_Command()
        }

        self._active_commands = {
            "img": False,
            "lyrics": False,
            "info": False,
            "vaporise": False,
            "vaporise_gif": False,
            "vaporise_gif_custom": False,
            "vaporise_gif_random": False
        }

    def set_active_commands(self, activation_list: list) -> None:

        for c in activation_list:
            if c in self._active_commands:
                self._active_commands[c] = True

    def _reset_active_commands(self) -> None:
        self._active_commands = self._active_commands.fromkeys(self._active_commands, False)

    def execute_commands(self, needs: dict[str, str], update: Update, context: CallbackContext, chat_id) -> None:
        for the_key, the_value in self._active_commands.items():
            if the_value:
                needed_str = needs[the_key]
                self._commands[the_key].executeCommand(update = update,
                                                       context = context,
                                                       chat_id = chat_id,
                                                       needed_string = needed_str,
                                                       options_list = needs['optional_audio_options_list'])

    @classmethod
    def needsDictBuilder(cls, result_dict: dict, video_info: dict):
        commands_names = result_dict["commands"]
        needsDict = {}
        filename = video_info['filename']
        needsDict['optional_audio_options_list'] = result_dict['optional_audio_options']
        for c in commands_names:
            if c == "img":
                needsDict[c] = filename + '.jpg'
            if c == "lyrics":
                needsDict[c] = video_info["artist"] + "///" + video_info["track_name"]
            if c == "info":
                needsDict[c] = video_info["artist"]
            if c == "vaporise":
                needsDict[c] = filename
            if c == "vaporise_gif":
                needsDict[c] = video_info["artist"] + "///" + filename
            if c == "vaporise_gif_custom":
                needsDict[c] = filename + result_dict['custom_gif_name']
            if c == "vaporise_gif_random":
                needsDict[c] = video_info["artist"] + "///" + filename
        return needsDict

    # self.__reset_active_commands()
