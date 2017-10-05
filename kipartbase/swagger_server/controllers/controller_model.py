import connexion
from swagger_server.models.model import Model
from swagger_server.models.model_data import ModelData
from swagger_server.models.model_new import ModelNew

from swagger_server.models.model_category import ModelCategory
from swagger_server.models.model_category_ref import ModelCategoryRef

from swagger_server.models.error import Error
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

from swagger_server.controllers.controller_model_category import find_models_category,\
    find_models_categories
from swagger_server.controllers.controller_upload_file import find_upload_file
from swagger_server.controllers.helpers import raise_on_error, ControllerError

import api.models
from django.db.models import Q
#import jsonpickle
def serialize_ModelData(fmodel, model=None):
    if model is None:
        model = ModelData()
    model.name = fmodel.name
    model.description = fmodel.description
    model.comment = fmodel.comment
    if fmodel.snapeda:
        model.snapeda = fmodel.snapeda
    if fmodel.snapeda_uid:
        model.snapeda_uid = fmodel.snapeda_uid
    if fmodel.updated:
        model.updated = fmodel.updated
    return model

def serialize_Model(fmodel, model=None):
    if model is None:
        model = Model()
    model.id = fmodel.id
    serialize_ModelData(fmodel, model)
    if fmodel.category:
        model.category = raise_on_error(find_models_category(fmodel.category.id))
    if fmodel.image:
        model.image = raise_on_error(find_upload_file(fmodel.image.id))
    if fmodel.model:
        model.model = raise_on_error(find_upload_file(fmodel.model.id))
    return model


def deserialize_ModelData(model, fmodel=None):
    if fmodel is None:
        fmodel = api.models.Model()
    fmodel.name = model.name
    fmodel.description = model.description
    fmodel.comment = model.comment
    if model.snapeda:
        fmodel.snapeda = model.snapeda
    if model.snapeda_uid:
        fmodel.snapeda_uid = model.snapeda_uid
    if model.updated:
        fmodel.updated = model.updated
    return fmodel


def deserialize_ModelNew(model, fmodel=None):
    fmodel = deserialize_ModelData(model, fmodel)
    if model.category:
        fmodel.category = api.models.ModelCategory.objects.get(id=model.category.id)
    else:
        fmodel.category = None
        
    if model.image:
        fmodel.image = api.models.File.objects.get(id=model.image.id)
    else:
        fmodel.image = None
        
    if model.model:
        fmodel.model = api.models.File.objects.get(id=model.model.id)
    else:
        fmodel.model = None

    return fmodel


def add_model(model):
    """
    add_model
    Creates a new model
    :param model: Model to add
    :type model: dict | bytes

    :rtype: Model
    """
    if connexion.request.is_json:
        model = ModelNew.from_dict(connexion.request.get_json())

    try:
        fmodel = deserialize_ModelNew(model)
    except ControllerError as e:
        return e.error

        
    fmodel.save()
    
    return serialize_Model(fmodel)


def delete_model(model_id):
    """
    delete_model
    Delete model
    :param model_id: Model id
    :type model_id: int

    :rtype: None
    """
    try:
        fmodel = api.models.Model.objects.get(pk=model_id)
    except:
        return Error(code=1000, message='Model %d does not exists'%model_id)
    # delete model
    fmodel.delete()
    return None


def find_model(model_id):
    """
    find_model
    Return a model
    :param model_id: Model id
    :type model_id: int

    :rtype: Model
    """
    try:
        fmodel = api.models.Model.objects.get(pk=model_id)
    except:
        return Error(code=1000, message='Model %d does not exists'%model_id)
    
    try:
        model = serialize_Model(fmodel)
    except ControllerError as e:
        return e.error
    
    return model

def find_models(category=None, search=None):
    """
    find_models
    Return all models
    :param category: Filter by category
    :type category: int
    :param search: Search for model matching pattern
    :type search: str

    :rtype: List[Model]
    """
    models = []
    
    fmodel_query = api.models.Model.objects
    
    if search:
        fmodel_query = fmodel_query.filter(
                    Q(name__contains=search) |
                    Q(description__contains=search) |
                    Q(comment__contains=search)
                )

    if category:
        # extract category
        categories = api.models.ModelCategory.objects.get(pk=int(category)).get_descendants(include_self=True)
        category_ids = [category.id for category in categories]
        # add a category filter
        fmodel_query = fmodel_query.filter(category__in=category_ids)

    for fmodel in fmodel_query.all():
        models.append(serialize_Model(fmodel))

    return models

def update_model(model_id, model):
    """
    update_model
    Update model
    :param model_id: Model id
    :type model_id: int
    :param model: Model to update
    :type model: dict | bytes

    :rtype: Model
    """
    if connexion.request.is_json:
        model = ModelNew.from_dict(connexion.request.get_json())
    else:
        return Error(code=1000, message='Missing payload')

    try:
        fmodel = deserialize_ModelNew(model, api.models.Model.objects.get(pk=model_id))
    except:
        return Error(code=1000, message='Model %d does not exists'%model_id)        

    fmodel.save()
    
    return serialize_Model(fmodel)
