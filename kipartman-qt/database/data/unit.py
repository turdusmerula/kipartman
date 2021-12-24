from database.models import Unit
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
        return f"search: {self.name}"

class FilterSearchSymbol(Filter):
    def __init__(self, symbol):
        self.symbol = symbol
        super(FilterSearchSymbol, self).__init__()
    
    def apply(self, request):
        return request.filter(symbol=self.symbol)

    def __str__(self):
        return f"search: {self.symbol}"

def find(filters=[]):
    request = Unit.objects
    
    for filter in filters:
        request = filter.apply(request)
    
    return request.order_by('id').all()

def create():
    return Unit()

def save(unit):
    unit.save()

def delete(unit):
    unit.delete()
