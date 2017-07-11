import connexion
from swagger_server.models.footprint import Footprint
from swagger_server.models.footprint_data import FootprintData
from swagger_server.models.footprint_new import FootprintNew

from swagger_server.models.footprint_category import FootprintCategory
from swagger_server.models.footprint_category_ref import FootprintCategoryRef

from swagger_server.models.error import Error
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

from swagger_server.controllers.controller_footprint_category import find_footprints_category

import api.models
#import jsonpickle

def serialize_FootprintData(ffootprint, footprint=None):
    if footprint is None:
        footprint = FootprintData()
    footprint.name = ffootprint.name
    footprint.description = ffootprint.description
    footprint.comment = ffootprint.comment
    if ffootprint.snapeda:
        footprint.snapeda = ffootprint.snapeda
    return footprint

def serialize_Footprint(ffootprint, footprint=None):
    if footprint is None:
        footprint = Footprint()
    footprint.id = ffootprint.id
    serialize_FootprintData(ffootprint, footprint)
    if ffootprint.category:
        footprint.category = find_footprints_category(ffootprint.category.id)
    return footprint


def deserialize_FootprintData(footprint, ffootprint=None):
    if ffootprint is None:
        ffootprint = api.models.Footprint()
    ffootprint.name = footprint.name
    ffootprint.description = footprint.description
    ffootprint.comment = footprint.comment
    #ffootprint.footprint
    if footprint.snapeda:
        ffootprint.snapeda = footprint.snapeda
    return ffootprint


def deserialize_FootprintNew(footprint, ffootprint=None):
    ffootprint = deserialize_FootprintData(footprint, ffootprint)
    if footprint.category:
        try:
            ffootprint.category = api.models.FootprintCategory.objects.get(pk=footprint.category.id)
        except:
            return Error(code=1000, message='Category %d does not exists'%footprint.category.id)
    return ffootprint


def add_footprint(footprint, footprint_file=None, image_file=None):
    """
    add_footprint
    Creates a new footprint
    :param footprint: Footprint to add
    :type footprint: dict | bytes
    :param footprint_file: Footprint to upload
    :type footprint_file: werkzeug.datastructures.FileStorage
    :param image_file: Image to upload
    :type image_file: werkzeug.datastructures.FileStorage

    :rtype: Footprint
    """
    if connexion.request.is_json:
        footprint = FootprintNew.from_dict(connexion.request.get_json())

    try:
        ffootprint = deserialize_FootprintNew(footprint)
    except Error as e:
        return e
    
    # TODO footprint_file
    # TODO image_file
    
    ffootprint.save()
    
    return serialize_Footprint(ffootprint)


def delete_footprint(footprint_id):
    """
    delete_footprint
    Delete footprint
    :param footprint_id: Footprint id
    :type footprint_id: int

    :rtype: None
    """
    try:
        ffootprint = api.models.Footprint.objects.get(pk=footprint_id)
    except:
        return Error(code=1000, message='Footprint %d does not exists'%footprint_id)
    # delete footprint
    ffootprint.delete()
    return None


def find_footprint(footprint_id):
    """
    find_footprint
    Return a footprint
    :param footprint_id: Footprint id
    :type footprint_id: int

    :rtype: List[FootprintTree]
    """
    try:
        ffootprint = api.models.Footprint.objects.get(pk=footprint_id)
    except:
        return Error(code=1000, message='Footprint %d does not exists'%footprint_id)
    
    footprint = serialize_Footprint(ffootprint)

    return footprint

def find_footprints():
    """
    find_footprints
    Return all footprints

    :rtype: List[Footprint]
    """
    footprints = []
    
    for ffootprint in api.models.Footprint.objects.all():
        footprints.append(serialize_Footprint(ffootprint))

    return footprints

def update_footprint(footprint_id, footprint, footprint_file=None, image_file=None):
    """
    update_footprint
    Update footprint
    :param footprint_id: Footprint id
    :type footprint_id: int
    :param footprint: Footprint to update
    :type footprint: dict | bytes
    :param footprint_file: Footprint to upload
    :type footprint_file: werkzeug.datastructures.FileStorage
    :param image_file: Image to upload
    :type image_file: werkzeug.datastructures.FileStorage

    :rtype: Footprint
    """
    if connexion.request.is_json:
        footprint = FootprintNew.from_dict(connexion.request.get_json())
    else:
        return Error(code=1000, message='Missing payload')
    try:
        ffootprint = deserialize_FootprintNew(footprint, api.models.Footprint.objects.get(pk=footprint_id))
    except:
        return Error(code=1000, message='Footprint %d does not exists'%footprint_id)        
        
    ffootprint.save()
    
    return footprint
