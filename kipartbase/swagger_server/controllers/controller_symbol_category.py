import connexion

from swagger_server.models.symbol_category import SymbolCategory
from swagger_server.models.symbol_category_new import SymbolCategoryNew
from swagger_server.models.symbol_category_ref import SymbolCategoryRef
from swagger_server.models.symbol_category_data import SymbolCategoryData

from swagger_server.models.error import Error
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

import api.models
#import jsonpickle

def serialize_SymbolCategoryData(fcategory, category=None):
    if category is None:
        category = SymbolCategoryData()
    category.name = fcategory.name
    category.description = fcategory.description
    return category

def serialize_SymbolCategory(fcategory, category=None):
    if category is None:
        category = SymbolCategory()
    category.id = fcategory.id
    if fcategory.parent:
        category.parent = SymbolCategoryRef(fcategory.parent.id)

    # TODO: optimiser cette partie
    path = "/"+fcategory.name
    fparent = fcategory.parent
    while fparent:
        if fparent:
            path = "/"+fparent.name+path
        fparent = fparent.parent
    category.path = path

    serialize_SymbolCategoryData(fcategory, category)
    return category


def deserialize_SymbolCategoryData(category, fcategory=None):
    if fcategory is None:
        fcategory = api.models.SymbolCategory()
    fcategory.name = category.name
    fcategory.description = category.description
    return fcategory

def deserialize_SymbolCategory(category, fcategory=None):
    fcategory = deserialize_SymbolCategoryData(category, fcategory)
    fcategory.pk = category.id
    return fcategory

def deserialize_SymbolCategoryNew(category, fcategory=None):
    fcategory = deserialize_SymbolCategoryData(category, fcategory)
    return fcategory


def add_symbols_category(category):
    """
    add_symbols_category
    Creates a new symbol category
    :param category: Category to add
    :type category: dict | bytes

    :rtype: SymbolCategory
    """
    if connexion.request.is_json:
        category = SymbolCategoryNew.from_dict(connexion.request.get_json())
    
    fcategory = deserialize_SymbolCategoryNew(category)
    if category.parent:
        try:
            fcategory.parent = api.models.SymbolCategory.objects.get(pk=category.parent.id)
        except:
            return Error(code=1000, message='Parent %d does not exists'%category.parent.id), 403
    fcategory.save()
    
    return serialize_SymbolCategory(fcategory)


def delete_symbols_category(category_id):
    """
    delete_symbols_category
    Delete symbol category
    :param category_id: Category id
    :type category_id: int

    :rtype: None
    """
    try:
        fcategory = api.models.SymbolCategory.objects.get(pk=category_id)
    except:
        return Error(code=1000, message='Category %d does not exists'%category_id), 403

    # set childrens to parent id
    for child in fcategory.get_children():
        if fcategory.is_child_node():
            parent = fcategory.get_ancestors(ascending=True)[0]
        else:
            parent = None 
        current_child = api.models.SymbolCategory.objects.get(id=child.id)
        current_child.move_to(parent, 'last-child')
    api.models.Symbol.objects.filter(category=fcategory.pk).update(category=fcategory.parent)
    # delete category
    fcategory.delete()
    # cleanup tree inconsistencies
    api.models.SymbolCategory._tree_manager.rebuild()
    return None


def find_symbols_categories():
    """
    find_symbols_categories
    Return all categories for symbols

    :rtype: List[SymbolCategory]
    """
    categories = []      # result list of root categories
    id_category_map = {} # map of id to container
    
    # create a tree of categories
    for fcategory in api.models.SymbolCategory.objects.all():
        # create category object
        if id_category_map.has_key(fcategory.pk):
            category = serialize_SymbolCategory(fcategory, id_category_map[fcategory.pk])
        else:
            category = serialize_SymbolCategory(fcategory)
        id_category_map[fcategory.pk] = category
        
        if fcategory.parent is None:
            categories.append(category)
        else:
            # if parent does not yet exists precreate it
            if id_category_map.has_key(category.parent.id)==False:
                id_category_map[category.parent.id] = SymbolCategory()
            
            parent = id_category_map[category.parent.id]
            if parent.childs is None:
                parent.childs = [category]
            else:
                parent.childs.append(category)
        
#    for category in api.models.SymbolCategory.objects.all():
#        print category.name
#        categories.append(serialize_SymbolCategory(category))
        
    return categories

def find_symbols_category(category_id):
    """
    find_symbols_category
    Return a symbol category
    :param category_id: Category id
    :type category_id: int

    :rtype: SymbolCategory
    """
    id_fcategory_map = {} # map of id to container

    for fcategory in api.models.SymbolCategory.objects.all():
        id_fcategory_map[fcategory.pk] = fcategory
    
    try:
        category = serialize_SymbolCategory(id_fcategory_map[category_id])
    except:
        return Error(code=1000, message='Category %d does not exists'%category_id), 403
    
    return category

def update_symbols_category(category_id, category):
    """
    update_symbols_category
    Update symbol category
    :param category_id: Category id
    :type category_id: int
    :param category: Category to update
    :type category: dict | bytes

    :rtype: SymbolCategory
    """
    if connexion.request.is_json:
        category = SymbolCategoryNew.from_dict(connexion.request.get_json())
    else:
        return Error(code=1000, message='Missing payload'), 403
    try:
        fcategory = deserialize_SymbolCategoryNew(category, api.models.SymbolCategory.objects.get(pk=category_id))
    except:
        return Error(code=1000, message='Category %d does not exists'%category_id), 403
    
    if category.parent:
        # check that instance will not be child of itself
        # TODO: with mptt there is surely a non recursive way to do this
        try:
            fcategory.parent = api.models.SymbolCategory.objects.get(pk=category.parent.id)
        except:
            return Error(code=1000, message='Parent %d does not exists'%category.parent.id), 403
            
        fparent = fcategory.parent
        while fparent is not None:
            if fparent.pk==category_id:
                return Error(code=1000, message='Category cannot be child of itself'), 403
            if fparent.parent:
                fparent = api.models.SymbolCategory.objects.get(pk=fparent.parent.pk)
            else:
                fparent = None
    else:
        fcategory.parent = None
    
    fcategory.save()
    
    return serialize_SymbolCategory(fcategory)
