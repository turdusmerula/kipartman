import api.models
import api.data
from django.db.models import Count
from helper.filter import Filter
from django.db.models import Q

class FilterSearchText(Filter):
    def __init__(self, text):
        self.text = text
        super(FilterSearchText, self).__init__()
    
    def apply(self, request):
        return request.filter(
                    Q(name__contains=self.text) |
                    Q(address__contains=self.text) |
                    Q(website__contains=self.text) |
                    Q(email__contains=self.text) |
                    Q(phone__contains=self.text) |
                    Q(comment__contains=self.text) 
                )

    def __str__(self):
        return f"search: {self.text}"

class FilterSearchManufacturer(Filter):
    def __init__(self, name):
        self.name = name
        super(FilterSearchManufacturer, self).__init__()
    
    def apply(self, request):
        return request.filter(name=self.name)

    def __str__(self):
        return f"search: {self.text}"

def find(filters=[]):
    request = api.models.Manufacturer.objects
        
    for filter in filters:
        request = filter.apply(request)
    
    return request.order_by('id').all()

def create():
    return api.models.Manufacturer()

def save(manufacturer):
    manufacturer.save()

def delete(manufacturer):
    api.data.part_manufacturer.find([api.data.part_manufacturer.FilterManufacturer(manufacturer)]).delete()
    manufacturer.delete()