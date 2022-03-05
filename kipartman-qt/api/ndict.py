import dpath.util
import jmespath
from munch import munchify, DefaultMunch
from schema import Schema, SchemaError, Optional, Hook, And, Or, Regex, Const, _callable_str
from collections.abc import MutableMapping

class NoneDefaultMunch(DefaultMunch):
    def __init__(self, *args, **kwargs):
        super(NoneDefaultMunch, self).__init__()

def ndict(value, default=None):
    return munchify(value, NoneDefaultMunch)

# def factory(type):
#     factory = {
#         list: nlist,
#         dict: ndict,
#         tuple: ntuple
#     }
#
#     if type in factory:
#         return factory[type]
#     return type
#
# class ndict(type(Proxy(dict))):
#     def __init__(self, *args, default: dict=None, schema=None, factory=factory, **kwargs):
#         self._store = dict()
#         self.update(dict(*args, **kwargs))  # use the free update to set keys
#
#         self._default = default
#         self._factory = factory 
#         self._schema = schema

