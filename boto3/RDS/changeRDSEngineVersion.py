import boto3 
import os

region = ['eu-west-1','us-east-1','us-west-2','ap-southeast-2']

def handler():
    for i in region:
        rds = boto3.client('rds', region_name=i)
        response = rds.describe_db_instances()
        for instance in response['DBInstances']:
            instance_name = instance['DBInstanceIdentifier']
            instance_type = instance['DBInstanceClass']
            instance_engine = instance['Engine']
            EngineVersion = instance['EngineVersion']
            if instance_engine == 'mysql' and EngineVersion != '8.0.40':
                rds.modify_db_instance(
                    DBInstanceIdentifier=instance_name, 
                    EngineVersion='8.0.40',
                    ApplyImmediately=True
                )
                print (f"Instance {instance_name} is being updated to MySQL 8.0.40")
if __name__ == '__main__':
    handler()
