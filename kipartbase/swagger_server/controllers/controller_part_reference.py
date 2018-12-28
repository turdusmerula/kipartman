import connexion
from swagger_server.models.part_reference import PartReference

from swagger_server.models.error import Error
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

import api.models

def serialize_PartReference(fpart_reference, part_reference=None):
    if part_reference is None:
        part_reference = PartReference()
    part_reference.name = fpart_reference.name
    if fpart_reference.description:
        part_reference.description = fpart_reference.description
    part_reference.manufacturer = fpart_reference.manufacturer
    part_reference.type = fpart_reference.type
    part_reference.uid = fpart_reference.uid
    if fpart_reference.updated:
        part_reference.updated = fpart_reference.updated
    return part_reference

def deserialize_PartReference(part_reference, fpart_reference=None):
    if fpart_reference is None:
        fpart_reference = api.models.PartReference()
    fpart_reference.name = part_reference.name
    if part_reference.description:
        fpart_reference.description = part_reference.description
    fpart_reference.manufacturer = part_reference.manufacturer
    fpart_reference.type = part_reference.type
    fpart_reference.uid = part_reference.uid
    if part_reference.updated:
        fpart_reference.description = part_reference.updated
    return fpart_reference

def find_part_references(part_id):
    """
    find_references
    Return all references

    :rtype: List[Reference]
    """
    references = []

    try:
        fpart = api.models.Part.objects.get(pk=part_id)
    except:
        return Error(code=1000, message='Part %d does not exists'%part_id), 403
    
    for freference in fpart.references.all():
        references.append(serialize_PartReference(freference))

    return references
