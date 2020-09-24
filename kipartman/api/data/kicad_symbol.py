from api.models import KicadSymbol
from helper.filter import Filter
from django.db.models import Q

class FilterPath(Filter):
    def __init__(self, path):
        self.path = path
        super(FilterPath, self).__init__()
    
    def apply(self, request):
        return request.filter(library__path__startswith=self.path)

    def __str__(self):
        return f"path: {self.path}"

class FilterTextSearch(Filter):
    def __init__(self, value):
        self.value = value
        super(FilterTextSearch, self).__init__()
    
    def apply(self, request):
        return request.filter(
                    Q(name__contains=self.value) |
                    Q(content__contains=self.value) |
                    Q(metadata__contains=self.value)
                )

    def __str__(self):
        return f"search: {self.value}"

def _add_default_annotations(request):
    # add the field child_count in request result 
    request = request.select_related('library') # preload for performance
    return request

def find(filters=[]):
    request = KicadSymbol.objects
    
    request = _add_default_annotations(request)
    
    for filter in filters:
        request = filter.apply(request)
    
    return request.order_by('id').all()

def create():
    symbol = KicadSymbol()
    
    return symbol
