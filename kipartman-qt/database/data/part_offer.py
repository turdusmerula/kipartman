import database.models
from datetime import date, datetime
from helper.filter import Filter
from database.models import PartOffer

class FilterDistributor(Filter):
    def __init__(self, distributor):
        self.distributor = distributor
        super(FilterDistributor, self).__init__()
     
    def apply(self, request):
        return request.filter(distributor_id=self.distributor.id)

def _add_default_annotations(request):
    # add the field child_count in request result 
    request = request.select_related('part', 'distributor') # preload for performance
    return request

def find(filters=[]):
    request = database.models.PartOffer.objects
    
    request = _add_default_annotations(request)
    
    for filter in filters:
        request = filter.apply(request)
    
    return request.order_by('id').all()

def create(**kwargs):
    part_offer = PartOffer(**kwargs)
    
    return part_offer
