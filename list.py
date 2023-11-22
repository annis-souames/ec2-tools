import boto3

def list_instance_regions():
    # Use the default session
    session = boto3.session.Session()

    # Get the current region
    current_region = session.region_name
    print(f"Current region: {current_region}")

    # Create an EC2 client in the current region
    ec2 = boto3.client('ec2', region_name=current_region)

    # Describe all instances in the current region
    instances = ec2.describe_instances()

    # Extract unique regions from the instances
    regions = set()
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            regions.add(instance['Placement']['AvailabilityZone'][:-1])  # Remove the trailing letter from the availability zone

    print("Regions of EC2 instances:")
    for region in regions:
        print(region)

if __name__ == "__main__":
    list_instance_regions()
