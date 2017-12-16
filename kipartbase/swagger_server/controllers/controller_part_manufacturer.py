import connexion
from swagger_server.models.part_manufacturer import PartManufacturer

from swagger_server.models.error import Error
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

from swagger_server.controllers.controller_manufacturer import serialize_Manufacturer

import api.models
#import jsonpickle

def serialize_PartManufacturer(fmanufacturer, part_manufacturer=None):
    if part_manufacturer is None:
        part_manufacturer = PartManufacturer()
    serialize_Manufacturer(fmanufacturer.manufacturer, part_manufacturer)
    part_manufacturer.part_name = fmanufacturer.part_name
    return part_manufacturer

    
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
