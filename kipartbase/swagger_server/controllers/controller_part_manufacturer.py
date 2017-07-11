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
    serialize_Manufacturer(fmanufacturer, part_manufacturer)
    return part_manufacturer

    
def find_part_manufacturers(part_id):
    """
    find_manufacturers
    Return all manufacturers

    :rtype: List[Manufacturer]
    """
    manufacturers_id = []
    
    for fmanufacturer in api.models.PartOffer.objects.filter(part=part_id).values('manufacturer').distinct():
        manufacturers_id.append(fmanufacturer['manufacturer'])
    
    manufacturers = []
    for fmanufacturer in api.models.Manufacturer.objects.filter(pk__in=manufacturers_id).all():
        manufacturer = serialize_PartManufacturer(fmanufacturer)
        manufacturers.append(manufacturer)

    return manufacturers
