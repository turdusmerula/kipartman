from api.filter import Filter, FilterRequest
import database.models
import database.data
from django.db.models import Count
from django.db.models import Q


def _add_default_annotations(request):
    return request

def find(filters=None):
    request = database.models.Storage.objects
    
    request = _add_default_annotations(request)
    
    if filters is not None:
        request = filters.Apply(request, filter=FilterRequest)
    
    return request.order_by('id').all()
    
# def save(storage):
#     storage.save()
#
#
# def create():
#     storage = Storage()
#
#     return storage
#
# def delete(storage):
#     database.data.part_storage.find([database.data.part_storage.FilterStorage(storage)]).delete()
#
#     storage.delete()
#

