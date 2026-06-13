from django.shortcuts import render
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

    return render(
        request,
        "jellyfin/index.html",
        {
            "libraries": data["Items"],
        },
    )


def library(request, library_id):
    url = os.getenv("JELLYFIN_URL")
    api_key = os.getenv("JELLYFIN_API_KEY")

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
    if data["Items"]:
        print(data["Items"][0])

    return render(
        request,
        "jellyfin/library.html",
        {
            "items": data["Items"],
            "library_name": library_name,
            "JELLYFIN_URL": url,
            "api_key": api_key,
        },
    )


def item(request, item_id):
    url = os.getenv("JELLYFIN_URL")
    api_key = os.getenv("JELLYFIN_API_KEY")

    if url is None:
        raise ValueError("JELLYFIN_URL is not set")

    if api_key is None:
        raise ValueError("JELLYFIN_API_KEY is not set")

    response = requests.get(
        f"{url}/Items",
        params={"Ids": item_id},
        headers={"X-Emby-Token": api_key},
    )

    data = response.json()

    return render(
        request,
        "jellyfin/item.html",
        {
            "item": data["Items"][0],
            "JELLYFIN_URL": url,
            "api_key": api_key,
        },
    )
