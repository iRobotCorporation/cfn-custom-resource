"""Decorators for using CloudFormationCustomResource with existing functions.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
from __future__ import absolute_import, print_function

from .cfn_custom_resource import CloudFormationCustomResource

class DecoratorHandler(CloudFormationCustomResource):
    #Storing functions here is weird because Python wants to bind them
    _create_func = None
    _update_func = None
    _delete_func = None
    
    #Disable resource type validity checking
    RESOURCE_TYPE_SPEC = None
    
    def create(self):
        return self.__class__._create_func(self)

    def update(self):
        return self.__class__._update_func(self)
    
    def delete(self):
        return self.__class__._delete_func(self)
    
def create(func):
    DecoratorHandler._create_func = func
    return func

def update(func):
    DecoratorHandler._update_func = func
    return func

def delete(func):
    DecoratorHandler._delete_func = func
    return func

handler = DecoratorHandler.get_handler()