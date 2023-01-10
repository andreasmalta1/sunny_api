import requests
import json

with open("login.json") as login_file:
    login_data = json.load(login_file)
    username = login_data["LOGIN"]
    password = login_data["PASSWORD"]


def login():

    login_url = "https://itssunnyapi.com/api/login"
    login_payload = {"username": username, "password": password}

    login_response = requests.post(login_url, data=login_payload)
    access_token = login_response.json()["access_token"]

    return access_token
