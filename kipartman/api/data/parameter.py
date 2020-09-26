import api.models
import api.data
from django.db.models import Count
from helper.filter import Filter
from django.db.models import Q

class FilterSearchText(Filter):
    def __init__(self, text):
        self.text = text
        super(FilterSearchText, self).__init__()
    
    def apply(self, request):
        return request.filter(
                    Q(name__contains=self.text) |
                    Q(description__contains=self.text)
                )

    def __str__(self):
        return f"search: {self.text}"

class FilterSearchParameter(Filter):
    def __init__(self, name):
        self.name = name
        super(FilterSearchParameter, self).__init__()
    
    def apply(self, request):
        return request.filter(name=self.name)

    def __str__(self):
        return f"search: {self.text}"

def _add_default_annotations(request):
    # add the field child_count in request result 
    request = request.select_related('unit') # preload for performance
    return request

def find(filters=[]):
    request = api.models.Parameter.objects
    
    request = _add_default_annotations(request)
    
    for filter in filters:
        request = filter.apply(request)
    
    return request.order_by('id').all()

def create():
    return api.models.Parameter()

def save(parameter):
    parameter.save()

def delete(parameter):
    api.data.part_parameter.find([api.data.part_parameter.FilterParameter(parameter)]).delete()

    parameter.delete()