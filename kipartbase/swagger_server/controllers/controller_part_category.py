import connexion

from swagger_server.models.part_category import PartCategory
from swagger_server.models.part_category_new import PartCategoryNew
from swagger_server.models.part_category_ref import PartCategoryRef
from swagger_server.models.part_category_data import PartCategoryData

from swagger_server.models.error import Error
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

import api.models
#import jsonpickle

def serialize_PartCategoryData(fcategory, category=None):
    if category is None:
        category = PartCategoryData()
    category.name = fcategory.name
    category.description = fcategory.description
    return category

def serialize_PartCategory(fcategory, category=None):
    if category is None:
        category = PartCategory()
    category.id = fcategory.id
    if fcategory.parent:
        category.parent = PartCategoryRef(fcategory.parent.id)

    # TODO: optimiser cette partie
    path = "/"+fcategory.name
    fparent = fcategory.parent
    while fparent:
        if fparent:
            path = "/"+fparent.name+path
        fparent = fparent.parent
    category.path = path

    serialize_PartCategoryData(fcategory, category)
    return category


def deserialize_PartCategoryData(category, fcategory=None):
    if fcategory is None:
        fcategory = api.models.PartCategory()
    fcategory.name = category.name
    fcategory.description = category.description
    return fcategory

def deserialize_PartCategory(category, fcategory=None):
    fcategory = deserialize_PartCategoryData(category, fcategory)
    fcategory.pk = category.id
    return fcategory

def deserialize_PartCategoryNew(category, fcategory=None):
    fcategory = deserialize_PartCategoryData(category, fcategory)
    return fcategory


def add_parts_category(category):
    """
    add_parts_category
    Creates a new part category
    :param category: Category to add
    :type category: dict | bytes

    :rtype: PartCategory
    """
    if connexion.request.is_json:
        category = PartCategoryNew.from_dict(connexion.request.get_json())
    
    fcategory = deserialize_PartCategoryNew(category)
    if category.parent:
        try:
            fcategory.parent = api.models.PartCategory.objects.get(pk=category.parent.id)
        except:
            return Error(code=1000, message='Parent %d does not exists'%category.parent.id), 403
    fcategory.save()
    
    return serialize_PartCategory(fcategory)


def delete_parts_category(category_id):
    """
    delete_parts_category
    Delete part category
    :param category_id: Category id
    :type category_id: int

    :rtype: None
    """
    try:
        fcategory = api.models.PartCategory.objects.get(pk=category_id)
    except:
        return Error(code=1000, message='Category %d does not exists'%category_id), 403

    # set childrens to parent id
    for child in fcategory.get_children():
        if fcategory.is_child_node():
            parent = fcategory.get_ancestors(ascending=True)[0]
        else:
            parent = None 
        current_child = api.models.PartCategory.objects.get(id=child.id)
        current_child.move_to(parent, 'last-child')
    api.models.Part.objects.filter(category=fcategory.pk).update(category=fcategory.parent)
    # delete category
    fcategory.delete()
    # cleanup tree inconsistencies
    api.models.PartCategory._tree_manager.rebuild()
    return None


def find_parts_categories():
    """
    find_parts_categories
    Return all categories for parts

    :rtype: List[PartCategory]
    """
    categories = []      # result list of root categories
    id_category_map = {} # map of id to container
    
    # create a tree of categories
    for fcategory in api.models.PartCategory.objects.all():
        # create category object
        if id_category_map.has_key(fcategory.pk):
            category = serialize_PartCategory(fcategory, id_category_map[fcategory.pk])
        else:
            category = serialize_PartCategory(fcategory)
        id_category_map[fcategory.pk] = category
        
        if fcategory.parent is None:
            categories.append(category)
        else:
            # if parent does not yet exists precreate it
            if id_category_map.has_key(category.parent.id)==False:
                id_category_map[category.parent.id] = PartCategory()
            
            parent = id_category_map[category.parent.id]
            if parent.childs is None:
                parent.childs = [category]
            else:
                parent.childs.append(category)
        
#    for category in api.models.PartCategory.objects.all():
#        print category.name
#        categories.append(serialize_PartCategory(category))
        
    return categories

def find_parts_category(category_id):
    """
    find_parts_category
    Return a part category
    :param category_id: Category id
    :type category_id: int

    :rtype: PartCategory
    """
    id_fcategory_map = {} # map of id to container

    for fcategory in api.models.PartCategory.objects.all():
        id_fcategory_map[fcategory.pk] = fcategory
    
    try:
        category = serialize_PartCategory(id_fcategory_map[category_id])
    except:
        return Error(code=1000, message='Category %d does not exists'%category_id), 403
    
    return category

def update_parts_category(category_id, category):
    """
    update_parts_category
    Update part category
    :param category_id: Category id
    :type category_id: int
    :param category: Category to update
    :type category: dict | bytes

    :rtype: PartCategory
    """
    if connexion.request.is_json:
        category = PartCategoryNew.from_dict(connexion.request.get_json())
    else:
        return Error(code=1000, message='Missing payload'), 403
    try:
        fcategory = deserialize_PartCategoryNew(category, api.models.PartCategory.objects.get(pk=category_id))
    except:
        return Error(code=1000, message='Category %d does not exists'%category_id), 403
    
    if category.parent:
        # check that instance will not be child of itself
        # TODO: with mptt there is surely a non recursive way to do this
        try:
            fcategory.parent = api.models.PartCategory.objects.get(pk=category.parent.id)
        except:
            return Error(code=1000, message='Parent %d does not exists'%category.parent.id), 403
            
        fparent = fcategory.parent
        while fparent is not None:
            if fparent.pk==category_id:
                return Error(code=1000, message='Category cannot be child of itself'), 403
            if fparent.parent:
                fparent = api.models.PartCategory.objects.get(pk=fparent.parent.pk)
            else:
                fparent = None
    else:
        fcategory.parent = None
    
    fcategory.save()
    
    return serialize_PartCategory(fcategory)
