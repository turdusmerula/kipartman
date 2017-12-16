import connexion
from swagger_server.models.upload_file import UploadFile
from swagger_server.models.upload_file_data import UploadFileData

from swagger_server.models.error import Error
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

import api.models
import api.file_storage

from os.path import expanduser
home = expanduser("~")

def serialize_UploadFileData(fupload_file, upload_file=None):
    if upload_file is None:
        upload_file = UploadFileData()
    upload_file.source_name = fupload_file.source_name
    upload_file.storage_path = fupload_file.storage_path
    return upload_file

def serialize_UploadFile(fupload_file, upload_file=None):
    if upload_file is None:
        upload_file = UploadFile()
    upload_file.id = fupload_file.id
    serialize_UploadFileData(fupload_file, upload_file)
    return upload_file


def add_upload_file(upfile=None, description=None):
    """
    add_upload_file
    Upload a file.
    :param upfile: The file to upload.
    :type upfile: werkzeug.datastructures.FileStorage
    :param description: The file to upload.
    :type description: str

    :rtype: UploadFile
    """
    storage = api.file_storage.FileStorage()
    
    fupload_file = storage.add_file(upfile)    
    return serialize_UploadFile(fupload_file)

def find_upload_file(upload_file_id):
    """
    find_upload_file
    Return a file
    :param upload_file_id: File id
    :type upload_file_id: int

    :rtype: UploadFile
    """
    
    try:
        fupload_file = api.models.File.objects.get(id=upload_file_id)
    except:
        return Error(code=1000, message='File %d does not exists'%upload_file_id), 403
    
    return serialize_UploadFile(fupload_file)
