import connexion

from swagger_server.models.model_category import ModelCategory
from swagger_server.models.model_category_new import ModelCategoryNew
from swagger_server.models.model_category_ref import ModelCategoryRef
from swagger_server.models.model_category_data import ModelCategoryData

from swagger_server.models.error import Error
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

import api.models
#import jsonpickle

def serialize_ModelCategoryData(fcategory, category=None):
    if category is None:
        category = ModelCategoryData()
    category.name = fcategory.name
    category.description = fcategory.description
    return category

def serialize_ModelCategory(fcategory, category=None):
    if category is None:
        category = ModelCategory()
    category.id = fcategory.id
    if fcategory.parent:
        category.parent = ModelCategoryRef(fcategory.parent.id)

    # TODO: optimiser cette partie
    path = "/"+fcategory.name
    fparent = fcategory.parent
    while fparent:
        if fparent:
            path = "/"+fparent.name+path
        fparent = fparent.parent
    category.path = path

    serialize_ModelCategoryData(fcategory, category)
    return category


def deserialize_ModelCategoryData(category, fcategory=None):
    if fcategory is None:
        fcategory = api.models.ModelCategory()
    fcategory.name = category.name
    fcategory.description = category.description
    return fcategory

def deserialize_ModelCategory(category, fcategory=None):
    fcategory = deserialize_ModelCategoryData(category, fcategory)
    fcategory.pk = category.id
    return fcategory

def deserialize_ModelCategoryNew(category, fcategory=None):
    fcategory = deserialize_ModelCategoryData(category, fcategory)
    return fcategory


def add_models_category(category):
    """
    add_models_category
    Creates a new model category
    :param category: Category to add
    :type category: dict | bytes

    :rtype: ModelCategory
    """
    if connexion.request.is_json:
        category = ModelCategoryNew.from_dict(connexion.request.get_json())
    
    fcategory = deserialize_ModelCategoryNew(category)
    if category.parent:
        try:
            fcategory.parent = api.models.ModelCategory.objects.get(pk=category.parent.id)
        except:
            return Error(code=1000, message='Parent %d does not exists'%category.parent.id)
    fcategory.save()
    
    return serialize_ModelCategory(fcategory)


def delete_models_category(category_id):
    """
    delete_models_category
    Delete model category
    :param category_id: Category id
    :type category_id: int

    :rtype: None
    """
    try:
        fcategory = api.models.ModelCategory.objects.get(pk=category_id)
    except:
        return Error(code=1000, message='Category %d does not exists'%category_id)

    # set childrens to parent id
    for child in fcategory.get_children():
        if fcategory.is_child_node():
            parent = fcategory.get_ancestors(ascending=True)[0]
        else:
            parent = None 
        current_child = api.models.ModelCategory.objects.get(id=child.id)
        current_child.move_to(parent, 'last-child')
    api.models.Model.objects.filter(category=fcategory.pk).update(category=fcategory.parent)
    # delete category
    fcategory.delete()
    # cleanup tree inconsistencies
    api.models.ModelCategory._tree_manager.rebuild()
    return None


def find_models_categories():
    """
    find_models_categories
    Return all categories for models

    :rtype: List[ModelCategory]
    """
    categories = []      # result list of root categories
    id_category_map = {} # map of id to container
    
    # create a tree of categories
    for fcategory in api.models.ModelCategory.objects.all():
        # create category object
        if id_category_map.has_key(fcategory.pk):
            category = serialize_ModelCategory(fcategory, id_category_map[fcategory.pk])
        else:
            category = serialize_ModelCategory(fcategory)
        id_category_map[fcategory.pk] = category
        
        if fcategory.parent is None:
            categories.append(category)
        else:
            # if parent does not yet exists precreate it
            if id_category_map.has_key(category.parent.id)==False:
                id_category_map[category.parent.id] = ModelCategory()
            
            parent = id_category_map[category.parent.id]
            if parent.childs is None:
                parent.childs = [category]
            else:
                parent.childs.append(category)
        
#    for category in api.models.ModelCategory.objects.all():
#        print category.name
#        categories.append(serialize_ModelCategory(category))
        
    return categories

def find_models_category(category_id):
    """
    find_models_category
    Return a model category
    :param category_id: Category id
    :type category_id: int

    :rtype: ModelCategory
    """
    id_fcategory_map = {} # map of id to container

    for fcategory in api.models.ModelCategory.objects.all():
        id_fcategory_map[fcategory.pk] = fcategory
    
    try:
        category = serialize_ModelCategory(id_fcategory_map[category_id])
    except:
        return Error(code=1000, message='Category %d does not exists'%category_id)
    
    return category

def update_models_category(category_id, category):
    """
    update_models_category
    Update model category
    :param category_id: Category id
    :type category_id: int
    :param category: Category to update
    :type category: dict | bytes

    :rtype: ModelCategory
    """
    if connexion.request.is_json:
        category = ModelCategoryNew.from_dict(connexion.request.get_json())
    else:
        return Error(code=1000, message='Missing payload')
    try:
        fcategory = deserialize_ModelCategoryNew(category, api.models.ModelCategory.objects.get(pk=category_id))
    except:
        return Error(code=1000, message='Category %d does not exists'%category_id)
    
    if category.parent:
        # check that instance will not be child of itself
        # TODO: with mptt there is surely a non recursive way to do this
        try:
            fcategory.parent = api.models.ModelCategory.objects.get(pk=category.parent.id)
        except:
            return Error(code=1000, message='Parent %d does not exists'%category.parent.id)
            
        fparent = fcategory.parent
        while fparent is not None:
            if fparent.pk==category_id:
                return Error(code=1000, message='Category cannot be child of itself')
            if fparent.parent:
                fparent = api.models.ModelCategory.objects.get(pk=fparent.parent.pk)
            else:
                fparent = None
    else:
        fcategory.parent = None
    
    fcategory.save()
    
    return serialize_ModelCategory(fcategory)
