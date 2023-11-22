import argparse
import boto3

def create_instance(ec2, ami_id, instance_type, key_name):
    print("Creating EC2 instance...")
    response = ec2.run_instances(
        ImageId=ami_id,
        InstanceType=instance_type,
        KeyName=key_name,
        MinCount=1,
        MaxCount=1
    )
    instance_id = response['Instances'][0]['InstanceId']
    print(f"Instance {instance_id} created successfully.")

def list_instances(ec2):
    print("Listing EC2 instances...")
    instances = ec2.describe_instances()
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            print(f"ID: {instance['InstanceId']}, State: {instance['State']['Name']}")

def terminate_instance(ec2, instance_id):
    print(f"Terminating instance {instance_id}...")
    ec2.terminate_instances(InstanceIds=[instance_id])
    print(f"Instance {instance_id} terminated successfully.")

def main():
    parser = argparse.ArgumentParser(description="Manage EC2 instances")
    parser.add_argument("--access-key", required=True, help="AWS Access Key ID")
    parser.add_argument("--secret-key", required=True, help="AWS Secret Access Key")
    parser.add_argument("--region", required=True, help="AWS Region")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    create_parser = subparsers.add_parser("create", help="Create a new EC2 instance")
    create_parser.add_argument("--ami-id", required=True, help="AMI ID")
    create_parser.add_argument("--instance-type", required=True, help="Instance type")
    create_parser.add_argument("--key-name", required=True, help="Key pair name")

    list_parser = subparsers.add_parser("list", help="List all EC2 instances")

    terminate_parser = subparsers.add_parser("terminate", help="Terminate an EC2 instance")
    terminate_parser.add_argument("instance_id", help="ID of the instance to terminate")

    args = parser.parse_args()

    ec2 = boto3.client(
        'ec2',
        aws_access_key_id=args.access_key,
        aws_secret_access_key=args.secret_key,
        region_name=args.region
    )

    if args.command == "create":
        create_instance(ec2, args.ami_id, args.instance_type, args.key_name)
    elif args.command == "list":
        list_instances(ec2)
    elif args.command == "terminate":
        terminate_instance(ec2, args.instance_id)
    else:
        print("Invalid command. Use --help for usage information.")

if __name__ == "__main__":
    main()
