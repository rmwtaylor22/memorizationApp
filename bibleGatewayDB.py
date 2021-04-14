import os
import requests
from dotenv import load_dotenv

load_dotenv()


def get_access_token():
    payload = {"username": os.getenv("BG_USERNAME"), "email": os.getenv("BG_EMAIL"),
               "password": os.getenv("BG_PASSWORD")}
    auth = requests.post(url="https://api.biblegateway.com/3/user/authenticate", data=payload)
    data = auth.json()
    access_token = data["authentication"]["access_token"]

    return access_token

def get_translations():
    access_token = get_access_token()
    url = "".join([os.getenv("BG_BASE_URL"), "?access_token=", access_token])

    request = requests.get(url=url)
    data = request.json()
    translations = []
    for i in data["data"]:
        translations.append(i["translation"])

    return translations

def get_content(osis_ref, translation):

    access_token = get_access_token()
    if translation not in get_translations():
        print("You do not have permission to access the " + translation + "translation")
        return

    url = "".join([os.getenv("BG_BASE_URL"), '/'])

    if len(osis_ref) == 1:
        url = "".join([url, osis_ref, '/'])
    else:
        for verse in osis_ref:
            url = "".join([url, verse, "%2C20"])

        url = "".join([url, "/"])
    url = "".join([url, translation, '?access_token=', access_token])

    request = requests.get(url=url)
    data = request.json()
    if len(osis_ref) == 1:
        verse = data["data"][0]["passages"][0]["content"]
    else:
        verse = []
        for i in range(len(osis_ref)):
            verse.append(data["data"][i]["passages"][0]["content"])

    return verse

# gen.1.1

