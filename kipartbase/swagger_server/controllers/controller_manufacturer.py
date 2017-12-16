import connexion
from swagger_server.models.manufacturer import Manufacturer
from swagger_server.models.manufacturer_data import ManufacturerData
from swagger_server.models.manufacturer_new import ManufacturerNew

from swagger_server.models.error import Error
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

import api.models
#import jsonpickle

def serialize_ManufacturerData(fmanufacturer, manufacturer=None):
    if manufacturer is None:
        manufacturer = ManufacturerData()
    manufacturer.name = fmanufacturer.name
    manufacturer.address = fmanufacturer.address
    manufacturer.website = fmanufacturer.website
    manufacturer.email = fmanufacturer.email
    manufacturer.phone = fmanufacturer.phone
    manufacturer.comment = fmanufacturer.comment
    return manufacturer

def serialize_Manufacturer(fmanufacturer, manufacturer=None):
    if manufacturer is None:
        manufacturer = Manufacturer()
    manufacturer.id = fmanufacturer.id
    serialize_ManufacturerData(fmanufacturer, manufacturer)
    return manufacturer


def deserialize_ManufacturerData(manufacturer, fmanufacturer=None):
    if fmanufacturer is None:
        fmanufacturer = api.models.Manufacturer()
    fmanufacturer.name = manufacturer.name
    fmanufacturer.address = manufacturer.address
    fmanufacturer.website = manufacturer.website
    fmanufacturer.email = manufacturer.email
    fmanufacturer.phone = manufacturer.phone
    fmanufacturer.comment = manufacturer.comment
    return fmanufacturer


def deserialize_ManufacturerNew(manufacturer, fmanufacturer=None):
    fmanufacturer = deserialize_ManufacturerData(manufacturer, fmanufacturer)
    return fmanufacturer


def add_manufacturer(manufacturer):
    """
    add_manufacturer
    Creates a new manufacturer
    :param manufacturer: Manufacturer to add
    :type manufacturer: dict | bytes

    :rtype: Manufacturer
    """
    if connexion.request.is_json:
        manufacturer = ManufacturerNew.from_dict(connexion.request.get_json())

    fmanufacturer = deserialize_ManufacturerNew(manufacturer)
    fmanufacturer.save()
    
    return serialize_Manufacturer(fmanufacturer)


def delete_manufacturer(manufacturer_id):
    """
    delete_manufacturer
    Delete manufacturer
    :param manufacturer_id: Manufacturer id
    :type manufacturer_id: int

    :rtype: None
    """
    try:
        fmanufacturer = api.models.Manufacturer.objects.get(pk=manufacturer_id)
    except:
        return Error(code=1000, message='Manufacturer %d does not exists'%manufacturer_id), 403
    # delete manufacturer
    fmanufacturer.delete()
    return None


def find_manufacturer(manufacturer_id):
    """
    find_manufacturer
    Return a manufacturer
    :param manufacturer_id: Manufacturer id
    :type manufacturer_id: int

    :rtype: Manufacturer
    """
    try:
        fmanufacturer = api.models.Manufacturer.objects.get(pk=manufacturer_id)
    except:
        return Error(code=1000, message='Manufacturer %d does not exists'%manufacturer_id), 403
    
    manufacturer = serialize_Manufacturer(fmanufacturer)
    return manufacturer

def find_manufacturers(name=None):
    """
    find_manufacturers
    Return all manufacturers
    :param name: Search manufacturers matching name
    :type name: str

    :rtype: List[Manufacturer]
    """
    manufacturers = []
    
    fmanufacturer_request = api.models.Manufacturer.objects
    if name:
        fmanufacturer_request = fmanufacturer_request.filter(name=name)
        
    for fmanufacturer in fmanufacturer_request.all():
        manufacturers.append(serialize_Manufacturer(fmanufacturer))

    return manufacturers

def update_manufacturer(manufacturer_id, category):
    """
    update_manufacturer
    Update a manufacturer
    :param manufacturer_id: Manufacturer id
    :type manufacturer_id: int
    :param category: Manufacturer to update
    :type category: dict | bytes

    :rtype: Manufacturer
    """
    if connexion.request.is_json:
        manufacturer = ManufacturerNew.from_dict(connexion.request.get_json())
    else:
        return Error(code=1000, message='Missing payload'), 403
    try:
        fmanufacturer = deserialize_ManufacturerNew(manufacturer, api.models.Manufacturer.objects.get(pk=manufacturer_id))
    except:
        return Error(code=1000, message='Manufacturer %d does not exists'%manufacturer_id), 403
        
    fmanufacturer.save()
    
    return manufacturer
