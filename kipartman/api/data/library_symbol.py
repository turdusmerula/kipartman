from api.models import LibrarySymbol
from helper.filter import Filter

class FilterPath(Filter):
    def __init__(self, path):
        self.path = path
        super(FilterPath, self).__init__()
    
    def apply(self, request):
        return request.filter(library__path__startswith=self.path)

    def __str__(self):
        return f"path: {self.path}"


def _add_default_annotations(request):
    # add the field child_count in request result 
    request = request.select_related('library') # preload for performance
    return request

def find(filters=[]):
    request = LibrarySymbol.objects
    
    request = _add_default_annotations(request)
    
    for filter in filters:
        request = filter.apply(request)
    
    return request.order_by('id').all()
