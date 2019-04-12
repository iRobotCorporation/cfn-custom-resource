from __future__ import print_function

import json
import unittest
import six

from cfn_custom_resource import CloudFormationCustomResource, utils as ccr_utils, decorator

CloudFormationCustomResource.RAISE_ON_FAILURE = True

import logging
logging.basicConfig()

class CustomResourceTestBase(CloudFormationCustomResource):
    def __init__(self, resource_type=None):
        kwargs = {}
        if resource_type:
            kwargs['resource_type'] = resource_type
        super(CustomResourceTestBase, self).__init__(**kwargs)
        
        self.send_response_function = self.capture_response
        
        self.test_response_resource = None
        self.test_response_url = None
        self.test_response_content = None
    
    def capture_response(self, resource, url, response_content):
        self.test_response_resource = resource
        self.test_response_url = url
        self.test_response_content = response_content
    
    def print_captured_response(self):
        six.print_('url:', self.test_response_url)
        six.print_('response:', self.test_response_content)

class BasicTest(unittest.TestCase):
    class CustomResourceBasicTest(CustomResourceTestBase):
        def __init__(self, outputs):
            super(BasicTest.CustomResourceBasicTest, self).__init__()
            self.create_called = False
            self.update_called = False
            self.delete_called = False
            self.outputs = outputs

        def create(self):
            self.create_called = True
            return self.outputs
        
        def update(self):
            self.update_called = True
            return self.outputs
        
        def delete(self):
            self.delete_called = True
            return self.outputs

    class CustomResourceNoStringifyTest(CustomResourceBasicTest):
        def __init__(self, outputs):
            super(BasicTest.CustomResourceNoStringifyTest, self).__init__(outputs)
            self.STRINGIFY_OUTPUT = False

    def test_create(self):
        properties = {
        }
        event = ccr_utils.generate_request('create', 'Custom::CustomResourceBasicTest', properties, CloudFormationCustomResource.DUMMY_RESPONSE_URL_SILENT)
        
        outputs = {'output_key': 'output_value'}
        
        obj = self.CustomResourceBasicTest(outputs)
        
        obj.handle(event, ccr_utils.MockLambdaContext())
        
        self.assertTrue(obj.create_called)
        
        self.assertEqual(obj.resource_outputs, outputs)

    def test_sns_create(self):
        properties = {
        }
        cfn_event = ccr_utils.generate_request('create', 'Custom::CustomResourceBasicTest', properties,
                                           CloudFormationCustomResource.DUMMY_RESPONSE_URL_SILENT)
        event = ccr_utils.generate_sns_event(json.dumps(cfn_event))

        outputs = {'output_key': 'output_value'}

        obj = self.CustomResourceBasicTest(outputs)

        obj.handle(event, ccr_utils.MockLambdaContext())

        self.assertTrue(obj.create_called)

        self.assertEqual(obj.resource_outputs, outputs)

    def test_update(self):
        properties = {
        }
        old_properties = {}
        event = ccr_utils.generate_request('update', 'Custom::CustomResourceBasicTest', properties, CloudFormationCustomResource.DUMMY_RESPONSE_URL_SILENT,
                                           old_properties=old_properties)
        
        outputs = {'output_key': 'output_value'}
        
        obj = self.CustomResourceBasicTest(outputs)
        
        obj.handle(event, ccr_utils.MockLambdaContext())
        
        self.assertTrue(obj.update_called)
        
        self.assertEqual(obj.resource_outputs, outputs)

    def test_sns_update(self):
        properties = {
        }
        old_properties = {}
        cfn_event = ccr_utils.generate_request('update', 'Custom::CustomResourceBasicTest', properties,
                                           CloudFormationCustomResource.DUMMY_RESPONSE_URL_SILENT,
                                           old_properties=old_properties)
        event = ccr_utils.generate_sns_event(json.dumps(cfn_event))

        outputs = {'output_key': 'output_value'}

        obj = self.CustomResourceBasicTest(outputs)

        obj.handle(event, ccr_utils.MockLambdaContext())

        self.assertTrue(obj.update_called)

        self.assertEqual(obj.resource_outputs, outputs)
    
    def test_delete(self):
        properties = {
        }
        event = ccr_utils.generate_request('delete', 'Custom::CustomResourceBasicTest', properties, CloudFormationCustomResource.DUMMY_RESPONSE_URL_SILENT)
        
        outputs = {'output_key': 'output_value'}
        
        obj = self.CustomResourceBasicTest(outputs)
        
        obj.handle(event, ccr_utils.MockLambdaContext())
        
        self.assertTrue(obj.delete_called)
        
        self.assertEqual(obj.resource_outputs, outputs)

    def test_sns_delete(self):
        properties = {
        }
        cfn_event = ccr_utils.generate_request('delete', 'Custom::CustomResourceBasicTest', properties,
                                           CloudFormationCustomResource.DUMMY_RESPONSE_URL_SILENT)
        event = ccr_utils.generate_sns_event(json.dumps(cfn_event))

        outputs = {'output_key': 'output_value'}

        obj = self.CustomResourceBasicTest(outputs)

        obj.handle(event, ccr_utils.MockLambdaContext())

        self.assertTrue(obj.delete_called)

        self.assertEqual(obj.resource_outputs, outputs)
    
    def test_single_output(self):
        properties = {
        }
        event = ccr_utils.generate_request('create', 'Custom::CustomResourceBasicTest', properties, CloudFormationCustomResource.DUMMY_RESPONSE_URL_SILENT)
        
        outputs = 'output_value'
        
        obj = self.CustomResourceBasicTest(outputs)
        
        obj.handle(event, ccr_utils.MockLambdaContext())
        
        self.assertTrue(obj.create_called)
        
        self.assertEqual(obj.resource_outputs, {'Value': outputs})
    
    def test_response_content(self):
        properties = {
        }
        event = ccr_utils.generate_request('create', 'Custom::CustomResourceBasicTest', properties, CloudFormationCustomResource.DUMMY_RESPONSE_URL_SILENT)
        
        outputs = {'output_key': 'output_value'}
        
        obj = self.CustomResourceBasicTest(outputs)
        
        obj.handle(event, ccr_utils.MockLambdaContext())
        
        self.assertEqual(obj.test_response_content['Status'], CloudFormationCustomResource.STATUS_SUCCESS)
        self.assertEqual(obj.test_response_content['Data'], outputs)

    def test_response_complex_content(self):
        properties = {
        }
        event = ccr_utils.generate_request('create', 'Custom::CustomResourceBasicTest', properties, CloudFormationCustomResource.DUMMY_RESPONSE_URL_SILENT)

        outputs = {'output_key': {'subkey': 'subvalue'}}

        obj = self.CustomResourceBasicTest(outputs)

        obj.handle(event, ccr_utils.MockLambdaContext())

        self.assertEqual(obj.test_response_content['Status'], CloudFormationCustomResource.STATUS_SUCCESS)
        self.assertEqual(obj.test_response_content['Data'],
                         {
                             'output_key': '{"subkey": "subvalue"}',  # stringified by default
                         })

    def test_response_complex_content_not_stringified(self):
        properties = {
        }
        event = ccr_utils.generate_request('create', 'Custom::CustomResourceNoStringifyTest', properties, CloudFormationCustomResource.DUMMY_RESPONSE_URL_SILENT)

        outputs = {'output_key': {'subkey': 'subvalue'}}

        obj = self.CustomResourceNoStringifyTest(outputs)

        obj.handle(event, ccr_utils.MockLambdaContext())

        self.assertEqual(obj.test_response_content['Status'], CloudFormationCustomResource.STATUS_SUCCESS)
        self.assertEqual(obj.test_response_content['Data'], outputs)

class TestPhysicalResourceId(unittest.TestCase):
    class CustomResourcePhysicalResourceId(CustomResourceTestBase):
        DISABLE_PHYSICAL_RESOURCE_ID_GENERATION = True
        
        def __init__(self, id_to_set, test_class):
            super(self.__class__, self).__init__()
            self.id_to_set = id_to_set
            self.test_class = test_class
        
        def create(self):
            self.test_class.assertIsNone(self.physical_resource_id)
            self.physical_resource_id = self.id_to_set
        
        def update(self):
            self.test_class.assertIsNone(self.physical_resource_id)
            self.physical_resource_id = self.id_to_set
        
        def delete(self):
            self.test_class.assertIsNone(self.physical_resource_id)
            self.physical_resource_id = self.id_to_set
    
    def test_set_physical_resource_id(self):
        properties = {
        }
        event = ccr_utils.generate_request('create', 'Custom::CustomResourcePhysicalResourceId', properties, CloudFormationCustomResource.DUMMY_RESPONSE_URL_SILENT)
        
        id_to_set = 'foo'
        
        obj = self.CustomResourcePhysicalResourceId(id_to_set, self)
        
        obj.handle(event, ccr_utils.MockLambdaContext())
        
        self.assertEqual(obj.physical_resource_id, id_to_set)

class TestDecorator(unittest.TestCase):
    
    def test_decorator(self):
        
        @decorator.create
        def create(resource):
            pass
        
        @decorator.update
        def update(resource):
            pass
        
        @decorator.delete
        def delete(resource):
            pass
        
        properties = {
        }
        event = ccr_utils.generate_request('create', 'Custom::DecoratorTest', properties, CloudFormationCustomResource.DUMMY_RESPONSE_URL_SILENT)
        
        decorator.handler(event, ccr_utils.MockLambdaContext())

if __name__ == '__main__':
    unittest.main()