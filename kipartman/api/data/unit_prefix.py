from api.models import UnitPrefix
from django.db.models import Count
from helper.filter import Filter

def find():
    request = UnitPrefix.objects
    
    return request.order_by('id').all()

def find_by_id(id):
    request = UnitPrefix.objects
    
    try:
        return request.get(pk=id)
    except:
        return None
