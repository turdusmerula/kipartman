from api.models import Part
from django.db.models import Count

class Filter(object):
    def __init__(self):
        pass
    
    def apply(self, request):
        return request

# filter to request part childs
class FilterChilds(Filter):
    def __init__(self, part):
        self.part = part
        super(FilterChilds, self).__init__()
    
    def apply(self, request):
        childs_id = []
        for child in self.part.childs.all():
            childs_id.append(child.pk)
        return request.filter(pk__in=childs_id)
    
def _add_default_annotations(request):
    # add the field child_count in request result 
    request = request.select_related('category', 'footprint', 'symbol') # preload for performance
    request = request.annotate(child_count=Count('childs'))
    return request

def find(filters=[]):
    request = Part.objects
    
    request = _add_default_annotations(request)
    
    for filter in filters:
        request = filter.apply(request)
    
    return request.all()
