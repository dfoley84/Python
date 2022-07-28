import datetime
import logging
import json
import boto3
import requests
import time 


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
webhook = 'https://hooks.slack.com/services/'
regions = ['us-east-1', 'us-west-2', 'eu-west-1', 'ap-southeast-1']


def run(event, context):
    current_time = datetime.datetime.now().time()
    name = context.function_name
    logger.info("Your cron function " + name + " ran at " + str(current_time))
    session = boto3.Session()

    for region in regions:
        cfstack = session.client('cloudformation', region_name=region)
        detectionIDs = {}
        stacks = cfstack.describe_stacks()
        
        try:
            next_token = stacks['NextToken']
            while True:
                next_stack = cfstack.describe_stacks(NextToken=next_token)
                stacks['Stacks'] = stacks['Stacks'] + stacks['Stacks']
                try:
                    next_token = next_stack['NextToken']
                except:
                    break
        except:
            print("No pages of stacks in region: ")
            
        try:
            for i in stacks['Stacks']:
                if i['StackStatus'] not in ['CREATE_IN_PROGRESS', 'CREATE_FAILED','ROLLBACK_FAILED','DELETE_FAILED','UPDATE_ROLLBACK_FAILED','UPDATE_IN_PROGRESS','REVIEW_IN_PROGRESS','DELETE_IN_PROGRESS', 'ROLLBACK_COMPLETE']:
                    detectionID = cfstack.detect_stack_drift( StackName=i['StackName'] )
                    time.sleep(.1)
                    detectionIDs[i['StackName']] = detectionID['StackDriftDetectionId']
            time.sleep(5)
                    
            for stackName, detectionID in detectionIDs.items():
                driftStatus = cfstack.describe_stack_drift_detection_status( StackDriftDetectionId=detectionID)
                
                while driftStatus['DetectionStatus'] == 'DETECTION_IN_PROGRESS':
                    time.sleep(5)
                    driftStatus = cfstack.describe_stack_drift_detection_status( StackDriftDetectionId=detectionID )
 
                if driftStatus['StackDriftStatus'] == 'DRIFTED':
                    stack_arn = driftStatus['StackId']
                    payload = {
                            "attachments":[
                                {
                                    "fallback":'<https://' + region + '.console.aws.amazon.com/cloudformation/home?region=' + region + '#/stack/detail?stackId=' + stack_arn + '| View>',
                                    "pretext":'<https://' + region + '.console.aws.amazon.com/cloudformation/home?region=' + region + '#/stack/detail?stackId=' + stack_arn + '| View>',
                                    "color":"#D00000",
                                    "fields":[
                                        {
                                            "title":"Drift Detected Region: " + region,
                                            "value": stackName,
                                            "short": "false"
                                        }
                                    ]
                                }
                            ]
                            
                        }
                    post = requests.post(webhook, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
                    if post.status_code != 200:
                        raise ValueError('Request to slack returned an error %s, the response is:\n%s' % (post.status_code, post.text))
                        
        except Exception as e:
            print(e)
            print("No stacks in region: " + region)
