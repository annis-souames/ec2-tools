import config
import boto3


def create_instance(cfg=None):
    region = input("What region you would like to use to create the instance ? \n")
    client = boto3.client(
        "ec2",
        aws_access_key_id=config.get_access_token(),
        aws_secret_access_key=config.get_secret(),
        region_name=region,
    )
    print(client)
    pass
