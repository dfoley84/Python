import boto3 
import os

region = ['eu-west-1','us-east-1','us-west-2','ap-southeast-2']

def handler():
    for i in region:
        rds = boto3.client('rds', region_name=i)
        #get All RDS instances
        response = rds.describe_db_instances()
        for instance in response['DBInstances']:
            instance_name = instance['DBInstanceIdentifier']
            instance_type = instance['DBInstanceClass']
            if instance_type.startswith('db.t3.'):
                new_instance_type = instance_type.replace('db.t3.', 'db.t4g.')
                rds.modify_db_instance(
                    DBInstanceIdentifier=instance_name, 
                    DBInstanceClass=new_instance_type,
                    ApplyImmediately=False
                    )
                print(f"Instance {instance_name} Will be modified to {new_instance_type} At the next maintenance window")
if __name__ == '__main__':
    handler()
