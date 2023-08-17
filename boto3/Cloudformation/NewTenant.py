import boto3, json

class NewTenant:
    def __init__(self, SourceRegion, StackName, TemplateBody, parameters):
        self.cf = boto3.client('cloudformation', region_name=SourceRegion)
        self.SourceRegion = SourceRegion
        self.StackName = StackName
        self.TemplateBody = TemplateBody
        self.parameters = parameters
    
    def CreateNewTenant(self):
        try:
            self.cf.create_stack(
                StackName=self.StackName,
                TemplateBody=self.TemplateBody,
                Parameters=self.parameters,
                Capabilities=[
                    'CAPABILITY_IAM',
                    'CAPABILITY_NAMED_IAM'
                ]
            )

            print(f"Creating New Tanent Stack '{self.StackName}'")
            waiter = self.cf.get_waiter('stack_create_complete')

            try:
                waiter.wait(StackName=self.StackName)
                print(f"Stack '{self.StackName}' created successfully")
            except Exception as e:
                print(f"Error: '{e}'")

        except Exception as e:
            print(f"Error: '{e}'")
            return False
        return True
        





    








