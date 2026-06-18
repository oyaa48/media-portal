from django.http import HttpResponse
from dotenv import load_dotenv
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
import json
import os
import requests

load_dotenv()

def login_view(request):

    if request.method == "POST":

        response = requests.post(
            f"{os.getenv('JELLYFIN_URL')}/Users/AuthenticateByName",
            headers={
                "Authorization": (
                    'MediaBrowser Client="Media Portal", '
                    'Device="Browser", '
                    'DeviceId="media-portal", '
                    'Version="1.0"'
                )
            },
            json={
                "Username": request.POST["username"],
                "Pw": request.POST["password"],
            },
        )

        data = response.json()

        request.session["jellyfin_token"] = data["AccessToken"]
        print("LOGIN TOKEN:", data["AccessToken"])
        request.session["user_id"] = data["User"]["Id"]
        request.session["username"] = data["User"]["Name"]

        return redirect("/")

    return render(request, "jellyfin/login.html")

@csrf_exempt
def report_progress(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    data = json.loads(request.body)

    print(data)

    response = requests.post(
        f"{os.getenv('JELLYFIN_URL')}/Sessions/Playing/Progress",
        headers={
            "X-Emby-Token": request.session["jellyfin_token"],
            "Content-Type": "application/json",
        },
        json={
            "ItemId": data["item_id"],
            "MediaSourceId": data["item_id"],
            "PositionTicks": int(data["position"] * 10000000),
            "CanSeek": True,
            "IsPaused": False,
            "PlayMethod": "DirectPlay",
        },
    )

    print("Jellyfin:", response.status_code)
    print(response.text)

    return JsonResponse({"ok": True})

@csrf_exempt
def playback_started(request):
    print("PLAYBACK STARTED HIT")
    data = json.loads(request.body)

    response = requests.post(
        f"{os.getenv('JELLYFIN_URL')}/Sessions/Playing",
        headers={
            "X-Emby-Token": request.session["jellyfin_token"],
            "Content-Type": "application/json",
        },
        json={
            "ItemId": data["item_id"],
            "MediaSourceId": data["item_id"],
            "CanSeek": True,
            "IsPaused": False,
            "PlayMethod": "DirectPlay",
        },
    )

    print("PLAYING:", response.status_code)

    return JsonResponse({"ok": True})

def index(request):
    url = os.getenv("JELLYFIN_URL")

    if "jellyfin_token" not in request.session:
        return redirect("/login/")
    api_key = request.session["jellyfin_token"]

    if api_key is None:
        raise ValueError("JELLYFIN_API_KEY is not set")

    response = requests.get(
        f"{url}/Library/MediaFolders",
        headers={"X-Emby-Token": api_key},
        timeout=10,
    )

    if response.status_code == 401:
        request.session.flush()
        return redirect("/login/")

    data = response.json()

    user_id = request.session["user_id"]

    context = {
        "libraries": data["Items"],
        "JELLYFIN_URL": url,
        "api_key": api_key,
    }

    context.update(
        get_navigation_libraries(url, api_key)
    )

    context.update(
        get_continue_watching(
            url,
            api_key,
            user_id,
        )
    )

    print(request.session.get("username"))

    return render(
        request,
        "jellyfin/index.html",
        context,
    )


def library(request, library_id):
    url = os.getenv("JELLYFIN_URL")
    api_key = request.session["jellyfin_token"]

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

    if response.status_code == 401:
        request.session.flush()
        return redirect("/login/")

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

    libraries = response.json()["Items"]

    return [
        library
        for library in libraries
        if library["CollectionType"] != "playlists"
    ]


def get_navigation_libraries(url, api_key):
    return {"navigation_libraries": get_libraries(url, api_key)}


def item(request, item_id):
    url = os.getenv("JELLYFIN_URL")
    api_key = request.session["jellyfin_token"]

    if "jellyfin_token" not in request.session:
        return redirect("/login/")

    if url is None:
        raise ValueError("JELLYFIN_URL is not set")

    if api_key is None:
        raise ValueError("JELLYFIN_API_KEY is not set")

    user_id = request.session["user_id"]
    response = requests.get(
        f"{url}/Items/{item_id}",
        params={"userId": user_id},
        headers={"X-Emby-Token": api_key},
    )

    if response.status_code == 401:
        request.session.flush()
        return redirect("/login/")

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
            "ApiKey": request.session["jellyfin_token"],
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

def get_continue_watching(url, api_key, user_id):
    response = requests.get(
        f"{url}/Users/{user_id}/Items/Resume",
        headers={"X-Emby-Token": api_key},
    )

    return {
        "continue_watching": response.json()["Items"]
    }