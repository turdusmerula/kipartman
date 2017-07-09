import connexion
from swagger_server.models.part import Part
from swagger_server.models.part_data import PartData
from swagger_server.models.part_ref import PartRef
from swagger_server.models.part_new import PartNew
from swagger_server.models.part_tree import PartTree

from swagger_server.models.part_category import PartCategory
from swagger_server.models.part_category_ref import PartCategoryRef
from swagger_server.models.part_category_tree import PartCategoryTree

from swagger_server.models.error import Error
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

from swagger_server.controllers.controller_part_category import find_parts_category
from swagger_server.controllers.controller_part_parameter import find_part_parameters

import api.models
#import jsonpickle

def serialize_PartData(fpart, part=None):
    if part is None:
        part = PartData()
    part.name = fpart.name
    part.description = fpart.description
    part.comment = fpart.comment
    if fpart.octopart:
        part.octopart = fpart.octopart
    if fpart.updated:
        part.updated = fpart.updated
    #part.footprint
    if fpart.id:
        part.parameters = find_part_parameters(fpart.id)
    #parameters
    #distributors
    #manufacturers
    return part

def serialize_Part(fpart, part=None):
    if part is None:
        part = Part()
    part.id = fpart.id
    serialize_PartData(fpart, part)
    if fpart.category:
        part.category = PartCategoryRef(fpart.category.id)
    part.has_childs = (fpart.childs.count()>0)
    return part

def serialize_PartTree(fpart, part=None):
    if part is None:
        part = PartTree()
    part.id = fpart.id
    serialize_PartData(fpart, part)
    if fpart.category:
        part.category = PartCategoryTree(fpart.category.id)
    if fpart.childs.count()>0:
        part.childs = []
    part.has_childs = (fpart.childs.count()>0)
    return part


def deserialize_PartData(part, fpart=None):
    if fpart is None:
        fpart = api.models.Part()
    fpart.name = part.name
    fpart.descrition = part.description
    fpart.comment = part.comment
    #fpart.footprint
    if part.octopart:
        fpart.octopart
    if part.updated:
        fpart.updated
    #parameters
    #distributors
    #manufacturers
    return fpart


def deserialize_PartNew(part, fpart=None):
    fpart = deserialize_PartData(part, fpart)
    if part.parent:
        fpart.parent
    if part.category:
        fpart.category
    return fpart


def add_part(part):
    """
    add_part
    Creates a new part
    :param part: Part to add
    :type part: dict | bytes

    :rtype: Part
    """
    if connexion.request.is_json:
        part = PartNew.from_dict(connexion.request.get_json())

    fpart = deserialize_PartNew(part)
    if part.category:
        try:
            fpart.category = api.models.PartCategory.objects.get(pk=part.category.id)
        except:
            return Error(code=1000, message='Category %d does not exists'%part.category.id)
    if part.childs:
        childs = []
        for child in part.childs:
            try:
                childs.append(api.models.Part.objects.get(pk=child.id))
            except:
                return Error(code=1000, message='Part %d does not exists'%part.id)
        fpart.childs.set(childs)
    fpart.save()
    
    return serialize_Part(fpart)


def delete_part(part_id):
    """
    delete_part
    Delete part
    :param part_id: Part id
    :type part_id: int

    :rtype: None
    """
    try:
        fpart = api.models.Part.objects.get(pk=part_id)
    except:
        return Error(code=1000, message='Part %d does not exists'%part_id)
    # delete part
    fpart.delete()
    return None


def find_part(part_id):
    """
    find_part
    Return a part
    :param part_id: Part id
    :type part_id: int

    :rtype: List[PartTree]
    """
    try:
        fpart = api.models.Part.objects.get(pk=part_id)
    except:
        return Error(code=1000, message='Part %d does not exists'%part_id)
    
    part = serialize_PartTree(fpart)
    if fpart.category:
        part.category = find_parts_category(fpart.category.id)

    # extract childs
    if part.has_childs:
        part.childs = []
    for fchild in fpart.childs.all():
        part.childs.append(find_part(fchild.id))
    return part

def find_parts():
    """
    find_parts
    Return all parts

    :rtype: List[Part]
    """
    parts = []
    
    for fpart in api.models.Part.objects.all():
        parts.append(serialize_Part(fpart))

    return parts

def update_part(part_id, part):
    """
    update_part
    Update part
    :param part_id: Part id
    :type part_id: int
    :param part: Part to update
    :type part: dict | bytes

    :rtype: Part
    """
    if connexion.request.is_json:
        part = PartNew.from_dict(connexion.request.get_json())
    else:
        return Error(code=1000, message='Missing payload')
    try:
        fpart = deserialize_PartNew(part, api.models.Part.objects.get(pk=part_id))
    except:
        return Error(code=1000, message='Part %d does not exists'%part_id)

    if part.childs:
        # check there is no recursion
        fchilds = []
        for child in part.childs:
            try:
                fchild = api.models.Part.objects.get(pk=child.id)
            except:
                return Error(code=1000, message='Part %d does not exists'%child.id)
            fchilds.append(fchild)
        fpart.childs.set(fchilds)
        # recursive check
        while len(fchilds)>0:
            fchild = fchilds.pop()
            if fchild.pk==part.id:
                return Error(code=1000, message='Part cannot be child of itself')
            for fchild in fchild.childs.all():
                fchilds.append(fchild)
        
        
    fpart.save()
    
    return part
