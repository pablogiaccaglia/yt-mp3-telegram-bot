# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from utils import utility
import yt_dlp

def getmp3(videoid: str, audioformat: str) -> dict:
    downloadurl = 'https://www.youtube.com/watch?v=' + videoid
    ydl_opts0 = {
        'nocheckcertificate': True,
        'addmetadata':        True,
    }

    with yt_dlp.YoutubeDL(ydl_opts0) as ydl0:
        info_dict = ydl0.extract_info(downloadurl, download = False)
        video_title = info_dict.get('title', None)
        artist = info_dict.get('artist', None)
        track_name = info_dict.get('track', None)
        clean_video_title = utility.slugify(video_title)

    ydl_opts = {
        'writethumbnail':     True,
        'nocheckcertificate': True,
        'format':             'bestaudio/best',
        'postprocessors':     [{
            'key':              'FFmpegExtractAudio',
            'preferredcodec':   audioformat,
            'preferredquality': '192',
        }],
        'outtmpl':            clean_video_title + '.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([downloadurl])

    info_dict = {
        "filename":   clean_video_title,
        "artist":     artist,
        "track_name": track_name
    }

    return info_dict
