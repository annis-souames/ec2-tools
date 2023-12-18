import config
import boto3


# Method for creating an instance
def create_instance(region="us-west-1", cfg_path=None):
    client = boto3.client(
        "ec2",
        aws_access_key_id=config.get_access_token(),
        aws_secret_access_key=config.get_secret(),
        region_name=region,
    )
    ec2_cfg = config.get_EC2_config(cfg_path)
    client.run_instances(
        BlockDeviceMappings=[
            {
                "DeviceName": "/dev/sdh",
                "Ebs": {
                    "VolumeSize": ec2_cfg["volume"],
                },
            },
        ],
        ImageId=ec2_cfg["ami"],
        InstanceType=ec2_cfg["type"],
        MaxCount=1,
        MinCount=1,
    )
    print("EC2 was created successfully")
    return None


def delete_instance(instance_id, region="us-west-1"):
    client = boto3.client(
        "ec2",
        aws_access_key_id=config.get_access_token(),
        aws_secret_access_key=config.get_secret(),
        region_name=region,
    )
    # Specify the instance ID to be terminated
    instances_to_terminate = [instance_id]

    # Terminate the EC2 instances
    try:
        response = client.terminate_instances(InstanceIds=instances_to_terminate)
        print(f"Instance {instance_id} termination response: {response}")
    except Exception as e:
        print(f"Error terminating instance {instance_id}: {e}")


def list_regions():
    # Retrieves all regions/endpoints that work with EC2
    ec2 = boto3.client(
        "ec2",
        aws_access_key_id=config.get_access_token(),
        aws_secret_access_key=config.get_secret(),
        region_name="us-west-1",
    )
    regs = ec2.describe_regions()
    # Retrieves availability zones only for region of the ec2 object
    az = ec2.describe_availability_zones()
    return {"regions": regs["Regions"], "zones": az["AvailabilityZones"]}


def list_instances(region: str):
    # Retrieve information about instances
    ec2 = boto3.client(
        "ec2",
        aws_access_key_id=config.get_access_token(),
        aws_secret_access_key=config.get_secret(),
        region_name=region,
    )
    response = ec2.describe_instances()
    instances = []

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instances.append(
                {
                    "InstanceId": instance["InstanceId"],
                    "State": instance["State"]["Name"],
                    "InstanceType": instance["InstanceType"],
                    "LaunchTime": instance["LaunchTime"].strftime("%Y-%m-%d %H:%M:%S"),
                    "PublicIpAddress": instance.get("PublicIpAddress", "N/A"),
                    "PrivateIpAddress": instance.get("PrivateIpAddress", "N/A"),
                }
            )

    return instances


def get_status(instance_id, region="us-west-1"):
    ec2 = boto3.client(
        "ec2",
        aws_access_key_id=config.get_access_token(),
        aws_secret_access_key=config.get_secret(),
        region_name=region,
    )
    # Retrieve the status of the specified instance
    response = ec2.describe_instance_status(
        InstanceIds=[instance_id], IncludeAllInstances=True
    )

    # Check if the instance status is available
    if "InstanceStatuses" in response and response["InstanceStatuses"]:
        instance_status = response["InstanceStatuses"][0]["InstanceState"]["Name"]
        return instance_status
    else:
        return "N/A"


# create_instance("ap-northeast-1", "templates/ex1.json")
# delete_instance("i-0d994367b97e88132", "ap-northeast-1")
