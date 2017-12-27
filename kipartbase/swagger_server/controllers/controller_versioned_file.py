import connexion
from swagger_server.models.versioned_file import VersionedFile
from swagger_server.models.versioned_file_data import VersionedFileData

from swagger_server.models.error import Error
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

import api.models
import api.file_storage

from os.path import expanduser
home = expanduser("~")

def synchronize_versioned_files(files):
    """
    synchronize_versioned_files
    Get synchronization status of a fileset
    :param files: File list to test synchronization
    :type files: list | bytes

    :rtype: List[VersionedFileStatus]
    """
    sync_files = []
    
    if connexion.request.is_json:
        files = [VersionedFile.from_dict(d) for d in connexion.request.get_json()]
    
    print "---", files
    return sync_files
