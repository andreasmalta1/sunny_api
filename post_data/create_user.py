import requests
import json

with open("login.json") as login_file:
    login_data = json.load(login_file)
    username = login_data["LOGIN"]
    password = login_data["PASSWORD"]


def create_user():

    user_url = "http://127.0.0.1:8000/api/users/"

    user_payload = {"email": username, "password": password}

    user_headers = {"Content-Type": "application/json"}

    response = requests.post(user_url, headers=user_headers, json=user_payload)
    print(response)


create_user()
