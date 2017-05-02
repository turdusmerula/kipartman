import requests

class GetQueryMixin(object):
    def get(self):
        return requests.get(self.baseurl+self.path, *self.args, **self.kwargs).json()

class UpdateQueryMixin(object):
    def update(self):
        pass


class CreateQueryMixin(object):
    def create(self):
        pass

class DeleteQueryMixin(object):
    def delete(self):
        pass
