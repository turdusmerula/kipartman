import database.models
import database.data
from django.db.models import Count
from helper.filter import Filter
from django.db.models import Q

class FilterParameter(Filter):
    def __init__(self, parameter):
        self.parameter = parameter
        super(FilterName, self).__init__()
    
    def apply(self, request):
        return request.filter(parameter_id=self.parameter.id)

class FilterName(Filter):
    def __init__(self, name):
        self.name = name
        super(FilterName, self).__init__()
    
    def apply(self, request):
        return request.filter(name=self.name)

def find(filters=[]):
    request = database.models.ParameterAlias.objects
    
    for filter in filters:
        request = filter.apply(request)
    
    return request.order_by('id').all()

def create():
    return database.models.ParameterAlias()

