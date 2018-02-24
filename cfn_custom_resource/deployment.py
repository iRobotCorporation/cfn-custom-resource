"""Utilities to deploy a custom resource Lambda.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import argparse
import sys, os.path
import pkg_resources
import six
import json
import shutil
import collections

def create_resource_and_output(name, code_uri, handler, set_function_name=False, runtime=None, policies=None, properties=None):
    if not runtime:
        runtime = 'python2.7' if six.PY2 else 'python3.6'
    
    if not policies:
        policies = 'AdministratorAccess'
    
    resource = {
        "Type": "AWS::Serverless::Function",
        "Properties": {
            "Handler": handler,
            "Runtime": runtime,
            "CodeUri": code_uri,
            "Policies": policies,
            "Timeout": 300,
        }
    }
    if set_function_name:
        resource['Properties']['FunctionName'] = name
    
    if properties:
        resource['Properties'].update(properties)
    
    output = {
        '{}Arn'.format(name): {
            'Value': {'Fn::GetAtt': [name, 'Arn']},
            'Export': {
                'Name': 'CustomResource:{}'.format(name)
            }
        }
    }
    
    return {name: resource}, output

def _parse_json(value):
    try:
        return json.loads(value)
    except:
        return value

def _property_argument(input):
    key, value = input.split('=')
    return (key, _parse_json(value))

"""
Input: file or dir
Option: 

"""

_config = collections.namedtuple('_config', ['name', 'code_uri', 'handler'])

def _get_config(path):
    if path.endswith('/'):
        path = path[:-1]
    handler_function = 'handler'
    if os.path.isfile(path):
        file_name = os.path.basename(path)
        name = file_name.rsplit('.',1)[0]
        code_uri = os.path.dirname(path)
        handler_file = name
    else:
        name = os.path.basename(path)
        code_uri = path
        for handler_file in [name, 'index', 'handler']:
            if os.path.isfile(os.path.join(path, '{}.py'.format(handler_file))):
                break
        else:
            raise RuntimeError('No handler file found!')
        
    handler = '{}.{}'.format(handler_file, handler_function)
    return _config(name, code_uri, handler)
         

def template_main():
    parser = argparse.ArgumentParser()
    parser.add_argument('code_uri')
    parser.add_argument('--set-function-name', action='store_true')
    parser.add_argument('--handler')
    parser.add_argument('--runtime')
    parser.add_argument('--policy', action='append', dest='policies')
    parser.add_argument('--property', action='append', type=_property_argument, dest='properties')
    
    parser.add_argument('--output', '-o')
    parser.add_argument('--add', '-a', action='store_true')
    parser.add_argument('--quiet', '-q', action='store_true')
    
    args = parser.parse_args()
    
    def exit(code, message=None):
        if args.quiet:
            message = None
        parser.exit(code, message)
    
    if not os.path.exists(args.code_uri):
        exit(1, "CodeUri is invalid")
    
    try:
        config = _get_config(args.code_uri)
    except Exception as e:
        exit(2, str(e))
    
    template_dir = '.'
    
    if not args.add:
        template_name = '{}-template.json'.format(config.name)
    else:
        template_name = 'template.json'
    
    if args.output:
        if os.path.isdir(args.output):
            template_dir = args.output
        else:
            template_dir, template_name = os.path.split(args.output)
    
    template_path = os.path.join(template_dir, template_name)
    
    if args.add and os.path.exists(template_path):
        with open(template_path, 'r') as fp:
            template = json.load(fp)
    else:
        template = {
            'Transform': 'AWS::Serverless-2016-10-31',
            'Resources': {},
            'Outputs': {}
        }
    
    kwargs = {
        'name': config.name,
        'code_uri': os.path.relpath(config.code_uri, template_dir),
        'handler': config.handler,
    }
    
    ccr_path = os.path.join(config.code_uri, 'cfn_custom_resource.py')
    if True: #not os.path.exists(ccr_path):
        with pkg_resources.resource_stream(__name__, 'cfn_custom_resource.py') as source, open(ccr_path, 'wb') as dest:
            shutil.copyfileobj(source, dest)
    
    resource, output = create_resource_and_output(**kwargs)

    template['Resources'].update(resource)
    template['Outputs'].update(output)
    
    with open(template_path, 'w') as fp:
        json.dump(template, fp, indent=2)
    
    if not args.quiet:
        sys.stdout.write('Wrote template to {}\n'.format(template_path))
