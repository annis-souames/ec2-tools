import json

CREDENTIALS = "credentials.json"

creds = json.loads(open("credentials.json", "r").read())


def get_access_token():
    return creds["access_token"]


def get_secret():
    return creds["secret"]
