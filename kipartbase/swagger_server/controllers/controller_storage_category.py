import connexion

from swagger_server.models.storage_category import StorageCategory
from swagger_server.models.storage_category_new import StorageCategoryNew
from swagger_server.models.storage_category_ref import StorageCategoryRef
from swagger_server.models.storage_category_data import StorageCategoryData

from swagger_server.models.error import Error
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

import api.models
#import jsonpickle

def serialize_StorageCategoryData(fcategory, category=None):
    if category is None:
        category = StorageCategoryData()
    category.name = fcategory.name
    category.description = fcategory.description
    return category

def serialize_StorageCategory(fcategory, category=None):
    if category is None:
        category = StorageCategory()
    category.id = fcategory.id
    if fcategory.parent:
        category.parent = StorageCategoryRef(fcategory.parent.id)

    # TODO: optimiser cette partie
    path = "/"+fcategory.name
    fparent = fcategory.parent
    while fparent:
        if fparent:
            path = "/"+fparent.name+path
        fparent = fparent.parent
    category.path = path

    serialize_StorageCategoryData(fcategory, category)
    return category


def deserialize_StorageCategoryData(category, fcategory=None):
    if fcategory is None:
        fcategory = api.models.StorageCategory()
    fcategory.name = category.name
    fcategory.description = category.description
    return fcategory

def deserialize_StorageCategory(category, fcategory=None):
    fcategory = deserialize_StorageCategoryData(category, fcategory)
    fcategory.pk = category.id
    return fcategory

def deserialize_StorageCategoryNew(category, fcategory=None):
    fcategory = deserialize_StorageCategoryData(category, fcategory)
    return fcategory


def add_storages_category(category):
    """
    add_storages_category
    Creates a new storage category
    :param category: Category to add
    :type category: dict | bytes

    :rtype: StorageCategory
    """
    if connexion.request.is_json:
        category = StorageCategoryNew.from_dict(connexion.request.get_json())
    
    fcategory = deserialize_StorageCategoryNew(category)
    if category.parent:
        try:
            fcategory.parent = api.models.StorageCategory.objects.get(pk=category.parent.id)
        except:
            return Error(code=1000, message='Parent %d does not exists'%category.parent.id), 403
    fcategory.save()
    
    return serialize_StorageCategory(fcategory)


def delete_storages_category(category_id):
    """
    delete_storages_category
    Delete storage category
    :param category_id: Category id
    :type category_id: int

    :rtype: None
    """
    try:
        fcategory = api.models.StorageCategory.objects.get(pk=category_id)
    except:
        return Error(code=1000, message='Category %d does not exists'%category_id), 403

    # set childrens to parent id
    for child in fcategory.get_children():
        if fcategory.is_child_node():
            parent = fcategory.get_ancestors(ascending=True)[0]
        else:
            parent = None 
        current_child = api.models.StorageCategory.objects.get(id=child.id)
        current_child.move_to(parent, 'last-child')
    api.models.Storage.objects.filter(category=fcategory.pk).update(category=fcategory.parent)
    # delete category
    fcategory.delete()
    # cleanup tree inconsistencies
    api.models.StorageCategory._tree_manager.rebuild()
    return None


def find_storages_categories():
    """
    find_storages_categories
    Return all categories for storages

    :rtype: List[StorageCategory]
    """
    categories = []      # result list of root categories
    id_category_map = {} # map of id to container
    
    # create a tree of categories
    for fcategory in api.models.StorageCategory.objects.all():
        # create category object
        if id_category_map.has_key(fcategory.pk):
            category = serialize_StorageCategory(fcategory, id_category_map[fcategory.pk])
        else:
            category = serialize_StorageCategory(fcategory)
        id_category_map[fcategory.pk] = category
        
        if fcategory.parent is None:
            categories.append(category)
        else:
            # if parent does not yet exists precreate it
            if id_category_map.has_key(category.parent.id)==False:
                id_category_map[category.parent.id] = StorageCategory()
            
            parent = id_category_map[category.parent.id]
            if parent.childs is None:
                parent.childs = [category]
            else:
                parent.childs.append(category)
        
#    for category in api.models.StorageCategory.objects.all():
#        print category.name
#        categories.append(serialize_StorageCategory(category))
        
    return categories

def find_storages_category(category_id):
    """
    find_storages_category
    Return a storage category
    :param category_id: Category id
    :type category_id: int

    :rtype: StorageCategory
    """
    id_fcategory_map = {} # map of id to container

    for fcategory in api.models.StorageCategory.objects.all():
        id_fcategory_map[fcategory.pk] = fcategory
    
    try:
        category = serialize_StorageCategory(id_fcategory_map[category_id])
    except:
        return Error(code=1000, message='Category %d does not exists'%category_id), 403
    
    return category

def update_storages_category(category_id, category):
    """
    update_storages_category
    Update storage category
    :param category_id: Category id
    :type category_id: int
    :param category: Category to update
    :type category: dict | bytes

    :rtype: StorageCategory
    """
    if connexion.request.is_json:
        category = StorageCategoryNew.from_dict(connexion.request.get_json())
    else:
        return Error(code=1000, message='Missing payload'), 403
    try:
        fcategory = deserialize_StorageCategoryNew(category, api.models.StorageCategory.objects.get(pk=category_id))
    except:
        return Error(code=1000, message='Category %d does not exists'%category_id), 403
    
    if category.parent:
        # check that instance will not be child of itself
        # TODO: with mptt there is surely a non recursive way to do this
        try:
            fcategory.parent = api.models.StorageCategory.objects.get(pk=category.parent.id)
        except:
            return Error(code=1000, message='Parent %d does not exists'%category.parent.id), 403
            
        fparent = fcategory.parent
        while fparent is not None:
            if fparent.pk==category_id:
                return Error(code=1000, message='Category cannot be child of itself'), 403
            if fparent.parent:
                fparent = api.models.StorageCategory.objects.get(pk=fparent.parent.pk)
            else:
                fparent = None
    else:
        fcategory.parent = None
    
    fcategory.save()
    
    return serialize_StorageCategory(fcategory)
