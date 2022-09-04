# -*- coding: utf-8 -*-

import urllib.request
from typing import Optional

from lyricsgenius import Genius
import wikipedia
import googleapiclient.discovery
import os
from serpapi import GoogleSearch
import requests


def scrape_video_ID(name: str) -> str:
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    max_results = 10
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyCCUfopny3vPgyeYmPMHxL5oCIytvMd3zw"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.search().list(
        part="snippet",
        channelType="any",
        maxResults=max_results,
        q=name
    )

    response = request.execute()

    # default video id to avoid errors and warnings
    videoID = "dQw4w9WgXcQ"

    # loop through results to skip channel / playlists results
    for i in range(max_results):
        try:
            videoID = response['items'][i]['id']['videoId']
            break
        except ValueError:
            pass

    return videoID


def scrape_thumbnail(videoID: str, filename: str) -> None:
    source = "https://i.ytimg.com/vi/" + videoID + "/maxresdefault.jpg"

    # Using pathlib, specify where the image is to be saved

    # Form a full image path by joining the path to the
    # images' new name

    # "/home/User/Downloads/new-image.png"

    # Using "urlretrieve()" from urllib.request save the image
    urllib.request.urlretrieve(source, filename + '.jpg')

    # urlretrieve() takes in 2 arguments
    # 1. The URL of the image to be downloaded
    # 2. The image new name after download. By default, the image is saved
    #    inside your current working directory


def scrape_lyrics(song_info: dict[str, str]) -> str:
    artist_name = song_info["artist"]
    genius = Genius("j0A7T1ydXf3ZFekAd5PEoLdzef2NzdMRKY5_d2Cr2zD3Xudr3YbVwNB2RSEMPDai")
    song = genius.search_song(song_info["title"], artist=artist_name)
    return song.lyrics


def scrape_info(name: str) -> str:
    info = wikipedia.summary(name, auto_suggest=False)
    return info


def scrape_artist_name(song_name: str) -> Optional[str]:
    genius = Genius("j0A7T1ydXf3ZFekAd5PEoLdzef2NzdMRKY5_d2Cr2zD3Xudr3YbVwNB2RSEMPDai")
    song = genius.search_song(song_name)
    if song is None:
        return None
    return song.artist


def scrape_song_name(user_song_name: str, artist_name: str = None) -> Optional[str]:
    genius = Genius("j0A7T1ydXf3ZFekAd5PEoLdzef2NzdMRKY5_d2Cr2zD3Xudr3YbVwNB2RSEMPDai")
    if artist_name is None:
            song = genius.search_song(user_song_name)
    else:
            song = genius.search_song(user_song_name, artist=artist_name)

    if song is None:
        return None

    return song.title


def scrape_general_info(query: str) -> str:
    params = {
        "q": query,
        "hl": "en",
        "gl": "us",
        "google_domain": "google.com",
        "api_key": "ea9bc5a5acc4eca45647457c08dcd413aebb3e98cf3655027d9877334e29cc3a"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    try:
        summary = results["answer_box"]['snippet']
    except:
        summary = results["knowledge_graph"]["description"]
        pass

    return summary


def scrape_gif(gif_url: str, gif_filename: str) -> None:
    with open(gif_filename, 'wb') as f:
        f.write(requests.get(gif_url).content)
