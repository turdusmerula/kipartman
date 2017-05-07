import requests

class GetQueryMixin(object):
    def get(self):
        url = self.baseurl+self.path
        return self.model(**requests.get(url, *self.args, **self.kwargs).json())
        

class UpdateQueryMixin(object):
    def update(self):
        pass


class CreateQueryMixin(object):
    def create(self):
        pass

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