from api.models import Part
from django.db.models import Count
from helper.filter import Filter
from django.db.models import Q
import api.data.part_parameter

class PartException(Exception):
    def __init__(self, error):
        super(PartException, self).__init__(error)

class FilterPart(Filter):
    def __init__(self, part):
        self.part = part
        super(FilterPart, self).__init__()
    
    def apply(self, request):
        return request.filter(id=self.part.id)

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

class FilterParameter(Filter):
    def __init__(self, parameter):
        self.parameter = parameter
        super(FilterParameter, self).__init__()
    
    def apply(self, request):
        return request.filter(parameters__parameter__id=self.parameter.id)

class FilterDistributor(Filter):
    def __init__(self, distributor):
        self.distributor = distributor
        super(FilterDistributor, self).__init__()
    
    def apply(self, request):
        return request.filter(offers__distributor__id=self.distributor.id)

class FilterManufacturer(Filter):
    def __init__(self, manufacturer):
        self.manufacturer = manufacturer
        super(FilterManufacturer, self).__init__()
    
    def apply(self, request):
        return request.filter(manufacturer__id=self.manufacturer.id)

class FilterStorage(Filter):
    def __init__(self, storage):
        self.storage = storage
        super(FilterStorage, self).__init__()
    
    def apply(self, request):
        return request.filter(storages__storage__id=self.storage.id)

class FilterUnit(Filter):
    def __init__(self, unit):
        self.unit = unit
        super(FilterUnit, self).__init__()
    
    def apply(self, request):
        return request.filter(parameters__parameter__unit__id=self.unit.id)

class FilterMetapart(Filter):
    def __init__(self, metapart):
        self.metapart = metapart
        super(FilterMetapart, self).__init__()
    
    def apply(self, request):
        return request.filter(metapart=self.metapart)

class FilterMetaParameter(Filter):
    def __init__(self, parameter):
        self.parameter = parameter
        super(FilterMetaParameter, self).__init__()
    
    def apply(self, request):
        operator = "="
        if self.parameter.operator is not None:
            operator = self.parameter.operator
        
        if self.parameter.parameter.value_type==api.models.ParameterType.TEXT:
            if operator=="=":
                return request.filter(parameters__text_value=self.parameter.text_value)
            elif operator=="!=":
                return request.filter(parameters__text_value__ne=self.parameter.text_value)
        else:
            if operator=="=":
                return request.filter(parameters__value=self.parameter.value)
            elif operator=="<":
                return request.filter(parameters__value__lt=self.parameter.value)
            elif operator=="<=":
                return request.filter(parameters__value__lte=self.parameter.value)
            elif operator==">":
                return request.filter(parameters__value__gt=self.parameter.value)
            elif operator==">=":
                return request.filter(parameters__value__gte=self.parameter.value)
            elif operator=="!=":
                return request.filter(parameters__value__ne=self.parameter.value)

        return request

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

def find_metapart_childs(part):
    filters = [FilterMetapart(False)]
    
    for parameter in part.parameters.all():
        filters.append(FilterMetaParameter(parameter))
        
    return find(filters)

def expanded_value(part):
    parameters = {}
    for parameter in api.data.part_parameter.find([api.data.part_parameter.FilterPart(part)]).all():
        parameters[parameter.parameter.name] = parameter
    
    res = ""
    token = None
    for c in part.value:
        if c=="{":
            token = ""
        elif c=="}":
            if token=="name":
                res += part.name
            if token in parameters:
                res += ""
            token = None
        else:
            if token is None:
                res += c
            else:
                token += c
    
def save(part):
    
    if part.pk is None:
        part.save()
        
    # build list of childs
    childs = {}
    for child in part.childs.add_pendings():
        childs[child.id] = child
    for childid in childs:
        for childchild in childs[childid].childs.all():
            if childchild.id not in childs:
                childs[childchild.id] = childchild

    if part.id in childs:
        raise PartException("Recursive equivalence detected, a part can not contain itself as an equivalent part")

    # build value
    # TODO
    
    part.save()
    
    
def create(**kwargs):
    part = Part(**kwargs)
    
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