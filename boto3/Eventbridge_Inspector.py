import boto3
from jira import JIRA

#Jira connection
jira_connection = JIRA(
    basic_auth=('@.com', ''),
    server="https://.atlassian.net")

def lambda_handler(event, context):

    #Get all the issues from Jira
    while True:
        start = initial * size
        issues = jira_connection.search_issues(
                                'project = SEC', start, size)
        if len(issues) == 0:
            break
        initial += 1
        for issue in issues:
            issue_title = issue.fields.summary
            list.append(issue_title)
    try:
        #Get the Event from EventBridge For Inspector Finding
        Vulnerability_title = event['detail']['title']
        Vulnerability_type = event['detail']['type']
        Vulnerability_severity = event['detail']['severity']
        RepositoryName = event['detail']['resources'][0]['details']['awsEcrContainerImage']['repositoryName']
        Vulnerability_VulnerabilityId = event['detail']['packageVulnerabilityDetails']['vulnerabilityId']
        
        #Check if Vulnerability already exists in Jira
        issues = jira_connection.search_issues(
                            'project = <> AND summary ~' + Vulnerability_VulnerabilityId)
        if len(issues) > 0:
            print('Vulnerability: ' + Vulnerability_VulnerabilityId + ' already exists in Jira\n')
        else
            issue_dict = {
                'project': {'key': ''},
                'summary':Vulnerability_VulnerabilityId,
                'priority': {'name': Vulnerability_priority },
                'labels': [RepositoryName],
                'description': 'Type: ' + Vulnerability_type + '\n ' +
                               'Title: ' + Vulnerability_title + '\n ' +
                               'Severity: ' + Vulnerability_severity + '\n ' +
                               'Repository Name: ' + RepositoryName + '\n ',
                'issuetype': {'name': 'Bug'}
                }
            new_issue = jira_connection.create_issue(fields=issue_dict)
    except Exception as e:
        print(e)

