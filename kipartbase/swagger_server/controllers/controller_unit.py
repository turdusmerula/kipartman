import connexion

from swagger_server.models.unit import Unit
from swagger_server.models.unit_prefix import UnitPrefix

from swagger_server.models.error import Error
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

import api.models
#import jsonpickle

def serialize_Unit(funit, unit=None):
    if unit is None:
        unit = Unit()
    unit.id = funit.id
    unit.name = funit.name
    unit.symbol = funit.symbol
    return unit

def serialize_UnitPrefix(funit_prefix, unit_prefix=None):
    if unit_prefix is None:
        unit_prefix = UnitPrefix()
    unit_prefix.id = funit_prefix.id
    unit_prefix.name = funit_prefix.name
    unit_prefix.symbol = funit_prefix.symbol
    unit_prefix.power = funit_prefix.power
    return unit_prefix


def find_unit(unit_id):
    """
    find_unit
    Return a unit
    :param unit_id: Unit id
    :type unit_id: int

    :rtype: Unit
    """
    try:
        unit = serialize_Unit(api.models.Unit.objects.get(pk=unit_id))
    except:
        return Error(code=1000, message='Unit %d does not exists'%unit_id)

    return unit


def find_unit_prefix(unit_prefix_id):
    """
    find_unit_prefix
    Return a unit prefixes
    :param unit_prefix_id: Unit prefix id
    :type unit_prefix_id: int

    :rtype: UnitPrefix
    """
    try:
        unit_prefix = serialize_UnitPrefix(api.models.UnitPrefix.objects.get(pk=unit_prefix_id))
    except:
        return Error(code=1000, message='Unit prefix %d does not exists'%unit_prefix_id)

    return unit_prefix

def find_unit_prefixes():
    """
    find_unit_prefixes
    Return list of unit prefixes

    :rtype: List[UnitPrefix]
    """
    unit_prefixes = []

    for funit_prefix in api.models.UnitPrefix.objects.all():
        unit_prefixes.append(serialize_UnitPrefix(funit_prefix))
    
    return unit_prefixes


def find_units():
    """
    find_units
    Return list of units

    :rtype: List[Unit]
    """
    units = []

    for funit in api.models.Unit.objects.all():
        units.append(serialize_Unit(funit))
    
    return units

