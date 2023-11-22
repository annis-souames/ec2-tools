import boto3
import config
import json

region = input("Enter Region \n")
ec2 = boto3.client(
    "ec2",
    aws_access_key_id=config.get_access_token(),
    aws_secret_access_key=config.get_secret(),
    region_name=region)


# Retrieves all regions/endpoints that work with EC2
response = ec2.describe_regions()
regions = response['Regions']

# Print the list of regions and their endpoints
print("Regions and Endpoints that work with EC2:")
for region in regions:
    print(f"Region: {region['RegionName']}, Endpoint: {region['Endpoint']}")

# Retrieves availability zones only for the region of the ec2 object
response = ec2.describe_availability_zones()
availability_zones = response['AvailabilityZones']
