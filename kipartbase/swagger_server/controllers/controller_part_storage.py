import connexion
from swagger_server.models.part_storage import PartStorage

from swagger_server.models.error import Error
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

from swagger_server.controllers.controller_storage import serialize_Storage

import api.models
#import jsonpickle

def serialize_PartStorage(fstorage, part_storage=None):
    if part_storage is None:
        part_storage = PartStorage()
    serialize_Storage(fstorage.storage, part_storage)
    part_storage.quantity = fstorage.quantity
    return part_storage

    
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
