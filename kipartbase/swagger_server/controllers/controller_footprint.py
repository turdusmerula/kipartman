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

from swagger_server.controllers.controller_footprint_category import find_footprints_category,\
    find_footprints_categories
from swagger_server.controllers.controller_upload_file import find_upload_file
from swagger_server.controllers.helpers import raise_on_error, ControllerError

import api.models
from django.db.models import Q
#import jsonpickle
def serialize_FootprintData(ffootprint, footprint=None):
    if footprint is None:
        footprint = FootprintData()
    footprint.name = ffootprint.name
    footprint.description = ffootprint.description
    footprint.comment = ffootprint.comment
    if ffootprint.snapeda:
        footprint.snapeda = ffootprint.snapeda
    if ffootprint.snapeda_uid:
        footprint.snapeda_uid = ffootprint.snapeda_uid
    if ffootprint.updated:
        footprint.updated = ffootprint.updated
    return footprint

def serialize_Footprint(ffootprint, footprint=None):
    if footprint is None:
        footprint = Footprint()
    footprint.id = ffootprint.id
    serialize_FootprintData(ffootprint, footprint)
    if ffootprint.category:
        footprint.category = raise_on_error(find_footprints_category(ffootprint.category.id))
    if ffootprint.image:
        footprint.image = raise_on_error(find_upload_file(ffootprint.image.id))
    if ffootprint.footprint:
        footprint.footprint = raise_on_error(find_upload_file(ffootprint.footprint.id))
    return footprint


def deserialize_FootprintData(footprint, ffootprint=None):
    if ffootprint is None:
        ffootprint = api.models.Footprint()
    ffootprint.name = footprint.name
    ffootprint.description = footprint.description
    ffootprint.comment = footprint.comment
    if footprint.snapeda:
        ffootprint.snapeda = footprint.snapeda
    if footprint.snapeda_uid:
        ffootprint.snapeda_uid = footprint.snapeda_uid
    if footprint.updated:
        ffootprint.updated = footprint.updated
    return ffootprint


def deserialize_FootprintNew(footprint, ffootprint=None):
    ffootprint = deserialize_FootprintData(footprint, ffootprint)
    if footprint.category:
        try:
            ffootprint.category = api.models.FootprintCategory.objects.get(id=footprint.category.id)
        except:
            raise_on_error(Error(code=1000, message='Category %d does not exists'%footprint.category.id))
    else:
        ffootprint.category = None
        
    if footprint.image:
        try:
            ffootprint.image = api.models.File.objects.get(id=footprint.image.id)
        except:
            raise_on_error(Error(code=1000, message='Image %d does not exists'%footprint.image.id))
    else:
        ffootprint.image = None
        
    if footprint.footprint:
        try:
            ffootprint.footprint = api.models.File.objects.get(id=footprint.footprint.id)
        except:
            raise_on_error(Error(code=1000, message='Footprint %d does not exists'%footprint.footprint.id))
    else:
        ffootprint.footprint = None

    return ffootprint


def add_footprint(footprint):
    """
    add_footprint
    Creates a new footprint
    :param footprint: Footprint to add
    :type footprint: dict | bytes

    :rtype: Footprint
    """
    if connexion.request.is_json:
        footprint = FootprintNew.from_dict(connexion.request.get_json())

    try:
        ffootprint = deserialize_FootprintNew(footprint)
    except ControllerError as e:
        return e.error

        
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

    :rtype: Footprint
    """
    try:
        ffootprint = api.models.Footprint.objects.get(pk=footprint_id)
    except:
        return Error(code=1000, message='Footprint %d does not exists'%footprint_id)
    
    try:
        footprint = serialize_Footprint(ffootprint)
    except ControllerError as e:
        return e.error
    
    return footprint

def find_footprints(category=None, search=None):
    """
    find_footprints
    Return all footprints
    :param category: Filter by category
    :type category: int
    :param search: Search for footprint matching pattern
    :type search: str

    :rtype: List[Footprint]
    """
    footprints = []
    
    ffootprint_query = api.models.Footprint.objects
    
    if search:
        ffootprint_query = ffootprint_query.filter(
                    Q(name__contains=search) |
                    Q(description__contains=search) |
                    Q(comment__contains=search)
                )

    if category:
        # extract category
        categories = api.models.FootprintCategory.objects.get(pk=int(category)).get_descendants(include_self=True)
        category_ids = [category.id for category in categories]
        # add a category filter
        ffootprint_query = ffootprint_query.filter(category__in=category_ids)

    for ffootprint in ffootprint_query.all():
        footprints.append(serialize_Footprint(ffootprint))

    return footprints

def update_footprint(footprint_id, footprint):
    """
    update_footprint
    Update footprint
    :param footprint_id: Footprint id
    :type footprint_id: int
    :param footprint: Footprint to update
    :type footprint: dict | bytes

    :rtype: Footprint
    """
    if connexion.request.is_json:
        footprint = FootprintNew.from_dict(connexion.request.get_json())
    else:
        return Error(code=1000, message='Missing payload')

    try:
        ffootprint = api.models.Footprint.objects.get(pk=footprint_id)
    except:
        return Error(code=1000, message='Footprint %d does not exists'%footprint_id)        

    try:
        ffootprint = deserialize_FootprintNew(footprint, ffootprint)
    except ControllerError as e:
        return e.error

    ffootprint.save()
    
    return serialize_Footprint(ffootprint)
