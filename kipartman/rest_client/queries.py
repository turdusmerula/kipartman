from rest_client import mixins
import copy

class GenericQuery():
    path = '/'
    baseurl = 'http://localhost:8100/api'
    args = ()
    kwargs = {}
    
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def _clone(self):
        kwargs = copy.deepcopy(self.kwargs)
        args = copy.deepcopy(self.args)
        url = copy.copy(self.url)
        cloned = self.__class__(url, *args, **kwargs)
        cloned.request_method = self.request_method
        return cloned


class ReadOnlyQuery(mixins.GetQueryMixin,
            GenericQuery):
    pass
        
class Query(mixins.GetQueryMixin,
            mixins.UpdateQueryMixin,
            mixins.DeleteQueryMixin,
            GenericQuery):
    pass


class QueryId(mixins.GetQueryMixin,
            mixins.UpdateQueryMixin,
            mixins.DeleteQueryMixin,
            GenericQuery):
    def __init__(self, object_id):
        self.path += "/"+object_id 


class QueryUrl(mixins.GetQueryMixin,
            mixins.UpdateQueryMixin,
            mixins.DeleteQueryMixin,
            GenericQuery):
    def __init__(self, url):
        self.path = url.replace(self.baseurl, "")

        
class QuerySet(mixins.GetQuerySetMixin,
               GenericQuery):
    def filter(self, **kwargs):
        pass
    
    def __iter__(self):
        return iter(self.get())

    def __len__(self):
        return len(self.get())

    def __getitem__(self, index):
        return self.get()[index]
