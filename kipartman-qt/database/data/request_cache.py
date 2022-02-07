import database.models
from datetime import date, datetime
from django.db.models import Q, Count

from database.models import RequestCache

def find(name, request):
    request = database.models.RequestCache.objects
    
    return request.filter(name=name).filter(request=request).order_by('updated').all()

