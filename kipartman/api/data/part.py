from api.models import Part
from django.db.models import Count
from helper.filter import Filter

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
        
class FilterCategory(Filter):
    def __init__(self, category):
        self.category = category
        super(FilterCategory, self).__init__()
    
    def apply(self, request):
        categories = self.category.get_descendants(include_self=True)
        category_ids = [category.id for category in categories]        
        
        return request.filter(category__in=category_ids)

    def __str__(self):
        return f"category: {self.category.name}"

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
    
    return request.order_by('id').all()

def save(part):
    part.save()
    
    
def create():
    part = Part()
    
    return part

def duplicate(part):
    request = Part.objects
    
    request = _add_default_annotations(request)
    
    newpart = request.get(pk=part.id)
    newpart.pk = None
#     parameters = []
#     for param in res.parameters.all():
#         param.pk = None
#         parameters.append(param)
#     print("***", res.parameters)
#     res.pk = None
#     
#     print("***", res.parameters)
    return newpart