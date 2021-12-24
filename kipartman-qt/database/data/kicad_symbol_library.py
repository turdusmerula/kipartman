from database.models import KicadSymbolLibrary
from django.db.models import Count
from helper.filter import Filter

class FilterPath(Filter):
    def __init__(self, path):
        self.path = path
        super(FilterPath, self).__init__()
    
    def apply(self, request):
        return request.filter(path__startswith=self.path)

    def __str__(self):
        return f"path: {self.path}"

def find(filters=[]):
    request = KicadSymbolLibrary.objects
        
    for filter in filters:
        request = filter.apply(request)

    return request.order_by('id').all()

def create():
    library = KicadSymbolLibrary()
    
    return library

def save(library):
    library.save()
