import boto3
import datetime


LaunchAge = 30

def days_old(date):
    date_obj = date.replace(tzinfo=None)
    diff = datetime.datetime.now() - date_obj
    return diff.days

ec2 = boto3.client('ec2')
instance = ec2.describe_instances()
for i in instance['Reservations']:
    for instance in i["Instances"]:
        instance_id = instance["InstanceId"]
        LaunchDate = instance['LaunchTime']

        day_old = days_old(LaunchDate) # Get Date from Launch

        if day_old > LaunchAge:
          response = ec2.terminate_instance(InstanceIds=[instance_id])
          print(response)

