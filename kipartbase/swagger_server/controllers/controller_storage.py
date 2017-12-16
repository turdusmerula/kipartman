import connexion
from swagger_server.models.storage import Storage
from swagger_server.models.storage_data import StorageData
from swagger_server.models.storage_new import StorageNew

from swagger_server.models.storage_category import StorageCategory
from swagger_server.models.storage_category_ref import StorageCategoryRef

from swagger_server.models.error import Error
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

from swagger_server.controllers.controller_storage_category import find_storages_category,\
    find_storages_categories
from swagger_server.controllers.controller_upload_file import find_upload_file
from swagger_server.controllers.helpers import raise_on_error, ControllerError

import api.models
from django.db.models import Q

#import jsonpickle
def serialize_StorageData(fstorage, storage=None):
    if storage is None:
        storage = StorageData()
    storage.name = fstorage.name
    storage.description = fstorage.description
    storage.comment = fstorage.comment
    return storage

def serialize_Storage(fstorage, storage=None):
    if storage is None:
        storage = Storage()
    storage.id = fstorage.id
    serialize_StorageData(fstorage, storage)
    if fstorage.category:
        storage.category = raise_on_error(find_storages_category(fstorage.category.id))
    
    return storage


def deserialize_StorageData(storage, fstorage=None):
    if fstorage is None:
        fstorage = api.models.Storage()
    fstorage.name = storage.name
    fstorage.description = storage.description
    fstorage.comment = storage.comment
    return fstorage


def deserialize_StorageNew(storage, fstorage=None):
    fstorage = deserialize_StorageData(storage, fstorage)
    if storage.category:
        fstorage.category = api.models.StorageCategory.objects.get(id=storage.category.id)
    else:
        fstorage.category = None
        
    return fstorage


def add_storage(storage):
    """
    add_storage
    Creates a new storage
    :param storage: Storage to add
    :type storage: dict | bytes

    :rtype: Storage
    """
    if connexion.request.is_json:
        storage = StorageNew.from_dict(connexion.request.get_json())

    try:
        fstorage = deserialize_StorageNew(storage)
    except ControllerError as e:
        return e.error, 403

        
    fstorage.save()
    
    return serialize_Storage(fstorage)


def delete_storage(storage_id):
    """
    delete_storage
    Delete storage
    :param storage_id: Storage id
    :type storage_id: int

    :rtype: None
    """
    try:
        fstorage = api.models.Storage.objects.get(pk=storage_id)
    except:
        return Error(code=1000, message='Storage %d does not exists'%storage_id), 403
    # delete storage
    fstorage.delete()
    return None


def find_storage(storage_id):
    """
    find_storage
    Return a storage
    :param storage_id: Storage id
    :type storage_id: int

    :rtype: Storage
    """
    try:
        fstorage = api.models.Storage.objects.get(pk=storage_id)
    except:
        return Error(code=1000, message='Storage %d does not exists'%storage_id), 403
    
    try:
        storage = serialize_Storage(fstorage)
    except ControllerError as e:
        return e.error, 403
    
    return storage

def find_storages(category=None, search=None):
    """
    find_storages
    Return all storages
    :param category: Filter by category
    :type category: int
    :param search: Search for storage matching pattern
    :type search: str

    :rtype: List[Storage]
    """
    storages = []
    
    fstorage_query = api.models.Storage.objects
    
    if search:
        fstorage_query = fstorage_query.filter(
                    Q(name__contains=search) |
                    Q(description__contains=search) |
                    Q(comment__contains=search)
                )

    if category:
        # extract category
        categories = api.models.StorageCategory.objects.get(pk=int(category)).get_descendants(include_self=True)
        category_ids = [category.id for category in categories]
        # add a category filter
        fstorage_query = fstorage_query.filter(category__in=category_ids)

    for fstorage in fstorage_query.all():
        storages.append(serialize_Storage(fstorage))

    return storages

def update_storage(storage_id, storage):
    """
    update_storage
    Update storage
    :param storage_id: Storage id
    :type storage_id: int
    :param storage: Storage to update
    :type storage: dict | bytes

    :rtype: Storage
    """
    if connexion.request.is_json:
        storage = StorageNew.from_dict(connexion.request.get_json())
    else:
        return Error(code=1000, message='Missing payload'), 403

    try:
        fstorage = deserialize_StorageNew(storage, api.models.Storage.objects.get(pk=storage_id))
    except:
        return Error(code=1000, message='Storage %d does not exists'%storage_id), 403       

    fstorage.save()
    
    return serialize_Storage(fstorage)
