import connexion
from swagger_server.models.part import Part
from swagger_server.models.part_data import PartData
from swagger_server.models.part_ref import PartRef
from swagger_server.models.part_new import PartNew

from swagger_server.models.part_category import PartCategory
from swagger_server.models.part_category_ref import PartCategoryRef

from swagger_server.models.error import Error
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

from swagger_server.controllers.controller_part_category import find_parts_category
from swagger_server.controllers.controller_part_parameter import find_part_parameters, deserialize_PartParameter
from swagger_server.controllers.controller_part_distributor import find_part_distributors
from swagger_server.controllers.controller_manufacturer import deserialize_ManufacturerData
from swagger_server.controllers.controller_part_offer import deserialize_PartOffer

import api.models
#import jsonpickle

def serialize_PartData(fpart, part=None, with_parameters=True):
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
    if fpart.id and with_parameters:
        part.parameters = find_part_parameters(fpart.id)
    #parameters
    #manufacturers
    return part

def serialize_Part(fpart, part=None, with_offers=True, with_parameters=True, with_childs=True):
    if part is None:
        part = Part()
    part.id = fpart.id
    serialize_PartData(fpart, part, with_parameters)
    if fpart.category:
        part.category = find_parts_category(fpart.category.id)
    # extract childs
    if with_childs:
        part.childs = []
        for fchild in fpart.childs.all():
            part.childs.append(find_part(fchild.id))
    part.has_childs = (fpart.childs.count()>0)
    
    if with_offers:
        part.distributors = find_part_distributors(fpart.id)
    
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
    if part.category:
        try:
            fpart.category = api.models.PartCategory.objects.get(pk=part.category.id)
        except:
            return Error(code=1000, message='Category %d does not exists'%part.category.id)

    if part.childs:
        fchilds = []
        for child in part.childs:
            try:
                fchilds.append(api.models.Part.objects.get(pk=child.id))
            except:
                return Error(code=1000, message='Part %d does not exists'%part.id)
        fpart.childs.set(fchilds)
        # recursive check
        while len(fchilds)>0:
            fchild = fchilds.pop()
            if fchild.pk==part.id:
                return Error(code=1000, message='Part cannot be child of itself')
            for fchild in fchild.childs.all():
                fchilds.append(fchild)

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

    try:
        fpart = deserialize_PartNew(part)
    except Error as e:
        return e
    
    fpart.save()
    
    fparameters = []
    if part.parameters:
        for parameter in part.parameters:
            fparameter = deserialize_PartParameter(parameter)
            fparameter.part = fpart
            fparameter.save()
            fparameters.append(fparameter)
        fpart.parameters.set(fparameters)

    foffers = []
    if part.distributors:
        for part_distributor in part.distributors:
            try:
                fdistributor = api.models.Distributor.objects.get(pk=part_distributor.id)
            except:
                return Error(code=1000, message='Distributor %d does not exists'%part_distributor.id)
                
            for offer in part_distributor.offers:
                foffer = deserialize_PartOffer(offer)
                foffer.part = fpart
                foffer.distributor = fdistributor
                foffer.save()
                foffers.append(foffer)
        fpart.offers.set(foffers)
    
    fpart_manufacturers = []
    if part.manufacturers:
        for part_manufacturer in part.manufacturers:
            try:
                fmanufacturer = api.models.Manufacturer.objects.get(pk=part_manufacturer.id)
            except:
                return Error(code=1000, message='Manufacturer %d does not exists'%part_manufacturer.id)
            fpart_manufacturer = api.models.PartManufacturer()
            fpart_manufacturer.part = fpart
            fpart_manufacturer.manufacturer = fmanufacturer
            fpart_manufacturer.save()
            fpart_manufacturers.append(fpart_manufacturer)
        fpart.manufacturers.set(fpart_manufacturers)

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


def find_part(part_id, with_offers=None, with_parameters=None, with_childs=None):
    """
    find_part
    Return a part
    :param part_id: Part id
    :type part_id: int
    :param with_offers: Include offers in answer
    :type with_offers: bool
    :param with_parameters: Include parameters in answer
    :type with_parameters: bool
    :param with_childs: Include childs in answer
    :type with_childs: bool

    :rtype: Part
    """
    try:
        fpart = api.models.Part.objects.get(pk=part_id)
    except:
        return Error(code=1000, message='Part %d does not exists'%part_id)
    
    try:
        part = serialize_Part(fpart, with_offers=with_offers, with_parameters=with_parameters, with_childs=with_childs)
    except Error as e:
        return e
    return part

def find_parts(category=None, with_offers=None, with_parameters=None, with_childs=None):
    """
    find_parts
    Return all parts

    :rtype: List[Part]
    """
    parts = []
    
    fpart_request = api.models.Part.objects
    
    if category:
        fpart_request = fpart_request.filter(category=category)
        
    try:
        for fpart in fpart_request.all():
            parts.append(serialize_Part(fpart, with_offers=with_offers, with_parameters=with_parameters, with_childs=with_childs))
    except Error as e:
        return e

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
        
    fpart.save()
    
    fparameters = []
    if part.parameters:
        # remove all parameters
        api.models.PartParameter.objects.filter(part=part_id).delete()
        # replace by interface ones
        for parameter in part.parameters:
            fparameter = deserialize_PartParameter(parameter)
            fparameter.part = fpart
            fparameter.save()
            fparameters.append(fparameter)
        fpart.parameters.set(fparameters)

    foffers = []
    if part.distributors:
        # remove all part distributors
        api.models.PartOffer.objects.filter(part=part_id).delete()
        # import new values
        for part_distributor in part.distributors:
            try:
                fdistributor = api.models.Distributor.objects.get(pk=part_distributor.id)
            except:
                return Error(code=1000, message='Distributor %d does not exists'%part_distributor.id)
                
            for offer in part_distributor.offers:
                foffer = deserialize_PartOffer(offer)
                foffer.part = fpart
                foffer.distributor = fdistributor
                foffer.save()
                foffers.append(foffer)
        fpart.offers.set(foffers)
    
    fpart_manufacturers = []
    if part.manufacturers:
        # remove all part distributors
        api.models.PartManufacturer.objects.filter(part=part_id).delete()
        # import new values
        for part_manufacturer in part.manufacturers:
            try:
                fmanufacturer = api.models.Manufacturer.objects.get(pk=part_manufacturer.id)
            except:
                return Error(code=1000, message='Manufacturer %d does not exists'%part_manufacturer.id)
            fpart_manufacturer = api.models.PartManufacturer()
            fpart_manufacturer.part = fpart
            fpart_manufacturer.manufacturer = fmanufacturer
            fpart_manufacturer.save()
            fpart_manufacturers.append(fpart_manufacturer)
        fpart.manufacturers.set(fpart_manufacturers)

    return part
