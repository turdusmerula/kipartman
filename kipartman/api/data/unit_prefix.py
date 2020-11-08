from api.models import UnitPrefix
from django.db.models import Count
from helper.filter import Filter

class FilterSymbol(Filter):
    def __init__(self, symbol):
        self.symbol = symbol
        super(FilterSymbol, self).__init__()
    
    def apply(self, request):
        
        return request.filter(symbol=self.symbol)

def find(filters=[]):
    request = UnitPrefix.objects
    
    for filter in filters:
        request = filter.apply(request)

    return request.order_by('id').all()

def find_by_id(id):
    request = UnitPrefix.objects
    
    try:
        return request.get(pk=id)
    except:
        return None
