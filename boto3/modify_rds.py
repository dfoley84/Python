import boto3
import os
import datetime
import hvac

#Login to Vault
Region = input('Enter the region: ')
Environment = input('Enter Environment (Dev, UAT, Prd): ')
client = hvac.Client(url='http://localhost:8200',token= os.environ['VAULT_TOKEN'])
secret = client.read_secret_version(path='aws/region/' + Environment)
aws_access_key_id = secret['data']['aws_access_key_id']
aws_secret_access_key = secret['data']['aws_secret_access_key']



session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=Region
)

client = session.client('rds')
DatabaseName = input("Enter the Database Name: ")
DBIncrease = int(input("Enter the DB Increase GB: "))

def DescribeDBInstances():
    response = client.describe_db_instances(
        DBInstanceIdentifier=DatabaseName
    )
    for i in response['DBInstances']:
        DescribeDBInstances.capacity = i['AllocatedStorage']
        Status = i['DBInstanceStatus']
        InstanceType = i['DBInstanceClass']

    print(
        'The capacity of the RDS instance is: ' + str( DescribeDBInstances.capacity) + 'GB' + '\n' +
        'The status of the RDS instance is: ' + Status + '\n' +
        'The instance type of the RDS instance is: ' + InstanceType + '\n'
        )

def createbackup():
    print(''' ---------------------------------------- \n 
              Creating a backup of the RDS instance... \n 
              ---------------------------------------- ''')

    response = client.create_db_snapshot(
        DBSnapshotIdentifier=DatabaseName + '-backup' + str(datetime.datetime.now().strftime("%Y-%m-%d")),
        DBInstanceIdentifier=DatabaseName
        )
    
    snapshot_id = response['DBSnapshot']['DBSnapshotIdentifier']
    snapshot_completed = client.get_waiter('db_snapshot_available')
    try:
        snapshot_completed.wait(DBSnapshotIdentifier=snapshot_id)
    except Exception as e:
        if 'DBSnapshotNotFound' in str(e):
            print('Snapshot not found')
        else:
            print(e)
            print('Snapshot not Completed')
            raise e


def modifydbinstance():
    print(''' ---------------------------------------- \n 
              Modifying the RDS instance... \n 
              ---------------------------------------- ''')

    response = client.modify_db_instance(
        DBInstanceIdentifier=DatabaseName,
        AllocatedStorage=NewCapacity,
        ApplyImmediately=True
    )
    print(response)
    
    waiter = client.get_waiter('modify_db_instance_is_completed')
    waiter.config.delay = datetime.timedelta(seconds=10)
    waiter.config.max_attempts = 3
    waiter.wait(DBInstanceIdentifier=DatabaseName)
    DescribeDBInstances()


#Calling the functions
DescribeDBInstances()
NewCapacity = DescribeDBInstances.capacity + DBIncrease
createbackup()
modifydbinstance()
