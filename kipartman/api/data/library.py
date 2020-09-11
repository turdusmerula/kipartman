from api.models import Library
from django.db.models import Count
from helper.filter import Filter


def find():
    request = Library.objects
        
    return request.order_by('id').all()

def create():
    library = Library()
    
    return library

def save(library):
    library.save()
