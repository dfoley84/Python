import boto3 
boto3.Session()


def getparameters(SourceRegion, StackName, updated_parameters=None):

    SourceCF = boto3.client('cloudformation', region_name=SourceRegion)
    response = SourceCF.describe_stacks(StackName=StackName)

    parameters = [] #Empty List to hold Parameters

    for parameter in response['Stacks'][0]['Parameters']:
        key = parameter['ParameterKey']
        if updated_parameters and key in updated_parameters: 
            value = updated_parameters[key]
        else:
            value = parameter['ParameterValue']
        parameters.append({'ParameterKey': key, 'ParameterValue': value})
    return parameters


def getCFTemplate(SourceRegion, TargetRegion, StackName, DRStackName, updated_parameters=None):

    SourceCF = boto3.client('cloudformation', region_name=SourceRegion)
    TargetCF = boto3.client('cloudformation', region_name=TargetRegion)

    parameters = getparameters(SourceRegion, StackName,updated_parameters) 

    try:
        response = SourceCF.get_template(StackName=StackName)
        template = response['TemplateBody'] 

        #Create a Clone of the Source Stack in the Target Region
        response = TargetCF.create_stack(
            StackName=DRStackName,
            TemplateBody=template,
            Parameters=parameters,
            #RoleARN=RoleName, 
            Capabilities=[
                'CAPABILITY_NAMED_IAM',
                'CAPABILITY_IAM'
                ],
            )
        #Wait for the Stack to be created
        waiter = TargetCF.get_waiter('stack_create_complete')
        waiter.wait(StackName=StackName)
        print('Stack Created')

    except Exception as e:
        print('Error: {}'.format(e))
        return False
    return True


if __name__ == "__main__":
    #RoleName = 'arn:aws:iam::ACCOUNT_ID:role/ROLE' <Change this to the ECS Role ARN> 


    #Overwrite the Parameters As Needed.
    updated_params = {
    }

    getCFTemplate('eu-west-1', 'eu-central-1', updated_parameters=updated_params)
    

    
