import os
import requests
from dotenv import load_dotenv

load_dotenv()


def get_access_token():
    payload = {"username": os.getenv("BG_USERNAME"), "email": os.getenv("BG_EMAIL"),
               "password": os.getenv("BG_PASSWORD")}
