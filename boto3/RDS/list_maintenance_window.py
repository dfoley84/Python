import boto3

region = ['eu-west-1','us-east-1','us-west-2','ap-southeast-2']

def handler():
    for i in region:
        rds = boto3.client('rds', region_name=i)
        response = rds.describe_db_instances()
        print(f"---Region: {i}---")
        for instance in response['DBInstances']:
            instance_name = instance['DBInstanceIdentifier']
            maintenance_window = instance['PreferredMaintenanceWindow']
            print(f"Instance: {instance_name}, Maintenance Window: {maintenance_window}")

if __name__ == '__main__':
    handler()
