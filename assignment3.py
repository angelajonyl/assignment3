# COSC 1104 – Assignment 3
# Angela Reyes

import boto3
from datetime import datetime, timedelta

INSTANCE_ID = 'i-0b6e5056448694fff'
REGION = 'us-west-2'


session = boto3.Session(profile_name="default")
cloudwatch = session.client('cloudwatch', region_name=REGION)

def get_cpu_utilization():
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=1)  # 1 hr before current time

    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[{'Name': 'InstanceId', 'Value': INSTANCE_ID}],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,  # 5 minutes
        Statistics=['Average']
    )

    if 'Datapoints' in response and response['Datapoints']:
        print(f"CPU Utilization for instance {INSTANCE_ID}:")
        sorted_datapoints = sorted(response['Datapoints'], key=lambda x: x['Timestamp'])
        for datapoint in sorted_datapoints:
            print(f"Time: {datapoint['Timestamp']}, CPU Utilization: {datapoint['Average']:.2f}%")
    else:
        print(f"No data points found for instance {INSTANCE_ID} in the last hour.")

if __name__ == "__main__":
    get_cpu_utilization()