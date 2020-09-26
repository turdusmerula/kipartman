from api.models import Unit
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
                    Q(symbol__contains=self.text)
                )

    def __str__(self):
        return f"search: {self.text}"

class FilterSearchUnit(Filter):
    def __init__(self, name):
        self.name = name
        super(FilterSearchUnit, self).__init__()
    
    def apply(self, request):
        return request.filter(name=self.name)

    def __str__(self):
        return f"search: {self.text}"

def find(filters=[]):
    request = Unit.objects
    
    for filter in filters:
        request = filter.apply(request)
    
    return request.order_by('id').all()
