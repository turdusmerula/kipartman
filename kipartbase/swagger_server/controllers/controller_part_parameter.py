import connexion
from swagger_server.models.part_parameter import PartParameter
from swagger_server.models.part_parameter_data import PartParameterData
from swagger_server.models.part_parameter_description import PartParameterDescription
from swagger_server.models.unit import Unit
from swagger_server.models.unit_prefix import UnitPrefix

from swagger_server.models.error import Error
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

from swagger_server.controllers.controller_unit import find_unit, find_unit_prefix
from swagger_server.controllers.helpers import raise_on_error

from django.db.models import Q
import api.models
#import jsonpickle

def serialize_PartParameterDescription(fpart_parameter, part_parameter=None):
    if part_parameter is None:
        part_parameter = PartParameterDescription()
    part_parameter.name = fpart_parameter['name']
    part_parameter.description = fpart_parameter['description']
    if fpart_parameter['unit']:
        part_parameter.unit = raise_on_error(find_unit(fpart_parameter['unit']))
    part_parameter.numeric = fpart_parameter['numeric']
    return part_parameter

def serialize_PartParameterData(fpart_parameter, part_parameter=None):
    if part_parameter is None:
        part_parameter = PartParameterData()
    part_parameter.name = fpart_parameter.name
    part_parameter.description = fpart_parameter.description
    if fpart_parameter.unit:
        part_parameter.unit = raise_on_error(find_unit(fpart_parameter.unit.id))
    part_parameter.numeric = fpart_parameter.numeric
    if fpart_parameter.text_value:
        part_parameter.text_value = fpart_parameter.text_value
    if fpart_parameter.min_value:
        part_parameter.min_value = fpart_parameter.min_value
    if fpart_parameter.min_prefix:
        part_parameter.min_prefix = raise_on_error(find_unit_prefix(fpart_parameter.min_prefix.id))
    if fpart_parameter.nom_value:
        part_parameter.nom_value = fpart_parameter.nom_value
    if fpart_parameter.nom_prefix:
        part_parameter.nom_prefix = raise_on_error(find_unit_prefix(fpart_parameter.nom_prefix.id))
    if fpart_parameter.max_value:
        part_parameter.max_value = fpart_parameter.max_value
    if fpart_parameter.max_prefix:
        part_parameter.max_prefix = raise_on_error(find_unit_prefix(fpart_parameter.max_prefix.id)) 
    return part_parameter

def serialize_PartParameter(fpart_parameter, part_parameter=None):
    if part_parameter is None:
        part_parameter = PartParameter()
    part_parameter.id = fpart_parameter.id
    serialize_PartParameterData(fpart_parameter, part_parameter)
    return part_parameter

def deserialize_PartParameterData(part_parameter, fpart_parameter=None):
    if fpart_parameter is None:
        fpart_parameter = api.models.PartParameter()
    fpart_parameter.name = part_parameter.name
    fpart_parameter.description = part_parameter.description
    if part_parameter.unit:
        try:
            fpart_parameter.unit = api.models.Unit.objects.get(pk=part_parameter.unit.id)
        except:
            raise Error(code=1000, message='Unit %d does not exists'%part_parameter.unit.id)
    fpart_parameter.numeric = part_parameter.numeric
    if part_parameter.text_value:
        fpart_parameter.text_value = part_parameter.text_value
    if part_parameter.min_value:
        fpart_parameter.min_value = part_parameter.min_value
    if part_parameter.min_prefix:
        try:
            fpart_parameter.min_prefix = api.models.UnitPrefix.objects.get(pk=part_parameter.min_prefix.id)
        except:
            raise Error(code=1000, message='Unit prefix %d does not exists'%part_parameter.min_prefix.id)
    if part_parameter.nom_value:
        fpart_parameter.nom_value = part_parameter.nom_value
    if part_parameter.nom_prefix:
        try:
            fpart_parameter.nom_prefix = api.models.UnitPrefix.objects.get(pk=part_parameter.nom_prefix.id)
        except:
            raise Error(code=1000, message='Unit prefix %d does not exists'%part_parameter.nom_prefix.id)
    if part_parameter.max_value:
        fpart_parameter.max_value = part_parameter.max_value
    if part_parameter.max_prefix:
        try:
            fpart_parameter.max_prefix = api.models.UnitPrefix.objects.get(pk=part_parameter.max_prefix.id)
        except:
            raise Error(code=1000, message='Unit prefix %d does not exists'%part_parameter.max_prefix.id)
    return fpart_parameter

def deserialize_PartParameter(part_parameter, fpart_parameter=None):
    fpart_parameter = deserialize_PartParameterData(part_parameter, fpart_parameter)
    return fpart_parameter


def add_part_parameters(part_id, parameters):
    """
    add_part_parameters
    Create some new part parameters
    :param part_id: Part id
    :type part_id: int
    :param parameters: Parameters to add
    :type parameters: list | bytes

    :rtype: List[PartParameter]
    """
    if connexion.request.is_json:
        parameters = [PartParameter.from_dict(d) for d in connexion.request.get_json()]
    
    try:
        fpart = api.models.Part.objects.get(pk=part_id)
    except:
        return Error(code=1000, message='Part %d does not exists'%part_id), 403

    fparameters = []
    for parameter in parameters:
        try:
            fparameters.append(deserialize_PartParameter(parameter))
        except Error as e:
            return e.error, 403
        fpart.parameters.set(fparameters)
    
    return None

def delete_part_parameter(part_id, parameter_id):
    """
    delete_part_parameter
    Delete part parameter
    :param part_id: Part id
    :type part_id: int
    :param parameter_id: Parameter id
    :type parameter_id: int

    :rtype: None
    """
    try:
        fpart_parameter = api.models.PartParameter.objects.get(part=part_id, pk=parameter_id)
    except:
        return Error(code=1000, message='Part parameter %d for part %d does not exists'%(parameter_id, part_id)), 403
    fpart_parameter.delete()
    
    return None

def delete_part_parameters(part_id, parameters):
    """
    delete_part_parameters
    Delete list of part parameters
    :param part_id: Part id
    :type part_id: int
    :param parameters: Parameters to delete
    :type parameters: list | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        parameters = [PartParameter.from_dict(d) for d in connexion.request.get_json()]

    fparameters_id = []
    for parameter in parameters:
        if parameter.id:
            fparameters_id.append(parameter.id)

    try:
        api.models.PartParameter.objects.filter(part=part_id).filter(id__in=fparameters_id).delete()
    except:
        return Error(code=1000, message='Deleting parameters failed'), 403
        
    return None

def find_part_parameter(part_id, parameter_id):
    """
    find_part_parameter
    Return a part parameter
    :param part_id: Part id
    :type part_id: int
    :param parameter_id: Parameter id
    :type parameter_id: int

    :rtype: List[PartParameter]
    """
    try:
        fpart_parameter = api.models.PartParameter.objects.get(part=part_id, pk=parameter_id)
    except:
        return Error(code=1000, message='Part parameter %d for part %d does not exists'%(parameter_id, part_id)), 403

    return serialize_PartParameter(fpart_parameter)

def find_parts_parameters(search=None):
    """
    find_parts_parameters
    Return all available parts parameters
    :param search: Search parameter matching value
    :type search: str

    :rtype: List[PartParameterDescription]
    """
    parameters = []
    
    fparameters_request = api.models.PartParameter.objects
    
    if search:
        fparameters_request = fparameters_request.filter(
                    Q(name__contains=search) |
                    Q(description__contains=search)
                )
    
#    fparameters = api.models.PartParameter.objects.order_by().values('name').distinct()
    fparameters = fparameters_request.values('name', 'description', 'unit', 'numeric').order_by('name', 'description', 'unit', 'numeric').distinct()
    
    try:
        for fparameter in fparameters:
            print fparameter
            parameters.append(serialize_PartParameterDescription(fparameter))
    except Error as e:
        return e.error, 403
        
    return parameters

def find_part_parameters(part_id):
    """
    find_part_parameters
    Return all parameters for part
    :param part_id: Part id
    :type part_id: int

    :rtype: List[PartParameter]
    """
    parameters = []
    
    try:
        fpart = api.models.Part.objects.get(pk=part_id)
    except:
        return Error(code=1000, message='Part %d does not exists'%part_id), 403
    
    for fparameter in fpart.parameters.all():
        parameters.append(serialize_PartParameter(fparameter))
        
    return parameters

def update_part_parameter(part_id, parameter_id, category):
    """
    update_part_parameter
    Update part parameter
    :param part_id: Part id
    :type part_id: int
    :param parameter_id: Parameter id
    :type parameter_id: int
    :param category: Parameter to update
    :type category: dict | bytes

    :rtype: PartParameter
    """
    if connexion.request.is_json:
        category = PartParameter.from_dict(connexion.request.get_json())
    return 'do some magic!'


def update_part_parameters(part_id, parameters):
    """
    update_part_parameters
    Update list of part parameters
    :param part_id: Part id
    :type part_id: int
    :param parameters: Parameters to update
    :type parameters: list | bytes

    :rtype: List[PartParameter]
    """
    if connexion.request.is_json:
        parameters = [PartParameter.from_dict(d) for d in connexion.request.get_json()]
    return 'do some magic!'
