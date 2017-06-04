from rest_client import fields
from rest_client import exceptions
from rest_client import registry
import copy


class MetaModel(type):
    """
    Used to register model classes inside registry, allowing to reference them with their
    name when class type is not possible
    """
    def __new__(cls, clsname, bases, attrs):
        # create a dictionary for model fields
        f = {}
        a = {}  # remove static attributes in class
        for attr in attrs:
            if issubclass(type(attrs[attr]), fields.Field):
                f[attr] = attrs[attr]
            else:
                a[attr] = attrs[attr]
        # create class object
        newclass = super(cls, MetaModel).__new__(cls, clsname, bases, a)
        newclass.__fields__ = f
        print clsname+": ", f
        
        # register class inside model registry
        registry.register(newclass)  # here is your register function
        return newclass

class Model(object):
    __metaclass__ = MetaModel
    """
    A class that allows to define a model with fields.
    Fields should be classes with 'set_value' and 'get_value' methods defined to access content
    """
    def __init__(self, *args, **kwargs):
        self.__values__ = {}
        # values associated to fields
        for f in self.__fields__:
            if kwargs.has_key(f):
                # put initialized value
                self.__values__[f] = copy.copy(self.__fields__[f])
                self.__values__[f].set_value(kwargs[f])
            else:
                # put default value
                self.__values__[f] = copy.copy(self.__fields__[f])

    def __setattr__(self, name, value):
        if hasattr(self, '__values__') and self.__values__.has_key(name):
            self.__values__[name].set_value(value)
        else:
            super(Model, self).__setattr__(name, value)

    def __getattr__(self, name):
        if self.__values__.has_key(name):
            return self.__values__[name].get_value()
        else:
            return super(Model, self).__getattr__(name)

        