"""
MySSMParameter:
  Type: Custom::SSMParameterInput
  Properties:
    Name: My/Parameter/Name
    [WithDecryption: True/False]

Access value by Ref-ing the resource.
All outputs from GetParameter are available as attributes.
"""

from cfn_custom_resource import CloudFormationCustomResource

class SSMParameterInput(CloudFormationCustomResource):
    DISABLE_PHYSICAL_RESOURCE_ID_GENERATION = True
    
    def _get(self):
        client = self.get_boto3_client('ssm')
        
        response = client.get_parameter(**self.resource_properties)
        
        value = response['Parameter']['Value']
        
        self.physical_resource_id = value
        
        return response['Parameter']
    
    def create(self):
        return self._get()
    
    def update(self):
        return self._get()
    
    def delete(self):
        pass