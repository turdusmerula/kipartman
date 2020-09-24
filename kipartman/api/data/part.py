from api.models import Part
from django.db.models import Count
from helper.filter import Filter
from django.db.models import Q

class PartException(Exception):
    def __init__(self, error):
        super(PartException, self).__init__(error)

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

class FilterSymbols(Filter):
    def __init__(self, symbols):
        self.symbols = symbols
        super(FilterSymbols, self).__init__()
    
    def apply(self, request):
        symbols_ids = [symbol.id for symbol in self.symbols]        
        
        return request.filter(symbol_id__in=symbols_ids)

class FilterFootprints(Filter):
    def __init__(self, footprints):
        self.footprints = footprints
        super(FilterFootprints, self).__init__()
    
    def apply(self, request):
        footprints_ids = [footprint.id for footprint in self.footprints]        
        
        return request.filter(footprint_id__in=footprints_ids)

class FilterTextSearch(Filter):
    def __init__(self, value):
        self.value = value
        super(FilterTextSearch, self).__init__()
    
    def apply(self, request):
        return request.filter(
                    Q(name__contains=self.value) |
                    Q(description__contains=self.value) |
                    Q(comment__contains=self.value)
                )

    def __str__(self):
        return f"search: {self.value}"

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
    
    childs = {}
    for child in part.childs.add_pendings():
        childs[child.id] = child
    for childid in childs:
        for childchild in childs[childid].childs.all():
            if childchild.id not in childs:
                childs[childchild.id] = childchild

    if part.id in childs:
        raise PartException("Recursive equivalence detected, a part can not contain itself as an equivalent part")

    part.save()
    
    
def create():
    part = Part()
    
    return part

def delete(part):
    part.delete()
    
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