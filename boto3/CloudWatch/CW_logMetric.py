#AWS CIS 1.4 :  Controls 4.4 - 4.14 - Log Metric Filters and Alarms

import boto3
from botocore.exceptions import ClientError

session = boto3.Session()
regions = ['eu-west-1']

for region in regions:
    client = boto3.client('logs', region_name=region)
    sns = boto3.client('sns', region_name=region)

    #Create SNS Topic and Subscription
    try:
        newsns = sns.create_topic(Name='SNS-Topic-SecurityHub-%s' % region)
        SNSTopicArn = newsns['TopicArn']
        response = sns.subscribe(
            TopicArn=SNSTopicArn,
            Protocol='email',
            Endpoint='david_foley@fundrecs.com')
    except ClientError as e:
        print(e)
        continue
    
    #Create Log Group
    try:
        response = client.create_log_group(logGroupName='CIS-SecurityHub-%s' % region)
    except ClientError as e:
        print(e)
        continue

    #4.4	Ensure a log metric filter and alarm exist for IAM policy changes
    try:
        response = client.put_metric_filter(
            logGroupName='CIS-SecurityHub',
            filterName='CIS-4.4',
            filterPattern='{($.eventName=DeleteGroupPolicy) || ($.eventName=DeleteRolePolicy) || ($.eventName=DeleteUserPolicy) || ($.eventName=PutGroupPolicy) || ($.eventName=PutRolePolicy) || ($.eventName=PutUserPolicy) || ($.eventName=CreatePolicy) || ($.eventName=DeletePolicy) || ($.eventName=CreatePolicyVersion) || ($.eventName=DeletePolicyVersion) || ($.eventName=AttachRolePolicy) || ($.eventName=DetachRolePolicy) || ($.eventName=AttachUserPolicy) || ($.eventName=DetachUserPolicy) || ($.eventName=AttachGroupPolicy) || ($.eventName=DetachGroupPolicy)}',
            metricTransformations=[
                {
                    'metricName': 'CIS 4.4',
                    'metricNamespace': 'SecurityHub',
                    'metricValue': '1'
                },
            ]
        )
        try:
            response = client.put_metric_filter(
            AlarmName='CIS-4.4',
            AlarmDescription='CIS 4.4',
            ActionsEnabled=True,
            AlarmActions=[
                SNSTopicArn,
            ],
            MetricName='CIS 4.4',
            Namespace='SecurityHub',
            Statistic='Sum',
            Period=300,
            EvaluationPeriods=1,
            Threshold=1.0,
            ComparisonOperator='GreaterThanOrEqualToThreshold')
        except ClientError as e:
            print(e)
            continue

    except ClientError as e:
        print(e)
        continue

    #4.5	Ensure a log metric filter and alarm exist for CloudTrail configuration changes
    try:
        response = client.put_metric_filter(
            logGroupName='CIS-SecurityHub',
            filterName='CIS-4.5',
            filterPattern='{($.eventName=CreateTrail) || ($.eventName=UpdateTrail) || ($.eventName=DeleteTrail) || ($.eventName=StartLogging) || ($.eventName=StopLogging)}',
            metricTransformations=[
                {
                    'metricName': 'CIS 4.5',
                    'metricNamespace': 'SecurityHub',
                    'metricValue': '1'
                },
            ]
        )
    except ClientError as e:
        print(e)
        continue


    #4.7	Ensure a log metric filter and alarm exist for disabling or scheduled deletion of customer created CMKs
    try:
        response = client.put_metric_filter(
            logGroupName='CIS-SecurityHub',
            filterName='CIS-4.7',
            filterPattern='{($.eventName=CreateTrail) || ($.eventName=UpdateTrail) || ($.eventName=DeleteTrail) || ($.eventName=StartLogging) || ($.eventName=StopLogging)}',
            metricTransformations=[
                {
                    'metricName': 'CIS 4.7',
                    'metricNamespace': 'SecurityHub',
                    'metricValue': '1'
                },
            ]
        )
    except ClientError as e:
        print(e)
        continue

    #4.8	Ensure a log metric filter and alarm exist for S3 bucket policy changes
    try:
        response = client.put_metric_filter(
            logGroupName='CIS-SecurityHub',
            filterName='CIS-4.8',
            filterPattern='{($.eventSource=s3.amazonaws.com) && (($.eventName=PutBucketAcl) || ($.eventName=PutBucketPolicy) || ($.eventName=PutBucketCors) || ($.eventName=PutBucketLifecycle) || ($.eventName=PutBucketReplication) || ($.eventName=DeleteBucketPolicy) || ($.eventName=DeleteBucketCors) || ($.eventName=DeleteBucketLifecycle) || ($.eventName=DeleteBucketReplication))}',
            metricTransformations=[
                {
                    'metricName': 'CIS 4.8',
                    'metricNamespace': 'SecurityHub',
                    'metricValue': '1'
                },
            ]
        )
    except ClientError as e:
        print(e)
        continue

    #4.9 Ensure a log metric filter and alarm exist for AWS Config configuration changes
    try:
        response = client.put_metric_filter(
            logGroupName='CIS-SecurityHub',
            filterName='CIS-4.9',
            filterPattern='{($.eventSource=config.amazonaws.com) && (($.eventName=StopConfigurationRecorder) || ($.eventName=DeleteDeliveryChannel) || ($.eventName=PutDeliveryChannel) || ($.eventName=PutConfigurationRecorder))}',
            metricTransformations=[
                {
                    'metricName': 'CIS 4.9',
                    'metricNamespace': 'SecurityHub',
                    'metricValue': '1'
                },
            ]
        )
    except ClientError as e:
        print(e)
        continue


    #4.10	Ensure a log metric filter and alarm exist for security group changes
    try:
        response = client.put_metric_filter(
            logGroupName='CIS-SecurityHub',
            filterName='CIS-4.10',
            filterPattern='{($.eventName=AuthorizeSecurityGroupIngress) || ($.eventName=AuthorizeSecurityGroupEgress) || ($.eventName=RevokeSecurityGroupIngress) || ($.eventName=RevokeSecurityGroupEgress) || ($.eventName=CreateSecurityGroup) || ($.eventName=DeleteSecurityGroup)}',
            metricTransformations=[
                {
                    'metricName': 'CIS 4.10',
                    'metricNamespace': 'SecurityHub',
                    'metricValue': '1'
                },
            ]
        )
    except ClientError as e:
        print(e)
        continue


    #4.11	Ensure a log metric filter and alarm exist for changes to Network Access Control Lists (NACL)
    try:
        response = client.put_metric_filter(
            logGroupName='CIS-SecurityHub',
            filterName='CIS-4.11',
            filterPattern='{($.eventName=CreateNetworkAcl) || ($.eventName=CreateNetworkAclEntry) || ($.eventName=DeleteNetworkAcl) || ($.eventName=DeleteNetworkAclEntry) || ($.eventName=ReplaceNetworkAclEntry) || ($.eventName=ReplaceNetworkAclAssociation)}',
            metricTransformations=[
                {
                    'metricName': 'CIS 4.11',
                    'metricNamespace': 'SecurityHub',
                    'metricValue': '1'
                },
            ]
        )
    except ClientError as e:
        print(e)
        continue


    #4.12	Ensure a log metric filter and alarm exist for changes to network gateways
    try:
        response = client.put_metric_filter(
            logGroupName='CIS-SecurityHub',
            filterName='CIS-4.12',
            filterPattern='{($.eventName=CreateCustomerGateway) || ($.eventName=DeleteCustomerGateway) || ($.eventName=AttachInternetGateway) || ($.eventName=CreateInternetGateway) || ($.eventName=DeleteInternetGateway) || ($.eventName=DetachInternetGateway)}',
            metricTransformations=[
                {
                    'metricName': 'CIS 4.12',
                    'metricNamespace': 'SecurityHub',
                    'metricValue': '1'
                },
            ]
        )
    except ClientError as e:
        print(e)
        continue


    #4.13	Ensure a log metric filter and alarm exist for route table changes
    try:
         response = client.put_metric_filter(
            logGroupName='CIS-SecurityHub',
            filterName='CIS-4.13',
            filterPattern='{($.eventName=CreateRoute) || ($.eventName=CreateRouteTable) || ($.eventName=ReplaceRoute) || ($.eventName=ReplaceRouteTableAssociation) || ($.eventName=DeleteRouteTable) || ($.eventName=DeleteRoute) || ($.eventName=DisassociateRouteTable)}',
            metricTransformations=[
                {
                    'metricName': 'CIS 4.13',
                    'metricNamespace': 'SecurityHub',
                    'metricValue': '1'
                },
            ]
        )
    except ClientError as e:
        print(e)
        continue

    #4.14	Ensure a log metric filter and alarm exist for VPC changes
    try:
         response = client.put_metric_filter(
            logGroupName='CIS-SecurityHub',
            filterName='CIS-4.14',
            filterPattern='{($.eventName=CreateVpc) || ($.eventName=DeleteVpc) || ($.eventName=ModifyVpcAttribute) || ($.eventName=AcceptVpcPeeringConnection) || ($.eventName=CreateVpcPeeringConnection) || ($.eventName=DeleteVpcPeeringConnection) || ($.eventName=RejectVpcPeeringConnection) || ($.eventName=AttachClassicLinkVpc) || ($.eventName=DetachClassicLinkVpc) || ($.eventName=DisableVpcClassicLink) || ($.eventName=EnableVpcClassicLink)}',
            metricTransformations=[
                {
                    'metricName': 'CIS 4.14',
                    'metricNamespace': 'SecurityHub',
                    'metricValue': '1'
                },
            ]
        )
    except ClientError as e:
        print(e)



   
