import boto3
from datetime import datetime, timedelta, timezone
import sys

def lambda_handler(event, context):
    time1 = datetime.now(timezone.utc) #Convert to UTC Time
    
    Session = boto3.Session()
    S3 = Session.resource('s3', region_name='us-east-1')
    S3Bucket = S3.Bucket('')

    #S3 Bucket Prefix
    Prefix = ['']

    #Remove Files older then 12 hours
    try:
        for i in Prefix: 
            for object in S3Bucket.objects.filter(Prefix=i):
                if object.last_modified < time1 - timedelta(hours=12):
                    object.delete()
                    print('Deleted: ' + object.key)
    except Exception as e:
        print(e)
        sys.exit(1)
