import boto3

ecs_client = boto3.client('ecs', region_name='eu-west-1')
cluster_name = '<>'

paginator = ecs_client.get_paginator('list_services')
service_arns = []

for page in paginator.paginate(cluster=cluster_name, PaginationConfig={'PageSize': 100}):
    service_arns.extend(page['serviceArns'])

for arn in service_arns:
    tags = ecs_client.list_tags_for_resource(resourceArn=arn)['tags']
    update_service = False
    for tag in tags:
        if tag['key'] == 'Restart' and tag['value'] == 'True':
            update_service = True
            break
            
    if update_service:
        ecs_client.update_service(cluster=cluster_name, service=arn, forceNewDeployment=True)
        print(f"Service {arn} Restarting")
