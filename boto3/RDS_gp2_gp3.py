import boto3 

regions = ['eu-west-1']
session = boto3.Session()

client = session.client('rds', 'eu-west-1')
response = client.describe_db_instances()
for i in response['DBInstances']:
    InstanceIdentifier = i['DBInstanceIdentifier']
    storagetype = i['StorageType']
    Storage = i['AllocatedStorage']
    
    if storagetype == 'gp2' or storagetype != 'aurora':
        try:
            if Storage < 20: #gp3 minimum size is 20GB
                StorageAllocated = 20
            else:
                StorageAllocated = Storage
            modify = client.modify_db_instance(
                    ApplyImmediately=True,
                    DBInstanceIdentifier=InstanceIdentifier,
                    StorageType='gp3',
                    AllocatedStorage = StorageAllocated
                )     
            print(modify)
        except:
            print('Error')
            continue
