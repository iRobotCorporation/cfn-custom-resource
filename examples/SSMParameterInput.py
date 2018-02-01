"""
MySSMParameter:
  Type: Custom::SSMParameterInput
  Properties:
    Name: My/Parameter/Name

A drop-in replacement for CloudFormation SSM parameter types
(see https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html#aws-ssm-parameter-types )
CloudFormation SSM parameter types don't allow for building the key from other 
inputs. They also don't allow for SecureString types. This resource will allow
getting the encrypted value of a SecureString, and the KeyId is available as
an attribute.

Access value by Ref-ing the resource.
All outputs from GetParameter are available as attributes.
"""

from cfn_custom_resource import CloudFormationCustomResource

class SSMParameterInput(CloudFormationCustomResource):
    DISABLE_PHYSICAL_RESOURCE_ID_GENERATION = True
    
    def _get(self):
        client = self.get_boto3_client('ssm')
        
        kwargs = {
            'Name': self.resource_properties['Name'],
            'WithDecryption': False,
        }
        
        response = client.get_parameter(**kwargs)
        
        value = response['Parameter']['Value']
        
        self.physical_resource_id = value
        
        return response['Parameter']
    
    def create(self):
        return self._get()
    
    def update(self):
        return self._get()
    
    def delete(self):
        pass