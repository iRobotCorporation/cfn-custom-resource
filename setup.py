"""cfn-custom-resource setup module

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from setuptools import setup

setup(
    name='cfn-custom-resource',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='1.1.0',

    description='Collection of tools to enable use of AWS Lambda with CloudFormation',
    
    entry_points={
        'console_scripts': [
            'cfn-custom-resource-template = cfn_custom_resource.deployment:template_main',
        ],
    },
    packages=["cfn_custom_resource"],
    install_requires=['boto3',
                      'botocore'],
    
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
    ],
    keywords='aws lambda cloudformation',
)
