
import boto3
import config  # Assuming you have a 'config' module with access token, secret, and region
from datetime import datetime, timedelta
from prettytable import PrettyTable

# Create a CloudWatch client
client = boto3.client(
    'cloudwatch',
    aws_access_key_id=config.get_access_token(),
    aws_secret_access_key=config.get_secret(),
    region_name="eu-north-1"
)

# List of EC2 instance IDs
instance_ids = ['i-04711786827346b8f', 'i-063fd105a5fd4eb97', 'i-088155b190f631489', 'i-062e96d9ad11d1c7a', 'i-049490b7fec2132a7']

# Metrics to collect
metrics_to_collect = ['CPUUtilization', 'EBSReadOps', 'EBSWriteBytes', 'NetworkIn', 'NetworkOut']


# Create a table
table = PrettyTable()
table.field_names = ['Instance ID'] + metrics_to_collect

# Collect metrics for each instance
for instance_id in instance_ids:
    row_data = [instance_id]

    for metric_name in metrics_to_collect:
        metric_data = client.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName=metric_name,
            Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
            StartTime=(datetime.utcnow() - timedelta(days=1)).isoformat(),
            EndTime=datetime.utcnow().isoformat(),
            Period=300,  # Adjust the period as needed
            Statistics=['Average', 'Sum']
        )

        # Extract the average value from the metric data
        datapoints = metric_data.get('Datapoints', [])
        average_value = datapoints[0]['Average'] if datapoints else 'N/A'
        row_data.append(average_value)

    # Add the row to the table
    table.add_row(row_data)

# Print the table
print(table)