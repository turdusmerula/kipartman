from rest_client import mixins
import copy
from exceptions import QueryError
    
class GenericQuery():
    path = '/'
    baseurl = 'http://localhost:8100/api'
    args = ()
    params = None

    def __init__(self, **kwargs):
        self.args = kwargs
        if self.params is None:
            self._decode()

    def _clone(self):
        kwargs = copy.deepcopy(self.kwargs)
        args = copy.deepcopy(self.args)
        url = copy.copy(self.url)
        cloned = self.__class__(url, **kwargs)
        cloned.request_method = self.request_method
        return cloned

    def _decode(self):
        self.params = []
        beg = 0
        pos = self.path.find('{', beg)
        while pos>-1:
            close = self.path.find('}', pos)
            if close>-1:
                param = self.path[pos+1:close]
                self.params.append(param)
            else:
                raise QueryError('%s: missing closing "}"' % (self.path))
            beg = close
            pos = self.path.find('{', beg)
            

class ReadOnlyQuery(mixins.GetQueryMixin,
            GenericQuery):
    def __init__(self, **kwargs):
        GenericQuery.__init__(self, **kwargs)
        
        
class Query(mixins.GetQueryMixin,
            mixins.UpdateQueryMixin,
            mixins.DeleteQueryMixin,
            GenericQuery):
    pass

        
class QuerySet(mixins.GetQuerySetMixin,
            mixins.CreateQueryMixin,
            mixins.UpdateQueryMixin,
            mixins.DeleteQueryMixin,
           GenericQuery):
    
    def __init__(self, **kwargs):
        GenericQuery.__init__(self, **kwargs)

    def filter(self, **kwargs):
        pass
    
    def __iter__(self):
        return iter(self.get())

    def __len__(self):
        return len(self.get())

    def __getitem__(self, index):
        return self.get()[index]
