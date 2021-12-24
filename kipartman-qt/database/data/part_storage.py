import database.models
from datetime import date, datetime
from helper.filter import Filter
from database.models import PartStorage

# class FilterPart(Filter):
#     def __init__(self, part):
#         self.part = part
#         super(FilterPart, self).__init__()
#     
#     def apply(self, request):
#         return request.filter(part_id=self.part.id)
# 
class FilterStorage(Filter):
    def __init__(self, storage):
        self.storage = storage
        super(FilterStorage, self).__init__()
     
    def apply(self, request):
        return request.filter(storage_id=self.storage.id)

class FilterPartStorage(Filter):
    def __init__(self, id):
        self.id = id
        super(FilterPartStorage, self).__init__()
     
    def apply(self, request):
        return request.filter(id=self.id)

def _add_default_annotations(request):
    # add the field child_count in request result 
    request = request.select_related('part', 'storage') # preload for performance
    return request

def find(filters=[]):
    request = database.models.PartStorage.objects
    
    request = _add_default_annotations(request)
    
    for filter in filters:
        request = filter.apply(request)
    
    return request.order_by('id').all()

def create(part, **kwargs):
    part_parameter = PartStorage(**kwargs)
    part_parameter.part = part
    
    return part_parameter
