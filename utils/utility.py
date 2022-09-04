import unicodedata
import re
from typing import Optional


def slugify(value: str, allow_unicode: bool = False) -> str:
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r"[-\s]+", '-', value).strip('-_')


def parse_options(string: str) -> dict:
    result = {
        "filename": string,
        "commands": [],
        "optional_audio_options": []

    }

    string_clean = string

    print(string_clean)

    if "-t" in string_clean:
        string_clean = string.replace('-t', '')
        result['optional_audio_options'].append("--tremolo")

    if "-p" in string_clean:
        (string_clean := string_clean.replace('-p', '')) if string_clean != '' else (
            string_clean := string.replace('-p', ''))
        result['optional_audio_options'].append("--phaser")

    if "-c" in string_clean:
        (string_clean := string_clean.replace('-c', '')) if string_clean != '' else (
            string_clean := string.replace('-c', ''))
        result['optional_audio_options'].append("--compand")

    if "-img" in string_clean:
        (string_clean := string_clean.replace('-img', '')) if string_clean != '' else (
            string_clean := string.replace('-img', ''))
        result['commands'].append("img")

    if "-l" in string_clean:
        (string_clean := string_clean.replace('-l', '')) if string_clean != '' else (
            string_clean := string.replace('-l', ''))
        result['commands'].append("lyrics")

    if "-i" in string_clean:
        (string_clean := string_clean.replace('-i', '')) if string_clean != '' else (
            string_clean := string.replace('-i', ''))
        result['commands'].append("info")

    if "-vgr" in string_clean:
        (string_clean := string_clean.replace('-vgr', '')) if string_clean != '' else (
            string_clean := string.replace('-vgr', ''))
        result['commands'].append("vaporise_gif_random")

    if "-vgc" in string_clean:
        custom_gif_name = get_first_word_after_token(string = string_clean, word = '-vgr')
        (string_clean := string_clean.replace('-vgr' + " " + custom_gif_name, '')) if string_clean != '' else (
            string_clean := string.replace('-vgr' + " " + custom_gif_name, ''))
        result['commands'].append("vaporise_gif_custom")
        result['custom_gif_name'] = custom_gif_name
        print(custom_gif_name)

    if "-vg" in string_clean:
        (string_clean := string_clean.replace('-vg', '')) if string_clean != '' else (
            string_clean := string.replace('-vg', ''))
        result['commands'].append("vaporise_gif")

    if "-v" in string_clean:
        (string_clean := string_clean.replace('-v', '')) if string_clean != '' else (
            string_clean := string.replace('-v', ''))
        result['commands'].append("vaporise")

    if string_clean == string:
        result['filename'] = string
    else:
        result['filename'] = string_clean

    print(result)

    return result


def get_first_word_after_token(string: str, word: str) -> Optional[str]:
    try:
        second_half = string.split(word)
        first_word = second_half(" ")[0]
        return first_word
    except:
        return None
