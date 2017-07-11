import connexion
from swagger_server.models.part_distributor import PartDistributor

from swagger_server.models.error import Error
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

from swagger_server.controllers.controller_distributor import serialize_Distributor
from swagger_server.controllers.controller_part_offer import find_part_offers

import api.models
#import jsonpickle

def serialize_PartDistributor(fdistributor, part_distributor=None):
    if part_distributor is None:
        part_distributor = PartDistributor()
    serialize_Distributor(fdistributor, part_distributor)
    return part_distributor

    
def find_part_distributors(part_id):
    """
    find_distributors
    Return all distributors

    :rtype: List[Distributor]
    """
    distributors_id = []
    
    for fdistributor in api.models.PartOffer.objects.filter(part=part_id).values('distributor').distinct():
        distributors_id.append(fdistributor['distributor'])
    
    distributors = []
    for fdistributor in api.models.Distributor.objects.filter(pk__in=distributors_id).all():
        distributor = serialize_PartDistributor(fdistributor)
        distributor.offers = find_part_offers(part_id, distributor.id)
        distributors.append(distributor)

    return distributors
