import requests
import gspread
from login import login


def update_quotes():
    sa = gspread.service_account(filename="service_account.json")
    sh = sa.open("Sunny Quotes")
    whs = sh.worksheet("Update")
    values = whs.get_all_values()
    header_column = values[0]
    header_column.pop(0)
    values.pop(0)

    access_token = login()
    post_headers = {"Authorization": "Bearer " + access_token}

    base_url = "https://itssunnyapi.com/api/quotes/"

    for row in values:
        post_payload = {}
        post_id = row[0]
        update_url = base_url + post_id
        row.pop(0)

        for index, column in enumerate(row):
            post_payload[header_column[index]] = column
        response = requests.put(update_url, headers=post_headers, json=post_payload)

        print(response)


update_quotes()
