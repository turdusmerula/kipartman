import requests
from rest_client.exceptions import QueryError
import re

# TODO: implement patch to update only modified elements

def create_serialize(obj):
    res = {}
    for field in obj.__fields__:
        if obj.__fields__[field].is_read_only()==False:
            res[field] = obj.__values__[field].serialize()
    return res

def update_serialize(obj):
    res = {}
    for field in obj.__fields__:
        if obj.__fields__[field].is_read_only()==False:
            res[field] = obj.__values__[field].serialize()
    return res

class GetQueryMixin(object):
    def get(self, *args, **kwargs):
        url = self.baseurl+self.path
        iarg = 0
        for arg in args:
            url.replace('{'+self.params[iarg]+'}', arg)
            iarg += 1
        for arg in kwargs:
            url.replace('{'+arg+'}', kwargs[arg])
        try:
            res = requests.get(url, *self.args, **self.kwargs)
            res.raise_for_status()
            return self.model(**res.json())
        except requests.HTTPError as e:
            raise QueryError(format(e), res.json())
        

class UpdateQueryMixin(object):
    def update(self, obj):
        if not issubclass(type(obj), self.model):
            raise QueryError("Cannot update object in %s: type mismatch" % (self.path))
        try:
            url = obj.path
            res = requests.put(url, json=update_serialize(obj))
            res.raise_for_status()
            return self.model(**res.json())
        except requests.HTTPError as e:
            raise QueryError(format(e), res.json())


class CreateQueryMixin(object):
    def create(self, obj):
        if not issubclass(type(obj), self.model):
            raise QueryError("Cannot create object in %s: type mismatch" % (self.path))
        try:
            url = self.baseurl+self.path
            url = re.sub('{.*}', '', url)
            res = requests.post(url, json=create_serialize(obj))
            res.raise_for_status()
            return self.model(**res.json())
        except requests.HTTPError as e:
            raise QueryError(format(e), res.json())

class DeleteQueryMixin(object):
    def delete(self, obj):
        if not issubclass(type(obj), self.model):
            raise QueryError("Cannot delete object in %s: type mismatch" % (self.path))
        try:
            url = obj.path
            res = requests.delete(url)
            res.raise_for_status()
        except requests.HTTPError as e:
            raise QueryError(format(e), res.json())
    
class GetQuerySetMixin(object):
    def get(self, *args, **kwargs):
        url = self.baseurl+self.path
        iarg = 0
        for arg in args:
            url = url.replace('{'+self.params[iarg]+'}', str(arg))
            iarg += 1
        for arg in kwargs:
            url.replace('{'+arg+'}', kwargs[arg])
        url = re.sub('{.*}', '', url)
        print url
        request = requests.get(url, params=self.args).json()
        # transform request result to a list of elements from model
        l = list()
        if isinstance(request, list): 
            for el in request:
                l.append(self.model(**el))
        else:
            l.append(self.model(**request))
        return l