"""cfn-custom-resource setup module

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from setuptools import setup

def get_version(name):
    import os.path
    path = os.path.join(name, '_version')
    if not os.path.exists(path):
        return "0.0.0"
    with open(path) as f:
        return f.read().strip()

setup(
    name='cfn-custom-resource',
    version=get_version('cfn_custom_resource'),
    description='Collection of tools to enable use of AWS Lambda with CloudFormation',
    entry_points={
        'console_scripts': [
            'cfn-custom-resource-template = cfn_custom_resource.deployment:template_main',
        ],
    },
    packages=["cfn_custom_resource"],
    package_data={
        "cfn_custom_resource": ["_version"]
    },
    install_requires=['boto3',
                      'botocore',
                      'requests'],
    project_urls={
        "Source Code": "https://github.com/iRobotCorporation/cfn-custom-resource",
    },
    author='Ben Kehoe',
    author_email='bkehoe@irobot.com',
    license='MPL-2.0',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='aws lambda cloudformation',
)
