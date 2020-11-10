import api.models
from datetime import date, datetime
from helper.filter import Filter
from api.models import PartParameter
from helper.unit import format_unit_prefix, format_float

class FilterPart(Filter):
    def __init__(self, part):
        self.part = part
        super(FilterPart, self).__init__()
    
    def apply(self, request):
        return request.filter(part_id=self.part.id)

class FilterParameter(Filter):
    def __init__(self, parameter):
        self.parameter = parameter
        super(FilterParameter, self).__init__()
    
    def apply(self, request):
        return request.filter(parameter_id=self.parameter.id)

def _add_default_annotations(request):
    # add the field child_count in request result 
    request = request.select_related('part', 'parameter') # preload for performance
    return request

def find(filters=[]):
    request = api.models.PartParameter.objects
    
    request = _add_default_annotations(request)
    
    for filter in filters:
        request = filter.apply(request)
    
    return request.order_by('id').all()

def create(**kwargs):
    part_parameter = PartParameter(**kwargs)
    
    return part_parameter


def expanded_parameter_value(part_parameter, with_operator=False):
    operator = ""
    if with_operator==True and part_parameter.operator is not None:
        operator = part_parameter.operator
        
    if part_parameter.parameter.value_type==api.models.ParameterType.TEXT:
        return operator+part_parameter.text_value
    else:
        if part_parameter.value is not None:
            unit_symbol = ''
            if part_parameter.parameter.unit is not None:
                unit_symbol = part_parameter.parameter.unit.symbol
            
            if part_parameter.parameter.value_type==api.models.ParameterType.INTEGER:
                return operator+str(int(part_parameter.value))+unit_symbol
            if part_parameter.parameter is not None and part_parameter.parameter.unit is not None:
                if part_parameter.parameter.unit.prefixable==True:
                    prefix = None
                    if part_parameter.prefix is not None:
                        prefix = part_parameter.prefix.symbol
                    return operator+format_unit_prefix(part_parameter.value, unit_symbol, prefix)
            return operator+format_float(part_parameter.value, 3)+unit_symbol
    return None
