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

def find(filters=[]):
    request = api.models.PartParameter.objects
    
    for filter in filters:
        request = filter.apply(request)
    
    return request.order_by('id').all()

def create(part):
    part_parameter = PartParameter()
    part_parameter.part = part
    
    return part_parameter
