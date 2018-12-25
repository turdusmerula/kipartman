import connexion
from swagger_server.models.part_manufacturer import PartManufacturer

from swagger_server.models.error import Error
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

from swagger_server.controllers.helpers import raise_on_error, ControllerError

from swagger_server.controllers.controller_manufacturer import serialize_Manufacturer
from swagger_server.controllers.controller_manufacturer import find_manufacturer

import api.models

def serialize_PartManufacturer(fpart_manufacturer, part_manufacturer=None):
    if part_manufacturer is None:
        part_manufacturer = PartManufacturer()
    serialize_Manufacturer(fpart_manufacturer.manufacturer, part_manufacturer)
    part_manufacturer.part_name = fpart_manufacturer.part_name
    return part_manufacturer

def deserialize_PartManufacturer(part_manufacturer, fpart_manufacturer=None):
    if fpart_manufacturer is None:
        fpart_manufacturer = api.models.PartManufacturer()
    fpart_manufacturer.manufacturer = raise_on_error(find_manufacturer(part_manufacturer.name))
    fpart_manufacturer.name = part_manufacturer.name
    return fpart_manufacturer


def find_part_manufacturers(part_id):
    """
    find_manufacturers
    Return all manufacturers

    :rtype: List[Manufacturer]
    """
    manufacturers = []

    try:
        fpart = api.models.Part.objects.get(pk=part_id)
    except:
        return Error(code=1000, message='Part %d does not exists'%part_id), 403
    
    for fmanufacturer in fpart.manufacturers.all():
        manufacturers.append(serialize_PartManufacturer(fmanufacturer))

    return manufacturers
