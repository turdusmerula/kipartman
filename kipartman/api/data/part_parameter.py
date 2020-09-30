import api.models
from datetime import date, datetime
from helper.filter import Filter
from api.models import PartParameter

class FilterPart(Filter):
    def __init__(self, part):
        self.part = part
        super(FilterPart, self).__init__()
    
    def apply(self, request):
        return request.filter(part_id=self.part.id)

class FilterParameter(Filter):
    def __init__(self, parameter):
        self.parameter = parameter
        super(FilterParameter, self).__init__()
    
    def apply(self, request):
        return request.filter(parameter_id=self.parameter.id)

def _add_default_annotations(request):
    # add the field child_count in request result 
    request = request.select_related('part', 'parameter') # preload for performance
    return request

def find(filters=[]):
    request = api.models.PartParameter.objects
    
    request = _add_default_annotations(request)
    
    for filter in filters:
        request = filter.apply(request)
    
    return request.order_by('id').all()

def create(part):
    part_parameter = PartParameter()
    part_parameter.part = part
    
    return part_parameter
