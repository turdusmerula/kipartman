from database.models import Storage
from django.db.models import Count
from helper.filter import Filter
from django.db.models import Q
import database.data.part_storage

class StorageException(Exception):
    def __init__(self, error):
        super(StorageException, self).__init__(error)

        
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



def _add_default_annotations(request):
    request = request.select_related('category') # preload for performance
    return request

def find(filters=[]):
    request = Storage.objects
    
    request = _add_default_annotations(request)
    
    for filter in filters:
        request = filter.apply(request)
    
    return request.order_by('id').all()
    
def save(storage):
    storage.save()
    
    
def create():
    storage = Storage()
    
    return storage

def delete(storage):
    database.data.part_storage.find([database.data.part_storage.FilterStorage(storage)]).delete()

    storage.delete()
    
