import boto3
import datetime
from jira import JIRA

regions = ['eu-west-1']
session = boto3.Session()

jira_connection = JIRA(
    basic_auth=('@.com', ''),
    server="https://.atlassian.net"
)


size = 1000
initial = 0
list = []

while True:
    start = initial * size
    issues = jira_connection.search_issues(
                            'project =  ', start, size)
    if len(issues) == 0:
        break
    initial += 1
    for issue in issues:
        issue_title = issue.fields.summary
        list.append(issue_title)

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
                            'value': 'AWS_ECR_CONTAINER_IMAGE',
                        },
                    ],
                })


  try:
      #Loop through all Findings pages
      for page in page_iterator:
          for finding in page['findings']:
              Vulnerability_firstObserved = finding['firstObservedAt']
              Vulnerability_type = finding['type']
              Vulnerability_title = finding['title']
              Vulnerability_severity = finding['severity']
              Vulnerability_VulnerabilityId = finding['packageVulnerabilityDetails']['vulnerabilityId']
              Vulnerability_repositoryName = finding['resources'][0]['details']['awsEcrContainerImage']['repositoryName']


              #Convert Vulnerability_firstObserved to date
              Vulnerability_Date = Vulnerability_firstObserved.strftime("%Y-%m-%d")
              Day = datetime.datetime.now().strftime("%Y-%m-%d")

              # Check if Vulnerability is new
              if Vulnerability_Date == Day:
                  # Check if Vulnerability already exists in Jira
                  if Vulnerability_VulnerabilityId in list:
                      print('Vulnerability: ' + Vulnerability_VulnerabilityId + ' already exists in Jira\n')
                  else:
                      issue_dict = {
                          'project': {'key': ''},
                          'labels': [Vulnerability_repositoryName],
                          'priority': {'name': 'High'},
                          'summary': Vulnerability_VulnerabilityId,
                          'description': 'Type: ' + Vulnerability_type + '\n' +
                          'Title: ' + Vulnerability_title + '\n' +
                          'Severity: ' + Vulnerability_severity + '\n' +
                          'Repository name: ' + Vulnerability_repositoryName + '\n' ,
                          'issuetype': {'name': 'Bug'},
                      }
                      new_issue = jira_connection.create_issue(fields=issue_dict)

  except Exception as e:
      print(e)
