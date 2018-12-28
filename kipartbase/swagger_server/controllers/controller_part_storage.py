import connexion
from swagger_server.models.part_storage import PartStorage

from swagger_server.models.error import Error
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

from swagger_server.controllers.controller_storage import serialize_StorageData, deserialize_StorageData

import api.models
from swagger_server.controllers.helpers import raise_on_error
#import jsonpickle

def serialize_PartStorage(fpart_storage, part_storage=None):
    if part_storage is None:
        part_storage = PartStorage()
    serialize_StorageData(fpart_storage.storage, part_storage)
    part_storage.quantity = fpart_storage.quantity
    return part_storage

def deserialize_PartStorage(part_storage, fpart_storage=None):
    if fpart_storage is None:
        fpart_storage = api.models.PartStorage()
    try:
        fstorage = api.models.Storage.objects.get(name=part_storage.name)
    except:
        return Error(code=1000, message='Storage %s does not exists'%part_storage.name), 403
    fpart_storage.storage = fstorage
    fpart_storage.quantity = part_storage.quantity
    if fpart_storage.quantity<0:
        fpart_storage.quantity = 0
    return fpart_storage
    
def find_part_storages(part_id):
    """
    find_storages
    Return all storages

    :rtype: List[Storage]
    """
    storages = []

    try:
        fpart = api.models.Part.objects.get(pk=part_id)
    except:
        return Error(code=1000, message='Part %d does not exists'%part_id), 403
    
    for fstorage in fpart.storages.all():
        storages.append(serialize_PartStorage(fstorage))

    return storages
