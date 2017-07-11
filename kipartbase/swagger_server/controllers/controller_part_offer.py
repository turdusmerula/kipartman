import connexion
from swagger_server.models.part_offer import PartOffer
from swagger_server.models.part_offer_data import PartOfferData

from swagger_server.models.error import Error
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

from swagger_server.controllers.controller_unit import find_unit, find_unit_prefix

import api.models
#import jsonpickle

def serialize_PartOfferData(fpart_offer, part_offer=None):
    if part_offer is None:
        part_offer = PartOfferData()
    part_offer.packaging_unit = fpart_offer.packaging_unit
    part_offer.quantity = fpart_offer.quantity
    part_offer.unit_price = fpart_offer.unit_price
    part_offer.currency = fpart_offer.currency
    part_offer.sku = fpart_offer.sku
    part_offer.updated = fpart_offer.updated
    
    return part_offer

def serialize_PartOffer(fpart_offer, part_offer=None):
    if part_offer is None:
        part_offer = PartOffer()
    part_offer.id = fpart_offer.id
    serialize_PartOfferData(fpart_offer, part_offer)
    return part_offer

def deserialize_PartOffer(part_offer, fpart_offer=None):
    if fpart_offer is None:
        fpart_offer = api.models.PartOffer()
    fpart_offer.packaging_unit = part_offer.packaging_unit
    fpart_offer.quantity = part_offer.quantity
    fpart_offer.unit_price = part_offer.unit_price
    fpart_offer.currency = part_offer.currency
    fpart_offer.sku = part_offer.sku
    if part_offer.updated:
        fpart_offer.updated = part_offer.updated
    else:
        fpart_offer.updated = datetime.now()
    return fpart_offer

def find_part_offers(part_id, distributor_id):
    
    offers = []
    for foffer in api.models.PartOffer.objects.filter(part=part_id).filter(distributor=distributor_id).all():
        offers.append(serialize_PartOffer(foffer))
        
    return offers
