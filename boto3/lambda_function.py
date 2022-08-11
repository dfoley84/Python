import boto3
import json
from jira import JIRA

regions = ['eu-west-1']
#Jira connection

jira_connection = JIRA(
    basic_auth=('', ''),
    server="https://.atlassian.net"
)

def lambda_handler(event, context):
    session = boto3.Session()

    for region in regions:
        inspector = session.client('inspector2',region_name=region)
        paginator = inspector.get_paginator('list_findings')
        page_iterator = paginator.paginate(filterCriteria={
                        'findingStatus': [
                            {
                                'comparison': 'EQUALS',
                                'value': 'ACTIVE', 
                            },
                        ],
                        'findingType': [
                            {
                                'comparison': 'EQUALS',
                                'value': 'PACKAGE_VULNERABILITY',
                            },
                        ],
                        'severity': [
                            {
                                'comparison': 'EQUALS',
                                'value': 'CRITICAL',
                            },
                        ],
                        'resourceType': [
                            {
                                'comparison': 'EQUALS',
                                'value': 'AWS_EC2_INSTANCE',
                            },
                        ],
                    })
        
        try:
            for page in page_iterator:
                for finding in page['findings']:
                    AccountId = finding['awsAccountId']
                    Title = finding['title']
                    Description = finding['description']
                    Severity = finding['severity']
                    for resource in finding['resources']:
                        InstanceId = resource['id']
                        InstanceRegion = resource['region']
                        
                        #print(AccountId, Title, Description, Severity, InstanceId, InstanceRegion)
                        
                        issue_dict = {
                        'project': {'key': '<key>'},
                        'summary': Title,
                        'description': 'Vulnerability Level: ' + Severity + '\n' +
                        'Resource ID: ' + InstanceId + '\n' + 
                        'Region: ' + InstanceRegion + '\n' + 
                        'AWS Account: ' + AccountId + '\n' +
                        'Description: ' + Description,
                       'issuetype': {'name': 'Bug'},
                        'priority': {'name': 'High'}
                    }
                    new_issue = jira_connection.create_issue(fields=issue_dict)
                    
        except Exception as e:
            print(e)
            pass


