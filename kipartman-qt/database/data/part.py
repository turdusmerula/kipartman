from api.filter import FilterGroup, Filter, FilterRequest

from database.models import Part, PartInstance, Parameter, ParameterType, PartParameter, PartParameterOperator
import database.data.part_parameter

from django.db.models import Q, Count
import math

class PartException(Exception):
    def __init__(self, error):
        super(PartException, self).__init__(error)

# class FilterRange(FilterData):
#     def __init__(self, start, end):
#         self.start = start
#         self.end = end
#
#     def apply(self, request):
#         request.filter()

# class FilterPart(Filter):
#     def __init__(self, part):
#         self.part = part
#         super(FilterPart, self).__init__()
#
#     def apply(self, request):
#         return request.filter(id=self.part.id)
#
# class FilterPartId(Filter):
#     def __init__(self, id):
#         self.id = id
#         super(FilterPartId, self).__init__()
#
#     def apply(self, request):
#         return request.filter(id=self.id)
#
class FilterPartCategories(FilterRequest):
    def __init__(self, part_category_list, recursive):
        if len(part_category_list)==1:
            super(FilterPartCategories, self).__init__(name="Part category", description=part_category_list[0].name)
        else:
            super(FilterPartCategories, self).__init__(name="Part categories", description=f"{len(part_category_list)} categories selected")
            
        self.part_category_list = part_category_list
        self.recursive = recursive
        
    def Apply(self, request):
        part_category_ids = []
        
        if self.recursive==True:
            for part_category in self.part_category_list:
                sub_part_categories = part_category.get_descendants(include_self=True)
                for sub_part_category in sub_part_categories:
                    if sub_part_category.id not in part_category_ids:
                        part_category_ids.append(sub_part_category.id)
        else:
            for part_category in self.part_category_list:
                part_category_ids.append(part_category.id)

        return request.filter(category__in=part_category_ids)

#
# class FilterSymbols(Filter):
#     def __init__(self, symbols):
#         self.symbols = symbols
#         super(FilterSymbols, self).__init__()
#
#     def apply(self, request):
#         symbols_ids = [symbol.id for symbol in self.symbols]        
#
#         return request.filter(symbol_id__in=symbols_ids)
#
# class FilterFootprints(Filter):
#     def __init__(self, footprints):
#         self.footprints = footprints
#         super(FilterFootprints, self).__init__()
#
#     def apply(self, request):
#         footprints_ids = [footprint.id for footprint in self.footprints]        
#
#         return request.filter(footprint_id__in=footprints_ids)
#
# class FilterTextSearch(Filter):
#     def __init__(self, value):
#         self.value = value
#         super(FilterTextSearch, self).__init__()
#
#     def apply(self, request):
#         return request.filter(
#                     Q(name__contains=self.value) |
#                     Q(description__contains=self.value) |
#                     Q(comment__contains=self.value)
#                 )
#
#     def __str__(self):
#         return f"search: {self.value}"
#
# class FilterParameter(Filter):
#     def __init__(self, parameter):
#         self.parameter = parameter
#         super(FilterParameter, self).__init__()
#
#     def apply(self, request):
#         return request.filter(parameters__parameter__id=self.parameter.id)
#
# class FilterDistributor(Filter):
#     def __init__(self, distributor):
#         self.distributor = distributor
#         super(FilterDistributor, self).__init__()
#
#     def apply(self, request):
#         return request.filter(offers__distributor__id=self.distributor.id)
#
# class FilterManufacturer(Filter):
#     def __init__(self, manufacturer):
#         self.manufacturer = manufacturer
#         super(FilterManufacturer, self).__init__()
#
#     def apply(self, request):
#         return request.filter(manufacturer__id=self.manufacturer.id)
#
# class FilterStorage(Filter):
#     def __init__(self, storage):
#         self.storage = storage
#         super(FilterStorage, self).__init__()
#
#     def apply(self, request):
#         return request.filter(storages__storage__id=self.storage.id)
#
# class FilterUnit(Filter):
#     def __init__(self, unit):
#         self.unit = unit
#         super(FilterUnit, self).__init__()
#
#     def apply(self, request):
#         return request.filter(parameters__parameter__unit__id=self.unit.id)

class FilterMetapart(FilterRequest):
    def __init__(self, metapart):
        super(FilterMetapart, self).__init__(name="Filter metaparts", description=f"{metapart}")
        self.metapart = metapart

    def Apply(self, request):
        if self.metapart:
            return request.filter(instance=PartInstance.METAPART)
        return request.exclude(instance=PartInstance.METAPART)

class FilterNonePart(FilterRequest):
    def __init__(self):
        super().__init__(name="Filter no part", description=f"")

    def Apply(self, request):
        return request.filter(id=-1)

class FilterMetaParameter(FilterRequest):
    def __init__(self, part_parameter):
        super(FilterMetaParameter, self).__init__(name="Filter metapart parameter", description=part_parameter.parameter.name)
        self.part_parameter = part_parameter

    def Apply(self, request):
        operator = PartParameterOperator.EQ
        if self.part_parameter.operator is not None:
            operator = self.part_parameter.operator

        if self.part_parameter.parameter.value_type==ParameterType.TEXT:
            value = self.part_parameter.value['value']
            if operator==PartParameterOperator.EQ:
                return request.filter(
                    Q(parameters__parameter__id=self.part_parameter.parameter.id) & 
                    Q(parameters__value__value=value)
                )
        else:
            # we compute an epsilon at 2^-19 for equality comparison
            value = self.part_parameter.value['value']
            m, e = math.frexp(value)
            epsilon = math.ldexp(1, e-19)
            if operator==PartParameterOperator.EQ:
                return request.filter(
                    Q(parameters__parameter__id=self.part_parameter.parameter.id) & 
                    Q(parameters__value__value__gt=value-epsilon) & 
                    Q(parameters__value__value__lt=value+epsilon)
                )
#             elif operator=="<":
#                 return request.filter(Q(parameters__parameter__id=self.parameter.parameter.id) & Q(parameters__value__lt=self.parameter.value-epsilon))
#             elif operator=="<=":
#                 return request.filter(Q(parameters__parameter__id=self.parameter.parameter.id) & Q(parameters__value__lte=self.parameter.value+epsilon))
#             elif operator==">":
#                 return request.filter(Q(parameters__parameter__id=self.parameter.parameter.id) & Q(parameters__value__gt=self.parameter.value+epsilon))
#             elif operator==">=":
#                 return request.filter(Q(parameters__parameter__id=self.parameter.parameter.id) & Q(parameters__value__gte=self.parameter.value-epsilon))
#             elif operator=="!=":
#                 return request.filter(Q(parameters__parameter__id=self.parameter.parameter.id) & (Q(parameters__value__lt=self.parameter.value-epsilon) | Q(parameters__value__gt=self.parameter.value+epsilon))) 
#
#         return request

def _add_default_annotations(request):
    # add the field child_count in request result 
    request = request.select_related('category') # preload for performance
    return request

def find(filters: Filter=None):
    request = Part.objects
    
    request = _add_default_annotations(request)
    
    # apply filters
    if filters is not None:
        request = filters.Apply(request, filter=FilterRequest)
    
    request = request.order_by('id')
    print(request.query)
    return request.all()

def find_metapart_childs(part):
    filters = FilterGroup()
    if len(part.parameters.all())>0:
        filters.Append(FilterMetapart(False))
        
        for part_parameter in part.parameters.all():
            filters.Append(FilterMetaParameter(part_parameter))
            
    else:
        filters.Append(FilterNonePart())
    return find(filters)
# def save(part):
#
#     if part.pk is None:
#         part.save()
#
#     # build value
#     # TODO
#
#     part.save()
#
#
# def compute_value():
#     return ""
#
# def create(**kwargs):
#     part = Part(**kwargs)
#
#     return part
#
# def delete(part):
#     part.delete()
#
# def duplicate(part):
#     request = Part.objects
#
#     request = _add_default_annotations(request)
#
#     newpart = request.get(pk=part.id)
#     newpart.pk = None
# #     parameters = []
# #     for param in res.parameters.all():
# #         param.pk = None
# #         parameters.append(param)
# #     print("***", res.parameters)
# #     res.pk = None
# #     
# #     print("***", res.parameters)
#     return newpart

