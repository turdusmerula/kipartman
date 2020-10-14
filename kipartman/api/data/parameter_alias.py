import api.models
import api.data
from django.db.models import Count
from helper.filter import Filter
from django.db.models import Q


def find(filters=[]):
    request = api.models.Parameter.objects
    
    for filter in filters:
        request = filter.apply(request)
    
    return request.order_by('id').all()

def create():
    return api.models.ParameterAlias()

