import api.models
from datetime import date, datetime
from helper.filter import Filter
from api.models import PartManufacturer

# class FilterPart(Filter):
#     def __init__(self, part):
#         self.part = part
#         super(FilterPart, self).__init__()
#     
#     def apply(self, request):
#         return request.filter(part_id=self.part.id)
# 
class FilterManufacturer(Filter):
    def __init__(self, manufacturer):
        self.manufacturer = manufacturer
        super(FilterManufacturer, self).__init__()
     
    def apply(self, request):
        return request.filter(manufacturer_id=self.manufacturer.id)

def _add_default_annotations(request):
    # add the field child_count in request result 
    request = request.select_related('part', 'manufacturer') # preload for performance
    return request

def find(filters=[]):
    request = api.models.PartManufacturer.objects
    
    request = _add_default_annotations(request)
    
    for filter in filters:
        request = filter.apply(request)
    
    return request.order_by('id').all()

def create(part, **kwargs):
    part_parameter = PartManufacturer(**kwargs)
    part_parameter.part = part
    
    return part_parameter
