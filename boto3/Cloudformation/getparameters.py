import boto3 
boto3.Session()

class Parameter:
    def __init__(self, Region, StackName, updated_parameters=None):
        self.cf=boto3.client('cloudformation', region_name=Region)
        self.Region = Region
        self.StackName = StackName
        self.updated_parameters = updated_parameters
        self.parameters = []
    
    def get_parameters(self):
        try: 
            response = self.cf.describe_stacks(StackName=self.StackName)
            for i in response['Stacks'][0]['Parameters']:
                key = i['ParameterKey']
                if self.updated_parameters and key in self.updated_parameters:
                    value = self.updated_parameters[key]
                else:
                    value = i['ParameterValue']
                self.parameters.append({'ParameterKey': key, 'ParameterValue': value})
            return self.parameters
        except Exception as e:
            print('Error: {}'.format(e))
            return False
        
    
            
