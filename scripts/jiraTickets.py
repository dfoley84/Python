import json
import urllib3
from urllib3.util import make_headers
def lambda_handler(event, context):
    jira_issue_id = event['issue_id'].split(",")
    jira_Token = event['jira_Token']
    jira_User = event['jira_User']
    http = urllib3.PoolManager()
    for i in jira_issue_id:
        url = f"https://<DOMAIN>.atlassian.net/rest/api/3/issue/{i}/transitions"

        headers = make_headers(basic_auth=f'{jira_User}:{jira_Token}')
        headers['Accept'] = 'application/json'
        headers['Content-Type'] = 'application/json'

        payload = json.dumps({
            "resolution": {
                "name": "Done"
            },
            "transition": {
                "id": "41"
            }
        })
        response = http.request('POST', url, body=payload, headers=headers)
        print(response.data)
