"""
MyS3Object:
  Type: Custom::S3Object
  Properties:
    Bucket: MyBucket
    Key: MyKey
    
    Text: <text>
    -OR-
    Binary: <base64>
    -OR-
    Json: <object, list, etc>
    
    [Other inputs to S3.PutObject]

Ref returns the ARN.
Bucket, Key are attributes.
"""

import six
import json
import base64

from botocore.exceptions import ClientError

from cfn_custom_resource import CloudFormationCustomResource

class S3Object(CloudFormationCustomResource):
    DISABLE_PHYSICAL_RESOURCE_ID_GENERATION = True
    
    def _put(self):
        bucket = self.resource_properties['Bucket']
        key = self.resource_properties['Key']
        
        inputs = {}
        body_count = 0
        for key, value in six.iteritems(self.resource_properties):
            if key in ['Text', 'Binary', 'Json']:
                body_count += 1
                continue
            inputs[key] = value
        
        if body_count > 1:
            raise KeyError("Body specified multiple times")
    
        if 'Text' in self.resource_properties:
            body = self.resource_properties['Text']
        elif 'Binary' in self.resource_properties:
            body = base64.b64decode(self.resource_properties['Binary'])
        elif 'Json' in self.resource_properties:
            body = json.dumps(self.resource_properties['Json'])
        else:
            raise KeyError("No body specified")
        
        inputs['Body'] = body
        
        client = self.get_boto3_client('s3')
        
        response = client.put_object(**inputs)
        
        self.physical_resource_id = 'arn:aws:s3:::{}/{}'.format(bucket, key)
        
        return {
            'Bucket': bucket,
            'Key': key,
        }
    
    def _delete(self, bucket, key):
        client = self.get_boto3_client('s3')
        try:
            client.delete_object(
                Bucket=bucket,
                Key=key)
        except ClientError as e:
            if e['Response']['Error']['Code'] not in ['NoSuchBucket', 'NoSuchKey']:
                raise
            else:
                self.logger.warn('Old object {}/{} seems to already be gone'.format(bucket, key))
    
    def create(self):
        return self._put()
    
    def update(self):
        return self._put()
    
    def delete(self):
        bucket, key = self.physical_resource_id.rsplit(':', 1)[-1].split('/', 1)
        return self._delete(bucket, key)

