import dpath.util
import jmespath
from mergedeep import merge, Strategy
from schema import Schema, SchemaError, Optional, Hook, And, Or, Regex, Const, _callable_str

class NDictException(Exception):
    def __init__(self, error):
        super(NDictException, self).__init__(error)

class NDictReadOnlyException(NDictException):
    def __init__(self):
        super(NDictReadOnlyException, self).__init__("Dict is read only")

def factory(type):
    factory = {
        list: nlist,
        dict: ndict,
        tuple: ntuple
    }
    
    if type in factory:
        return factory[type]
    return type

class _iterator(object):
    def __init__(self, values, strategy, factory):
        self._values = values
        self._strategy = strategy
        self._factory = factory
        self._iter = iter(self._values)
      
    def __next__(self):
        v = next(self._iter)
        t = type(v)
        f = self._factory(t)
        if f is not t:
            return f(v, strategy=self._strategy, factory=self._factory, ro=True)
        return v

class ndict(object):
    def __init__(self, *args, default: dict=None, schema=None, strategy=Strategy.REPLACE, factory=factory, ro=False, **kwargs):
        try:
            # we try first not to make a copy
            _dict, = args
            if isinstance(_dict, dict)==False:
                # we shall make a copy
                _dict =  dict(*args, **kwargs)
        except Exception as e:
            # we shall make a copy
            _dict =  dict(*args, **kwargs)
        if isinstance(default, dict):
            default = ndict(default)
            
        super().__setattr__('_dict', _dict)
        super().__setattr__('_default', default)
        super().__setattr__('_strategy', strategy)
        super().__setattr__('_factory', factory)
        super().__setattr__('_ro', ro)
        # self._schema = schema

    def __getattr__(self, name):
        _dict = self.__getattribute__('_dict')
        _factory = self.__getattribute__('_factory')
        _strategy = self.__getattribute__('_strategy')
        _default = self.__getattribute__('_default')
        _ro = self.__getattribute__('_ro')
        
        # if hasattr(_dict, name):
        #     return getattr(_dict, name)
        if hasattr(super(), name):
            return getattr(super(), name)
        else:
            if _default is not None: 
                try:
                    v = _dict[name]
                except KeyError as e:
                    v = _default[name]
            else:
                v = _dict[name]
            t = type(v)
            f = _factory(t)
            if f is not t:
                return f(v, default=(_default or {}).get(name, None), strategy=_strategy, factory=_factory, ro=_ro)
            return v

    def __setattr__(self, name, value):
        _dict = self.__getattribute__('_dict')
        _ro = self.__getattribute__('_ro')
        
        if _ro:
            raise NDictReadOnlyException()

        # if hasattr(_dict, name):
        #     setattr(_dict, name, value)
        if hasattr(super(), name):
            setattr(super(), name, value)
        else:
            _dict[name] = value

    def __getitem__(self, name):
        _dict = self.__getattribute__('_dict')
        _strategy = self.__getattribute__('_strategy')
        _factory = self.__getattribute__('_factory')
        _default = self.__getattribute__('_default')
        _ro = self.__getattribute__('_ro')

        if _default is not None: 
            try:
                v = _dict[name]
            except KeyError as e:
                v = _default[name]
        else:
            v = _dict[name]
        t = type(v)
        f = _factory(t)
        if f is not t:
            return f(v, default=(_default or {}).get(name, None), strategy=_strategy, factory=_factory, ro=_ro)
        return v

    def get(self, name, default=None):
        _dict = self.__getattribute__('_dict')
        _strategy = self.__getattribute__('_strategy')
        _factory = self.__getattribute__('_factory')
        _default = self.__getattribute__('_default')
        _ro = self.__getattribute__('_ro')

        v = default
        if _default is not None: 
            try:
                v = _dict[name]
            except KeyError as e:
                v = _default[name]
        else:
            v = _dict[name]
        t = type(v)
        f = _factory(t)
        if f is not t:
            return f(v, default=(_default or {}).get(name, None), strategy=_strategy, factory=_factory, ro=_ro)
        return v

    def __setitem__(self, key, value):
        _dict = self.__getattribute__('_dict')
        _ro = self.__getattribute__('_ro')

        if _ro:
            raise NDictReadOnlyException()

        _dict[key] = value

    def __eq__(self, other):
        _dict = self.__getattribute__('_dict')
        return _dict==other

    def __str__(self):
        _dict = self.__getattribute__('_dict')
        return _dict.__str__()
    
    def __repr__(self):
        _dict = self.__getattribute__('_dict')
        return _dict.__repr__()

    def __getstate__(self):
        _dict = self.__getattribute__('_dict')
        return _dict
        
    # def __setstate__(self, dict):
    #     fh = open(dict['name'])  # reopen file
    #     self.name = dict['name']
    #     self.file = fh

    def __iter__(self):
        to_dict = self.__getattribute__('to_dict')
        _strategy = self.__getattribute__('_strategy')
        _factory = self.__getattribute__('_factory')
        return _iterator(to_dict(), strategy=_strategy, factory=_factory)

    def keys(self):
        to_dict = self.__getattribute__('to_dict')
        return to_dict().keys()

    def values(self):
        to_dict = self.__getattribute__('to_dict')
        return to_dict().values()
    
    def items(self):
        to_dict = self.__getattribute__('to_dict')
        return to_dict().items()

    def to_dict(self): #, recursive=True, strategy=Strategy.REPLACE):
        _dict = self.__getattribute__('_dict')
        _strategy = self.__getattribute__('_strategy')
        _default = self.__getattribute__('_default')
        res = {}
        if _default is None:
            merge(res, _dict, strategy=_strategy)
        else:
            merge(res, _default.to_dict(), _dict, strategy=_strategy)
        return res


class nlist(list):
    def __init__(self, *args, default=None, strategy=Strategy.REPLACE, factory=factory, ro=False, **kwargs):
        super(nlist, self).__init__(*args, **kwargs)

        try:
            # we try first not to make a copy
            _list, = args
            if isinstance(_list, list)==False:
                # we shall make a copy
                _list =  list(*args, **kwargs)
        except Exception as e:
            # we shall make a copy
            _list =  list(*args, **kwargs)
        super().__setattr__('_list', _list)
        super().__setattr__('_factory', factory)
        super().__setattr__('_strategy', strategy)
        super().__setattr__('_ro', ro)
        
    def __getattr__(self, name):
        _list = self.__getattribute__('_list')
        if hasattr(_list, name):
            return getattr(_list, name)
        else:
            return getattr(super(), name)

    def __setattr__(self, name, value):
        _list = self.__getattribute__('_list')
        _ro = self.__getattribute__('_ro')
        
        if _ro:
            raise NDictReadOnlyException()

        if hasattr(_list, name):
            setattr(_list, name, value)
        else:
            setattr(super(), name, value)

    def __getitem__(self, key):
        _list = self.__getattribute__('_list')
        _strategy = self.__getattribute__('_strategy')
        _factory = self.__getattribute__('_factory')
        _ro = self.__getattribute__('_ro')
        v = _list[key]
        t = type(v)
        f = _factory(t)
        if f is not t:
            return f(v, strategy=_strategy, factory=_factory, ro=_ro)
        return v

    def __setitem__(self, key, value):
        _list = self.__getattribute__('_list')
        _ro = self.__getattribute__('_ro')
        
        if _ro:
            raise NDictReadOnlyException()

        _list[key] = value
    
    def __eq__(self, other):
        _list = self.__getattribute__('_list')
        return _list==other

    def __str__(self):
        _list = self.__getattribute__('_list')
        return _dict.__str__()
    
    def __repr__(self):
        _list = self.__getattribute__('_list')
        return _list.__repr__()

    def __iter__(self):
        _list = self.__getattribute__('_list')
        _strategy = self.__getattribute__('_strategy')
        _factory = self.__getattribute__('_factory')
        return _iterator(_list, strategy=_strategy, factory=_factory)

class ntuple(tuple):
    def __init__(self, *args, factory=factory, **kwargs):
        super(ntuple, self).__init__(*args, **kwargs)
    
class Merge():
    pass

class Replace():
    pass
