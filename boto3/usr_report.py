import boto3

profile = boto3.session.Session(profile_name='Automation')
resource = boto3.resource('iam')

report = resource.get_account_authorization_details(Filter=['User'])
r = report['UserDetailList'].decode('utf-8')
with open('report.csv', 'w') as f:
    f.write(r)

