from django.shortcuts import render
from django.http import HttpResponse
from dotenv import load_dotenv
import os
import requests

load_dotenv()


def index(request):
    url = os.getenv("JELLYFIN_URL")
    api_key = os.getenv("JELLYFIN_API_KEY")

    if api_key is None:
        raise ValueError("JELLYFIN_API_KEY is not set")

    response = requests.get(
        f"{url}/Library/MediaFolders",
        headers={"X-Emby-Token": api_key},
        timeout=10,
    )

    data = response.json()

    context = {
        "libraries": data["Items"],
    }

    context.update(get_navigation_libraries(url, api_key))

    return render(
        request,
        "jellyfin/index.html",
        context,
    )


def library(request, library_id):
    url = os.getenv("JELLYFIN_URL")
    api_key = os.getenv("JELLYFIN_API_KEY")

    if url is None:
        raise ValueError("JELLYFIN_URL is not set")

    if api_key is None:
        raise ValueError("JELLYFIN_API_KEY is not set")

    response = requests.get(
        f"{url}/Items",
        params={
            "ParentId": library_id,
        },
        headers={"X-Emby-Token": api_key},
        timeout=10,
    )

    data = response.json()

    library_name = request.GET.get("name", "Library")

    context = {
        "items": data["Items"],
        "library_name": library_name,
        "JELLYFIN_URL": url,
        "api_key": api_key,
    }

    context.update(get_navigation_libraries(url, api_key))

    return render(
        request,
        "jellyfin/library.html",
        context,
    )


def get_libraries(url, api_key):
    response = requests.get(
        f"{url}/Library/MediaFolders",
        headers={
            "X-Emby-Token": api_key,
        },
    )

    return response.json()["Items"]


def get_navigation_libraries(url, api_key):
    return {"navigation_libraries": get_libraries(url, api_key)}


def item(request, item_id):
    url = os.getenv("JELLYFIN_URL")
    api_key = os.getenv("JELLYFIN_API_KEY")

    if url is None:
        raise ValueError("JELLYFIN_URL is not set")

    if api_key is None:
        raise ValueError("JELLYFIN_API_KEY is not set")

    user_id = get_user_id(url, api_key)

    response = requests.get(
        f"{url}/Items/{item_id}",
        params={"userId": user_id},
        headers={"X-Emby-Token": api_key},
    )

    data = response.json()

    subtitle_streams = [
        stream for stream in data["MediaStreams"]
        if stream["Type"] == "Subtitle"
    ]

    LANGUAGES = {
        "eng": "English",
        "en": "English",

        "tur": "Turkish",
        "tr": "Turkish",

        "ces": "Czech",
        "cze": "Czech",
        "cs": "Czech",

        "deu": "German",
        "ger": "German",
        "de": "German",

        "fra": "French",
        "fre": "French",
        "fr": "French",

        "spa": "Spanish",
        "es": "Spanish",

        "ita": "Italian",
        "it": "Italian",

        "por": "Portuguese",
        "pt": "Portuguese",

        "rus": "Russian",
        "ru": "Russian",

        "ukr": "Ukrainian",
        "uk": "Ukrainian",

        "pol": "Polish",
        "pl": "Polish",

        "nld": "Dutch",
        "dut": "Dutch",
        "nl": "Dutch",

        "swe": "Swedish",
        "sv": "Swedish",

        "nor": "Norwegian",
        "no": "Norwegian",

        "dan": "Danish",
        "da": "Danish",

        "fin": "Finnish",
        "fi": "Finnish",

        "hun": "Hungarian",
        "hu": "Hungarian",

        "ron": "Romanian",
        "rum": "Romanian",
        "ro": "Romanian",

        "ell": "Greek",
        "gre": "Greek",
        "el": "Greek",

        "bul": "Bulgarian",
        "bg": "Bulgarian",

        "srp": "Serbian",
        "sr": "Serbian",

        "hrv": "Croatian",
        "hr": "Croatian",

        "slk": "Slovak",
        "slo": "Slovak",
        "sk": "Slovak",

        "slv": "Slovenian",
        "sl": "Slovenian",

        "jpn": "Japanese",
        "ja": "Japanese",

        "kor": "Korean",
        "ko": "Korean",

        "zho": "Chinese",
        "chi": "Chinese",
        "zh": "Chinese",

        "ara": "Arabic",
        "ar": "Arabic",

        "heb": "Hebrew",
        "he": "Hebrew",

        "hin": "Hindi",
        "hi": "Hindi",

        "tha": "Thai",
        "th": "Thai",

        "vie": "Vietnamese",
        "vi": "Vietnamese",

        "ind": "Indonesian",
        "id": "Indonesian",

        "msa": "Malay",
        "may": "Malay",
        "ms": "Malay",
    }

    for subtitle in subtitle_streams:
        subtitle["Label"] = LANGUAGES.get(
            subtitle.get("Language"),
            subtitle.get("DisplayTitle"),
        )

    subtitle["Label"] = LANGUAGES.get(
        subtitle.get("Language", "").lower(),
        subtitle.get("DisplayTitle", "Subtitles"),
    )

    context = {
        "item": data,
        "JELLYFIN_URL": url,
        "api_key": api_key,
        "subtitle_streams": subtitle_streams,
    }

    context.update(get_navigation_libraries(url, api_key))

    return render(
        request,
        "jellyfin/item.html",
        context,
    )

def ticks_to_vtt(ticks):
    total_seconds = ticks / 10000000

    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    milliseconds = int((total_seconds % 1) * 1000)

    return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"

def subtitle(request, item_id, stream_index):
    response = requests.get(
        f"{os.getenv('JELLYFIN_URL')}/Videos/{item_id}/{item_id}/Subtitles/{stream_index}/0/Stream.js",
        params={
            "ApiKey": os.getenv("JELLYFIN_API_KEY"),
        },
    )
    data = response.json()
    vtt = "WEBVTT\n\n"

    for event in data["TrackEvents"]:
        start = ticks_to_vtt(event["StartPositionTicks"])
        end = ticks_to_vtt(event["EndPositionTicks"])

        vtt += f"{start} --> {end}\n"
        vtt += event["Text"] + "\n\n"

    return HttpResponse(
        vtt,
        content_type="text/vtt",
    )

def get_user_id(url, api_key):
    response = requests.get(
        f"{url}/Users",
        headers={"X-Emby-Token": api_key},
    )

    users = response.json()
    return users[0]["Id"]
