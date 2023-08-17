import boto3 
from parameters import Parameter
boto3.Session()

class CloneStack:
    def __init__(self, SourceRegion, TargetRegion, StackName, CloneStackName, updated_parameters=None):
        self.source_cf = boto3.client('cloudformation', region_name=SourceRegion) 
        self.target_cf = boto3.client('cloudformation', region_name=TargetRegion) 
        self.SourceRegion = SourceRegion
        self.TargetRegion = TargetRegion
        self.stack_name = StackName
        self.dr_stack_name = CloneStackName
        self.updated_parameters = updated_parameters


    def CloneCFStack(self):
        parameter_handler = Parameter(self.SourceRegion, self.stack_name, self.updated_parameters)
        parameters = parameter_handler.get_parameters()
        try:
            response = self.source_cf.get_template(StackName=self.stack_name) 
            template = response['TemplateBody'] 
            
            response = self.target_cf.create_stack(
                StackName=self.dr_stack_name,
                TemplateBody=template,
                Parameters=parameters,
                Capabilities=[
                    'CAPABILITY_NAMED_IAM',
                    'CAPABILITY_IAM'],
                )
            
            print(f"Creating Stack '{self.dr_stack_name}'")
            waiter = self.target_cf.get_waiter('stack_create_complete')
            
            try:
                waiter.wait(StackName=self.dr_stack_name)
                print(f"Stack '{self.dr_stack_name}' Created")
            except Exception as e:
                print(f"Error: '{e}'")
           
        except Exception as e:
            print(f"Error: '{e}'")
            return False
        return True


