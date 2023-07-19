import boto3 
boto3.Session()


def getCFTemplate(SourceRegion, TargetRegion, StackName, Role):

    SourceCF = boto3.client('cloudformation', region_name=SourceRegion)
    TargetCF = boto3.client('cloudformation', region_name=TargetRegion)
  
    try:
        response = SourceCF.get_template(StackName=StackName)
        template = response['TemplateBody']

        #Get Parameters from the source CF Template
        response = SourceCF.describe_stacks(StackName=StackName)
        parameters = response['Stacks'][0]['Parameters']
        print(parameters)

        #Create the Stack in different Region
        StackClone = StackName + '-backup'
        response = TargetCF.create_stack(
            StackName=StackClone,
            TemplateBody=template,
            RoleARN=Role,
            Parameters=parameters,
            Capabilities=[
                'CAPABILITY_NAMED_IAM',
                'CAPABILITY_IAM'
                ],
            )
        
        waiter = TargetCF.get_waiter('stack_create_complete')
        waiter.wait(StackName=StackName)
        print('Stack Created')

    except Exception as e:
        print('Error: {}'.format(e))
        return False
    
    return True
if __name__ == "__main__":
    Role = 'arn:aws:iam::<AccountID>:role/<ROLE>'
    getCFTemplate('<REGION>', '<REGION>', '<CF-Name>', Role)

    
         

        



