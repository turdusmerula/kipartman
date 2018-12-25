import connexion
from swagger_server.models.part_attachement import PartAttachement

from swagger_server.models.error import Error
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

from swagger_server.controllers.helpers import raise_on_error, ControllerError
from swagger_server.controllers.controller_upload_file import find_upload_file

import api.models
#import jsonpickle

def serialize_PartAttachement(fpart_attachement, part_attachement=None):
    if part_attachement is None:
        part_attachement = PartAttachement()
    
    file = raise_on_error(find_upload_file(fpart_attachement.file.id))
    part_attachement.id = fpart_attachement.file.id
    part_attachement.description = fpart_attachement.description
    part_attachement.source_name = file.source_name
    part_attachement.storage_path = file.storage_path
    return part_attachement

def deserialize_PartAttachement(part_attachement, fpart_attachement=None):
    if fpart_attachement is None:
        fpart_storage = api.models.PartAttachement()
    fpart_attachement.description = part_attachement.description
    return fpart_attachement

    
def find_part_attachements(part_id):
    """
    find_attachements
    Return all attachements

    :rtype: List[Attachement]
    """
    attachements = []

    try:
        fpart = api.models.Part.objects.get(pk=part_id)
    except:
        return Error(code=1000, message='Part %d does not exists'%part_id), 403
    
    for fattachement in fpart.attachements.all():
        attachements.append(serialize_PartAttachement(fattachement))

    return attachements
