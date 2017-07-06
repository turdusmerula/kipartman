import connexion
from swagger_server.models.part_category import PartCategory
from swagger_server.models.part_category_data import PartCategoryData
from swagger_server.models.error import Error
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

import api.models
#import jsonpickle


def serialize_PartCategory(fcategory, category=None):
    if category is None:
        category = PartCategory()
    category.id = fcategory.id
    if fcategory.parent:
        category.parent = fcategory.parent.id
    category.name = fcategory.name
    return category

def deserialize_PartCategoryData(category, fcategory=None):
    if fcategory is None:
        fcategory = api.models.PartCategory()
#    if category.parent:
#        fcategory.parent = category.parent.id
    fcategory.name = category.name
    return fcategory

def deserialize_PartCategory(category, fcategory=None):
    fcategory = deserialize_PartCategoryData(category, fcategory)
    fcategory.pk = category.id
    return fcategory



def add_parts_category(category):
    """
    add_parts_category
    Creates a new part category
    :param category: Category to add
    :type category: dict | bytes

    :rtype: Category
    """
    if connexion.request.is_json:
        category = PartCategoryData.from_dict(connexion.request.get_json())
    
    fcategory = deserialize_PartCategoryData(category)
    if category.parent:
        try:
            fcategory.parent = api.models.PartCategory.objects.get(pk=category.parent)
        except:
            return Error(code=1000, message='Parent %d does not exists'%category.parent)
    fcategory.save()
    
    return serialize_PartCategory(fcategory)


def delete_parts_category(category_id):
    """
    delete_parts_category
    Delete part category
    :param category_id: Part category to update
    :type category_id: int

    :rtype: None
    """
    try:
        fcategory = api.models.PartCategory.objects.get(pk=category_id)
    except:
        return Error(code=1000, message='Category %d does not exists'%category_id)

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

    #TODO: remove category from parts
    
    return None


def find_parts_categories():
    """
    find_parts_categories
    Return all categories for parts

    :rtype: List[Category]
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
            
        # if parent does not yet exists precreate it
        if id_category_map.has_key(category.parent)==False:
            id_category_map[category.parent] = PartCategory()
            
        parent = id_category_map[category.parent]
        if parent.childs is None:
            parent.childs = [category]
        else:
            parent.childs.append(category)
        
#    for category in api.models.PartCategory.objects.all():
#        print category.name
#        categories.append(serialize_PartCategory(category))
        
    return categories


def update_parts_category(category_id):
    """
    update_parts_category
    Update part category
    :param category_id: Part category to update
    :type category_id: int

    :rtype: Category
    """
    if connexion.request.is_json:
        category = PartCategoryData.from_dict(connexion.request.get_json())
    else:
        return Error(code=1000, message='Missing payload')
    try:
        fcategory = deserialize_PartCategoryData(category, api.models.PartCategory.objects.get(pk=category_id))
    except:
        return Error(code=1000, message='Category %d does not exists'%category_id)
    
    if category.parent:
        # check that instance will not be child of itself
        # TODO: with mptt there is surely a non recursive way to do this
        try:
            fcategory.parent = api.models.PartCategory.objects.get(pk=category.parent)
        except:
            return Error(code=1000, message='Parent %d does not exists'%category.parent)
            
        fparent = fcategory.parent
        while fparent is not None:
            if fparent.pk==category_id:
                return Error(code=1000, message='Category cannot be child of itself')
            if fparent.parent:
                fparent = api.models.PartCategory.objects.get(pk=fparent.parent.pk)
            else:
                fparent = None
                
    fcategory.save()
    
    return None
