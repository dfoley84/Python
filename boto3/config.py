#!/usr/bin/python3.6
import urllib3
import json
import requests
http = urllib3.PoolManager()


def lambda_handler(event, context):
    region = event['region']
    resource_id = event["detail"]["configurationItem"]["resourceId"]
    resource_type = event["detail"]["configurationItem"]["resourceType"]
    
    webhook = "https://hooks.slack.com/<>"
    msg = {
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "\n* Prod:: Config Item Change*"   
            }
        },
            {
              "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*`Region:`* " + region + "\n*`Resource Type:`* "+resource_type+"\n*`Resource ID:`* "+ resource_id
            },
          },
            {
              "type": "divider"
            },
            {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "For more details."
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "AWS Config"
                },
                "value": "View",
                "url": "https://console.aws.amazon.com/config/home?region="+region+"#/timeline/"+resource_type+"/"+resource_id+"/configuration",
                "action_id": "button-action"
            }
        }
        ]
    }
    
    post = requests.post(webhook, data=json.dumps(msg), headers={'Content-Type': 'application/json'})
    if post.status_code != 200:
        raise ValueError('Request to slack returned an error %s, the response is:\n%s' % (post.status_code, post.text))
        
    
