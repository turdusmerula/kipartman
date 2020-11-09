import api.models
from datetime import date, datetime
from helper.filter import Filter
from api.models import PartReference


def _add_default_annotations(request):
    # add the field child_count in request result 
    request = request.select_related('part') # preload for performance
    return request

def find(filters=[]):
    request = api.models.PartReference.objects
    
    request = _add_default_annotations(request)
    
    for filter in filters:
        request = filter.apply(request)
    
    return request.order_by('id').all()

def create(**kwargs):
    part_reference = PartReference(**kwargs)
    
    return part_reference
