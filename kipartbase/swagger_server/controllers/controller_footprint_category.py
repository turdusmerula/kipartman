import connexion

from swagger_server.models.footprint_category import FootprintCategory
from swagger_server.models.footprint_category_new import FootprintCategoryNew
from swagger_server.models.footprint_category_ref import FootprintCategoryRef
from swagger_server.models.footprint_category_data import FootprintCategoryData

from swagger_server.models.error import Error
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

import api.models
#import jsonpickle

def serialize_FootprintCategoryData(fcategory, category=None):
    if category is None:
        category = FootprintCategoryData()
    category.name = fcategory.name
    category.description = fcategory.description
    return category

def serialize_FootprintCategory(fcategory, category=None):
    if category is None:
        category = FootprintCategory()
    category.id = fcategory.id
    if fcategory.parent:
        category.parent = FootprintCategoryRef(fcategory.parent.id)

    # TODO: optimiser cette partie
    path = "/"+fcategory.name
    fparent = fcategory.parent
    while fparent:
        if fparent:
            path = "/"+fparent.name+path
        fparent = fparent.parent
    category.path = path

    serialize_FootprintCategoryData(fcategory, category)
    return category


def deserialize_FootprintCategoryData(category, fcategory=None):
    if fcategory is None:
        fcategory = api.models.FootprintCategory()
    fcategory.name = category.name
    fcategory.description = category.description
    return fcategory

def deserialize_FootprintCategory(category, fcategory=None):
    fcategory = deserialize_FootprintCategoryData(category, fcategory)
    fcategory.pk = category.id
    return fcategory

def deserialize_FootprintCategoryNew(category, fcategory=None):
    fcategory = deserialize_FootprintCategoryData(category, fcategory)
    return fcategory


def add_footprints_category(category):
    """
    add_footprints_category
    Creates a new footprint category
    :param category: Category to add
    :type category: dict | bytes

    :rtype: FootprintCategory
    """
    if connexion.request.is_json:
        category = FootprintCategoryNew.from_dict(connexion.request.get_json())
    
    fcategory = deserialize_FootprintCategoryNew(category)
    if category.parent:
        try:
            fcategory.parent = api.models.FootprintCategory.objects.get(pk=category.parent.id)
        except:
            return Error(code=1000, message='Parent %d does not exists'%category.parent.id)
    fcategory.save()
    
    return serialize_FootprintCategory(fcategory)


def delete_footprints_category(category_id):
    """
    delete_footprints_category
    Delete footprint category
    :param category_id: Category id
    :type category_id: int

    :rtype: None
    """
    try:
        fcategory = api.models.FootprintCategory.objects.get(pk=category_id)
    except:
        return Error(code=1000, message='Category %d does not exists'%category_id)

    # set childrens to parent id
    for child in fcategory.get_children():
        if fcategory.is_child_node():
            parent = fcategory.get_ancestors(ascending=True)[0]
        else:
            parent = None 
        current_child = api.models.FootprintCategory.objects.get(id=child.id)
        current_child.move_to(parent, 'last-child')
    api.models.Footprint.objects.filter(category=fcategory.pk).update(category=fcategory.parent)
    # delete category
    fcategory.delete()
    # cleanup tree inconsistencies
    api.models.FootprintCategory._tree_manager.rebuild()
    return None


def find_footprints_categories():
    """
    find_footprints_categories
    Return all categories for footprints

    :rtype: List[FootprintCategory]
    """
    categories = []      # result list of root categories
    id_category_map = {} # map of id to container
    
    # create a tree of categories
    for fcategory in api.models.FootprintCategory.objects.all():
        # create category object
        if id_category_map.has_key(fcategory.pk):
            category = serialize_FootprintCategory(fcategory, id_category_map[fcategory.pk])
        else:
            category = serialize_FootprintCategory(fcategory)
        id_category_map[fcategory.pk] = category
        
        if fcategory.parent is None:
            categories.append(category)
        else:
            # if parent does not yet exists precreate it
            if id_category_map.has_key(category.parent.id)==False:
                id_category_map[category.parent.id] = FootprintCategory()
            
            parent = id_category_map[category.parent.id]
            if parent.childs is None:
                parent.childs = [category]
            else:
                parent.childs.append(category)
        
#    for category in api.models.FootprintCategory.objects.all():
#        print category.name
#        categories.append(serialize_FootprintCategory(category))
        
    return categories

def find_footprints_category(category_id):
    """
    find_footprints_category
    Return a footprint category
    :param category_id: Category id
    :type category_id: int

    :rtype: FootprintCategory
    """
    id_fcategory_map = {} # map of id to container

    for fcategory in api.models.FootprintCategory.objects.all():
        id_fcategory_map[fcategory.pk] = fcategory
    
    try:
        category = serialize_FootprintCategory(id_fcategory_map[category_id])
    except:
        return Error(code=1000, message='Category %d does not exists'%category_id)
    
    return category

def update_footprints_category(category_id, category):
    """
    update_footprints_category
    Update footprint category
    :param category_id: Category id
    :type category_id: int
    :param category: Category to update
    :type category: dict | bytes

    :rtype: FootprintCategory
    """
    if connexion.request.is_json:
        category = FootprintCategoryNew.from_dict(connexion.request.get_json())
    else:
        return Error(code=1000, message='Missing payload')
    try:
        fcategory = deserialize_FootprintCategoryNew(category, api.models.FootprintCategory.objects.get(pk=category_id))
    except:
        return Error(code=1000, message='Category %d does not exists'%category_id)
    
    if category.parent:
        # check that instance will not be child of itself
        # TODO: with mptt there is surely a non recursive way to do this
        try:
            fcategory.parent = api.models.FootprintCategory.objects.get(pk=category.parent.id)
        except:
            return Error(code=1000, message='Parent %d does not exists'%category.parent.id)
            
        fparent = fcategory.parent
        while fparent is not None:
            if fparent.pk==category_id:
                return Error(code=1000, message='Category cannot be child of itself')
            if fparent.parent:
                fparent = api.models.FootprintCategory.objects.get(pk=fparent.parent.pk)
            else:
                fparent = None
    else:
        fcategory.parent = None
    
    fcategory.save()
    
    return serialize_FootprintCategory(fcategory)
