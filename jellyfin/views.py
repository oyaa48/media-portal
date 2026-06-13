from django.shortcuts import render
from django.http import HttpResponse
from dotenv import load_dotenv
import os
import requests

load_dotenv()

def index(request):
    url = os.getenv("JELLYFIN_URL")
    api_key = os.getenv("JELLYFIN_API_KEY")

    response = requests.get(
            f"{url}/Library/MediaFolders",
            headers={"X-Emby-Token": api_key},
            timeout=10,

    )

    data = response.json()

    html = "<h1>Gectube</h1><ul>"

    for item in data["Items"]:
        html += f"<li>{item['Name']}</li>"

    html += "</ul>"

    return HttpResponse(html)
