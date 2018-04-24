import connexion
from swagger_server.models.part import Part
from swagger_server.models.part_data import PartData
from swagger_server.models.part_ref import PartRef
from swagger_server.models.part_new import PartNew

from swagger_server.models.part_category import PartCategory
from swagger_server.models.part_category_ref import PartCategoryRef
from swagger_server.models.part_attachement import PartAttachement

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

from django.db.models import Q
import api.models
from swagger_server.controllers.controller_part_manufacturer import find_part_manufacturers
from swagger_server.controllers.controller_part_storage import find_part_storages
from swagger_server.controllers.controller_upload_file import find_upload_file
from swagger_server.controllers.helpers import raise_on_error, ControllerError
from swagger_server.controllers.controller_versioned_file import find_versioned_file

def serialize_PartData(fpart, part=None, with_parameters=True):
    if part is None:
        part = PartData()
    part.name = fpart.name
    part.description = fpart.description
    part.comment = fpart.comment
    if fpart.octopart:
        part.octopart = fpart.octopart
    if fpart.octopart_uid:
        part.octopart_uid = fpart.octopart_uid
    if fpart.updated:
        part.updated = fpart.updated
    if fpart.id and with_parameters:
        part.parameters = raise_on_error(find_part_parameters(fpart.id))
    return part

def serialize_Part(fpart, part=None, with_offers=True, with_parameters=True, with_childs=True, with_distributors=True, with_manufacturers=True, with_storages=True, with_attachements=True):
    if part is None:
        part = Part()
    part.id = fpart.id
    serialize_PartData(fpart, part, with_parameters)
    if fpart.category:
        part.category = raise_on_error(find_parts_category(fpart.category.id))
    if fpart.footprint:
        part.footprint = raise_on_error(find_versioned_file(fpart.footprint.id))
    if fpart.symbol:
        part.symbol = raise_on_error(find_versioned_file(fpart.symbol.id))
    # extract childs
    if with_childs:
        part.childs = []
        for fchild in fpart.childs.all():
            part.childs.append(raise_on_error(find_part(fchild.id, with_offers=with_offers, with_parameters=with_parameters, with_childs=with_childs, with_distributors=with_distributors, with_manufacturers=with_manufacturers, with_storages=with_storages, with_attachements=with_attachements)))
    part.has_childs = (fpart.childs.count()>0)
    
    if with_distributors:
        part.distributors = raise_on_error(find_part_distributors(fpart.id))
    
    if with_manufacturers:
        part.manufacturers = raise_on_error(find_part_manufacturers(fpart.id))

    if with_storages:
        part.storages = raise_on_error(find_part_storages(fpart.id))

    if with_attachements:
        part.attachements = []
        for fattachement in fpart.attachements.all():
            file = raise_on_error(find_upload_file(fattachement.file.id))
            attachement = PartAttachement()
            attachement.id = fattachement.file.id
            attachement.description = fattachement.description
            attachement.source_name = file.source_name
            attachement.storage_path = file.storage_path
            part.attachements.append(attachement)

    return part


def deserialize_PartData(part, fpart=None):
    if fpart is None:
        fpart = api.models.Part()
    fpart.name = part.name
    fpart.description = part.description
    fpart.comment = part.comment
    if part.octopart:
        fpart.octopart = part.octopart
    if part.octopart_uid:
        fpart.octopart_uid = part.octopart_uid
    if part.updated:
        fpart.updated = part.updated
    return fpart


def deserialize_PartNew(part, fpart=None):
    fpart = deserialize_PartData(part, fpart)
    if part.category:
        try:
            fpart.category = api.models.PartCategory.objects.get(pk=part.category.id)
        except:
            raise_on_error(Error(code=1000, message='Category %d does not exists'%part.category.id))
    else:
        fpart.category = None

    if part.footprint:
        try:
            fpart.footprint = api.models.VersionedFile.objects.get(pk=part.footprint.id)
        except:
            raise_on_error(Error(code=1000, message='Footprint %d does not exists'%part.footprint.id))
    else:
        fpart.footprint = None

    if part.symbol:
        try:
            fpart.symbol = api.models.VersionedFile.objects.get(pk=part.symbol.id)
        except:
            raise_on_error(Error(code=1000, message='Symbol %d does not exists'%part.symbol.id))
    else:
        fpart.symbol = None

    if not part.childs is None:
        fchilds = []
        fchilds_check = []
        for child in part.childs:
            try:
                fchild = api.models.Part.objects.get(pk=child.id)
                fchilds.append(fchild)
                fchilds_check.append(fchild)
            except:
                raise_on_error(Error(code=1000, message='Part %d does not exists'%part.id))

        # recursive check
        while len(fchilds_check)>0:
            fchild = fchilds_check.pop()
            if fchild.pk==part.id:
                raise_on_error(Error(code=1000, message='Part cannot be child of itself'))
            for fchild in fchild.childs.all():
                fchilds_check.append(fchild)

        fpart.childs.set(fchilds)

    return fpart

def deserialize_Part(part, fpart=None):
    fpart = deserialize_PartNew(part, fpart)
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
    except ControllerError as e:
        return e.error, 403
    
    fpart.save()
    
    fparameters = []
    if part.parameters:
        for parameter in part.parameters:
            fparameter = deserialize_PartParameter(parameter)
            fparameter.part = fpart
            fparameter.save()
            fparameters.append(fparameter)
        fpart.parameters.set(fparameters)

# TODO: enable bulk insert
    foffers = []
    if part.distributors:
        for part_distributor in part.distributors:
            try:
                fdistributor = api.models.Distributor.objects.get(name=part_distributor.name)
            except:
                return Error(code=1000, message='Distributor %s does not exists'%part_distributor.name), 403
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
                fmanufacturer = api.models.Manufacturer.objects.get(name=part_manufacturer.name)
            except:
                return Error(code=1000, message='Manufacturer %s does not exists'%part_manufacturer.name), 403
            fpart_manufacturer = api.models.PartManufacturer()
            fpart_manufacturer.part = fpart
            fpart_manufacturer.manufacturer = fmanufacturer
            fpart_manufacturer.part_name = part_manufacturer.part_name
            fpart_manufacturer.save()
            fpart_manufacturers.append(fpart_manufacturer)
        fpart.manufacturers.set(fpart_manufacturers)

    fpart_storages = []
    if part.storages:
        for part_storage in part.storages:
            try:
                fstorage = api.models.Storage.objects.get(id=part_storage.id)
            except:
                return Error(code=1000, message='Storage %s does not exists'%part_storage.name), 403
            fpart_storage = api.models.PartStorage()
            fpart_storage.part = fpart
            fpart_storage.storage = fstorage
            fpart_storage.quantity = part_storage.quantity
            fpart_storage.save()
            fpart_storage.append(fpart_storage)
        fpart.storages.set(fpart_storages)

    fpart_attachements = []
    if part.attachements:
        for part_attachement in part.attachements:
            try:
                fattachement = api.models.File.objects.get(id=part_attachement.id)
            except:
                return Error(code=1000, message='File %s does not exists'%part_attachement.id), 403
            fpart_attachement = api.models.PartAttachement()
            fpart_attachement.part = fpart
            fpart_attachement.file = fattachement
            fpart_attachement.description = part_attachement.description
            fpart_attachement.save()
            fpart_attachements.append(fpart_attachement)
        fpart.attachements.set(fpart_attachements)

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
        return Error(code=1000, message='Part %d does not exists'%part_id), 403
    # delete part
    fpart.delete()
    return None


def find_part(part_id, with_offers=None, with_parameters=None, with_childs=None, with_distributors=None, with_manufacturers=None, with_storages=None, with_attachements=None):
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
    :param with_distributors: Include distributors in answer
    :type with_distributors: bool
    :param with_manufacturers: Include manufacturers in answer
    :type with_manufacturers: bool
    :param with_storages: Include storages in answer
    :type with_storages: bool
    :param with_attachements: Include attachements in answer
    :type with_attachements: bool

    :rtype: Part
    """
    try:
        fpart = api.models.Part.objects.get(pk=part_id)
    except:
        return Error(code=1000, message='Part %d does not exists'%part_id), 403
    
    try:
        part = serialize_Part(fpart, with_offers=with_offers, with_parameters=with_parameters, with_childs=with_childs, with_distributors=with_distributors, with_manufacturers=with_manufacturers, with_storages=with_storages, with_attachements=with_attachements)
    except Error as e:
        return e, 403
    return part

def find_parts(category=None, storage=None, with_offers=None, with_parameters=None, with_childs=None, with_distributors=None, with_manufacturers=None, with_storages=None, search=None, with_attachements=None):
    """
    find_parts
    Return all parts
    :param category: Filter by category
    :type category: int
    :param with_offers: Include offers in answer
    :type with_offers: bool
    :param with_parameters: Include parameters in answer
    :type with_parameters: bool
    :param with_childs: Include childs in answer
    :type with_childs: bool
    :param with_distributors: Include distributors in answer
    :type with_distributors: bool
    :param with_manufacturers: Include manufacturers in answer
    :type with_manufacturers: bool
    :param with_storages: Include storages in answer
    :type with_storages: bool
    :param with_attachements: Include attachements in answer
    :type with_attachements: bool
    :param search: Search for parts matching pattern
    :type search: str

    :rtype: List[Part]
    """
    parts = []
    
    fpart_request = api.models.Part.objects

    if search:
        fpart_request = fpart_request.filter(
                    Q(name__contains=search) |
                    Q(description__contains=search) |
                    Q(comment__contains=search)
                )
    
    if category:
        # extract category
        categories = api.models.PartCategory.objects.get(pk=int(category)).get_descendants(include_self=True)
        category_ids = [category.id for category in categories]
        # add a category filter
        fpart_request = fpart_request.filter(category__in=category_ids)

    if storage:
        fparts = api.models.PartStorage.objects.filter(storage=int(storage))
        fpart_ids = [fpart.part.id for fpart in fparts]
        # add a category filter
        fpart_request = fpart_request.filter(id__in=fpart_ids)

    try:
        for fpart in fpart_request.all():
            parts.append(serialize_Part(fpart, with_offers=with_offers, with_parameters=with_parameters, with_childs=with_childs, with_distributors=with_distributors, with_manufacturers=with_manufacturers, with_storages=with_storages, with_attachements=with_attachements))
    except Error as e:
        return e.error, 403

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
        part = Part.from_dict(connexion.request.get_json())
    else:
        return Error(code=1000, message='Missing payload'), 403
    
    try:
        fpart = api.models.Part.objects.get(pk=part_id)
    except:
        return Error(code=1000, message='Part %d does not exists'%part_id), 403
    
    try:
        fpart = deserialize_Part(part, fpart)
    except ControllerError as e:
        return e.error, 403
    
    fpart.save()

    fparameters = []
    if not part.parameters is None:
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
    if not part.distributors is None:
        # remove all part distributors
        api.models.PartOffer.objects.filter(part=part_id).delete()
        # import new values
        for part_distributor in part.distributors:
            try:
                fdistributor = api.models.Distributor.objects.get(name=part_distributor.name)
            except:
                return Error(code=1000, message='Distributor %s does not exists'%part_distributor.name), 403
                
            for offer in part_distributor.offers:
                foffer = deserialize_PartOffer(offer)
                foffer.part = fpart
                foffer.distributor = fdistributor
                foffer.save()
                foffers.append(foffer)
        fpart.offers.set(foffers)
    
    fpart_manufacturers = []
    if not part.manufacturers is None:
        # remove all part distributors
        api.models.PartManufacturer.objects.filter(part=part_id).delete()
        # import new values
        for part_manufacturer in part.manufacturers:
            try:
                fmanufacturer = api.models.Manufacturer.objects.get(name=part_manufacturer.name)
            except:
                return Error(code=1000, message='Manufacturer %s does not exists'%part_manufacturer.name), 403
            fpart_manufacturer = api.models.PartManufacturer()
            fpart_manufacturer.part = fpart
            fpart_manufacturer.manufacturer = fmanufacturer
            fpart_manufacturer.part_name = part_manufacturer.part_name
            fpart_manufacturer.save()
            fpart_manufacturers.append(fpart_manufacturer)
        fpart.manufacturers.set(fpart_manufacturers)

    fpart_storages = []
    if not part.storages is None:
        # remove all part distributors
        api.models.PartStorage.objects.filter(part=part_id).delete()
        # import new values
        for part_storage in part.storages:
            try:
                fstorage = api.models.Storage.objects.get(id=part_storage.id)
            except:
                return Error(code=1000, message='Storage %s does not exists'%part_storage.id), 403
            fpart_storage = api.models.PartStorage()
            fpart_storage.part = fpart
            fpart_storage.storage = fstorage
            fpart_storage.quantity = part_storage.quantity
            if fpart_storage.quantity<0:
                fpart_storage.quantity = 0
                
            fpart_storage.save()
            fpart_storages.append(fpart_storage)
        fpart.storages.set(fpart_storages)

    fpart_attachements = []
    if not part.attachements is None:
        # remove all part distributors
        api.models.PartAttachement.objects.filter(part=part_id).delete()
        # import new values
        for part_attachement in part.attachements:
            try:
                fattachement = api.models.File.objects.get(id=part_attachement.id)
            except:
                return Error(code=1000, message='File %s does not exists'%part_attachement.id), 403
            fpart_attachement = api.models.PartAttachement()
            fpart_attachement.part = fpart
            fpart_attachement.file = fattachement
            fpart_attachement.description = part_attachement.description
            fpart_attachement.save()
            fpart_attachements.append(fpart_attachement)
        fpart.attachements.set(fpart_attachements)

    return serialize_Part(fpart)
