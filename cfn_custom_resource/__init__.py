"""Module providing a base class for Lambda-backed custom CloudFormation resources.

The class, CloudFormationCustomResource, has methods that child classes
implement to create, update, or delete the resource, while taking care of the
parsing of the input, exception handling, and response sending.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from __future__ import absolute_import

def _get_version():
    import pkg_resources, codecs
    if not pkg_resources.resource_exists(__name__, '_version'):
        return '0.0.0'
    with pkg_resources.resource_stream(__name__, '_version') as fp:
        return codecs.getreader('utf-8')(fp).read().strip()
__version__ = _get_version()

from .cfn_custom_resource import CloudFormationCustomResource
from . import utils