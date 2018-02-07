"""
Created on Feb 7, 2018

@author: bkehoe
"""
from __future__ import absolute_import, print_function

from .cfn_custom_resource import CloudFormationCustomResource

class DecoratorHandler(CloudFormationCustomResource):
    #TODO: storing functions here is weird because Python wants to bind them
    # quick fix is to store them as 1-tuples
    _create_func = None
    _update_func = None
    _delete_func = None
    
    RESOURCE_TYPE = None
    
    def create(self):
        return self._create_func[0](self)

    def update(self):
        return self._update_func[0](self)
    
    def delete(self):
        return self._delete_func[0](self)
    
def create(func):
    DecoratorHandler._create_func = (func,)
    return func

def update(func):
    DecoratorHandler._update_func = (func,)
    return func

def delete(func):
    DecoratorHandler._delete_func = (func,)
    return func

handler = DecoratorHandler.get_handler()