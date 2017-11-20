import connexion
from swagger_server.models.distributor import Distributor
from swagger_server.models.distributor_data import DistributorData
from swagger_server.models.distributor_new import DistributorNew

from swagger_server.models.error import Error
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

import api.models
#import jsonpickle

def serialize_DistributorData(fdistributor, distributor=None):
    if distributor is None:
        distributor = DistributorData()
    distributor.name = fdistributor.name
    distributor.address = fdistributor.address
    distributor.website = fdistributor.website
    distributor.sku_url = fdistributor.sku_url
    distributor.email = fdistributor.email
    distributor.phone = fdistributor.phone
    distributor.comment = fdistributor.comment
    distributor.allowed = fdistributor.allowed
    return distributor

def serialize_Distributor(fdistributor, distributor=None):
    if distributor is None:
        distributor = Distributor()
    distributor.id = fdistributor.id
    serialize_DistributorData(fdistributor, distributor)
    return distributor


def deserialize_DistributorData(distributor, fdistributor=None):
    if fdistributor is None:
        fdistributor = api.models.Distributor()
    fdistributor.name = distributor.name
    fdistributor.address = distributor.address
    fdistributor.website = distributor.website
    fdistributor.sku_url = distributor.sku_url
    fdistributor.email = distributor.email
    fdistributor.phone = distributor.phone
    fdistributor.comment = distributor.comment
    fdistributor.allowed = distributor.allowed
    return fdistributor


def deserialize_DistributorNew(distributor, fdistributor=None):
    fdistributor = deserialize_DistributorData(distributor, fdistributor)
    return fdistributor


def add_distributor(distributor):
    """
    add_distributor
    Creates a new distributor
    :param distributor: Distributor to add
    :type distributor: dict | bytes

    :rtype: Distributor
    """
    if connexion.request.is_json:
        distributor = DistributorNew.from_dict(connexion.request.get_json())

    fdistributor = deserialize_DistributorNew(distributor)
    fdistributor.save()
    
    return serialize_Distributor(fdistributor)


def delete_distributor(distributor_id):
    """
    delete_distributor
    Delete distributor
    :param distributor_id: Distributor id
    :type distributor_id: int

    :rtype: None
    """
    try:
        fdistributor = api.models.Distributor.objects.get(pk=distributor_id)
    except:
        return Error(code=1000, message='Distributor %d does not exists'%distributor_id), 403
    # delete distributor
    fdistributor.delete()
    return None


def find_distributor(distributor_id):
    """
    find_distributor
    Return a distributor
    :param distributor_id: Distributor id
    :type distributor_id: int

    :rtype: Distributor
    """
    try:
        fdistributor = api.models.Distributor.objects.get(pk=distributor_id)
    except:
        return Error(code=1000, message='Distributor %d does not exists'%distributor_id), 403
    
    distributor = serialize_Distributor(fdistributor)
    return distributor

def find_distributors(name=None):
    """
    find_distributors
    Return all distributors
    :param name: Search distributors matching name
    :type name: str

    :rtype: List[Distributor]
    """
    distributors = []

    fdistributors_query = api.models.Distributor.objects
    if name:
        fdistributors_query = fdistributors_query.filter(name=name)
        
    for fdistributor in fdistributors_query.all():
        distributors.append(serialize_Distributor(fdistributor))

    return distributors

def update_distributor(distributor_id, category):
    """
    update_distributor
    Update a distributor
    :param distributor_id: Distributor id
    :type distributor_id: int
    :param category: Distributor to update
    :type category: dict | bytes

    :rtype: Distributor
    """
    if connexion.request.is_json:
        distributor = DistributorNew.from_dict(connexion.request.get_json())
    else:
        return Error(code=1000, message='Missing payload'), 403
    try:
        fdistributor = deserialize_DistributorNew(distributor, api.models.Distributor.objects.get(pk=distributor_id))
    except:
        return Error(code=1000, message='Distributor %d does not exists'%distributor_id), 403
        
    fdistributor.save()
    
    return distributor
