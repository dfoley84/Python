import boto3
regions = ['eu-west-1', 'us-east-1', 'us-west-2', 'ap-southeast-2']

for region in regions:
    client = boto3.client('ecr', region_name=region)
    response = client.describe_repositories()
    for repo in response['repositories']:
        repo_name = repo['repositoryName']

        client.put_image_scanning_configuration(
            repositoryName=repo_name,
            imageScanningConfiguration={
                'scanOnPush': True
            }
        )
        print(f"Image scanning on push enabled for repository: {repo_name} in region: {region}")
