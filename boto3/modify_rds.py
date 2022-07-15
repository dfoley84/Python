from re import S
import boto3
import datetime

session = boto3.Session(
    aws_access_key_id='',
    aws_secret_access_key='',
    aws_session_token='',
    region_name=''
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
