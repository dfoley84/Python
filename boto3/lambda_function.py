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
        
        
        #JIRA Query
        size = 100
        initial = 0

        list = []
        while True:
            start= initial*size
            issues = jira_connection.search_issues('project=<>',  start,size)
            if len(issues) == 0:
                break
            initial += 1
            for issue in issues:
                issue_title = issue.fields.summary
                issues_description = issue.fields.description[13:]
                s = issues_description.replace('Region: ','')
                s1 = s[:s.find('\n')]
                list.append([s1,issue_title])

        try:
            for page in page_iterator:
                for finding in page['findings']:
                    AccountId = finding['awsAccountId']
                    Title = finding['title']
                    for resource in finding['resources']:
                        InstanceId = resource['id']
                        InstanceRegion = resource['region']
                        if [InstanceId, Title] in list:
                            print('Issue Exists')
                        else:
                            issue_dict = {
                                'project': {'key': 'TET'},
                                'summary': Title,
                                'description':  'Resource ID: ' + InstanceId + '\n' + 
                                'Region: ' + InstanceRegion + '\n',
                                'issuetype': {'name': 'Bug'}
                            }
                            new_issue = jira_connection.create_issue(fields=issue_dict)


        except Exception as e:
            print(e)
