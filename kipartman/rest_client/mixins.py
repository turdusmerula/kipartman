import requests
from rest_client.exceptions import QueryError

def create_serialize(obj):
    res = {}
    for field in obj.__fields__:
        if obj.__fields__[field].is_read_only()==False:
            res[field] = obj.__values__[field].serialize()
    return res

class GetQueryMixin(object):
    def get(self):
        try:
            url = self.baseurl+self.path
            res = requests.get(url, *self.args, **self.kwargs)
            res.raise_for_status()
            return self.model(**res.json())
        except requests.HTTPError as e:
            raise QueryError(format(e))
        

class UpdateQueryMixin(object):
    def update(self):
        pass


class CreateQueryMixin(object):
    def create(self, obj):
        if not issubclass(type(obj), self.model):
            raise QueryError("Cannot create object in %s: type mismatch" % (self.path))
        try:
            url = self.baseurl+self.path+'/'
            res = requests.post(url, json=create_serialize(obj))
            res.raise_for_status()
            return self.model(**res.json())
        except requests.HTTPError as e:
            raise QueryError(format(e))

class DeleteQueryMixin(object):
    def delete(self):
        pass
    
class GetQuerySetMixin(object):
    def get(self):
        url = self.baseurl+self.path
        request = requests.get(url, *self.args, **self.kwargs).json()
        # transform request result to a list of elements from model
        l = list()
        for el in request:
            l.append(self.model(**el))
        return l