from parameters import Parameter
import boto3 
boto3.Session()

def getCFTemplate(SourceRegion, TargetRegion, StackName, DRStackName, updated_parameters=None):

    SourceCF = boto3.client('cloudformation', region_name=SourceRegion)
    TargetCF = boto3.client('cloudformation', region_name=TargetRegion) 

    parameter_handler = Parameter(SourceRegion, StackName, updated_parameters)
    parameters = parameter_handler.get_parameters()


    try:
        response = SourceCF.get_template(StackName=StackName) 
        template = response['TemplateBody'] 

        #Create a Clone of the Source Stack in the Target Region
        response = TargetCF.create_stack(
            StackName=DRStackName,
            TemplateBody=template,
            Parameters=parameters,
            Capabilities=[
                'CAPABILITY_NAMED_IAM',
                'CAPABILITY_IAM'
                ],
            )
        print(f"Creating Stack '{DRStackName}'")

        #Wait for the Stack to be created
        waiter = TargetCF.get_waiter('stack_create_complete')
        try:
            waiter.wait(StackName=DRStackName)
            print(f"Stack '{DRStackName}' Created")
        except Exception as e:
            print(f"Error: '{e}'")
           
    except Exception as e:
        print(f"Error: '{e}'")
        return False
    return True

if __name__ == "__main__":
    updated_params = {
    }
    getCFTemplate( updated_parameters=updated_params) 
    

    
