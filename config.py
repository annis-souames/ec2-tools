import json

CREDENTIALS = "credentials.json"

creds = json.loads(open("credentials.json", "r").read())


def get_access_token():
    return creds["access_token"]


def get_secret():
    return creds["secret"]


def get_EC2_config(path: str):
    ec2_cfg = json.loads(open(path).read())
    return ec2_cfg
