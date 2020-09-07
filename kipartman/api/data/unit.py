from api.models import Unit
from django.db.models import Count
from helper.filter import Filter

def find():
    request = Unit.objects
    
    return request.order_by('id').all()
