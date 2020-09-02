import api.models
from datetime import date, datetime
from helper.filter import Filter

class FilterPart(Filter):
    def __init__(self, part):
        self.part = part
        super(FilterPart, self).__init__()
    
    def apply(self, request):
        return request.filter(part_id=self.part.id)

def find(filters=[]):
    request = api.models.PartParameter.objects
    
    for filter in filters:
        request = filter.apply(request)
    
    return request.order_by('id').all()

