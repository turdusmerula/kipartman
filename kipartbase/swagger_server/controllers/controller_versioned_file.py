import connexion
from swagger_server.models.versioned_file import VersionedFile 
from swagger_server.models.versioned_file_data import VersionedFileData
from swagger_server.controllers.helpers import raise_on_error, ControllerError

from swagger_server.models.error import Error
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime
import json

import api.models
import api.versioned_file_storage

from django.db.models import Q

from os.path import expanduser
home = expanduser("~")

def serialize_VersionedFileData(ffile, file=None):
    if file is None:
        file = VersionedFileData()
    file.source_path = ffile.source_path
    file.storage_path = ffile.storage_path
    file.md5 = ffile.md5
    file.version = ffile.version
    file.metadata = ffile.metadata
    #ffile.state is private
    file.updated = ffile.updated
    return file

def serialize_VersionedFile(ffile, file=None):
    if file is None:
        file = VersionedFile()
    file.id = ffile.id
    serialize_VersionedFileData(ffile, file)
    return file

def deserialize_VersionedFile(file, ffile=None):
    if ffile is None:
        ffile = api.models.VersionedFile()
    ffile.source_path = file.source_path
    ffile.storage_path = file.storage_path
    ffile.md5 = file.md5
    ffile.version = file.version
    ffile.metadata = file.metadata
    #ffile.state is private
    ffile.updated = file.updated
    return ffile


def update_file_state(file):
    # possibles states:
    #  conflict_add
    #  conflict_change
    #  conflict_del
    #  income_add
    #  income_change
    #  income_del
    #  outgo_add
    #  outgo_change
    #  outgo_del
    #  error
    
    ffile = None
    try:
        if file.id:
            ffile = api.models.VersionedFile.objects.get(id=file.id)
        else:
            ffile = api.models.VersionedFile.objects.get(source_path=file.source_path)
    except:
        pass

    if file.state is None or file.state=='conflict_add' or file.state=='conflict_change' or file.state=='conflict_del':
        file.state = ''
        
#    if not file.version and ffile:
#        file.version = 1 
#        file.version = ffile.version 
    
    if ffile and file.version and file.version>ffile.version:
        return Error(code=1000, message='Inconsistent version for file %s'%file.source_path)
    
    if ffile and ffile.state==api.models.VersionedFileState.deleted:
        ffile = None

    if not file.id and ffile:
        file.id = ffile.pk
        
    if file.state=='':
        if ffile and file.md5==ffile.md5:
            file.state = ''
        if ffile and ( file.md5!=ffile.md5 or file.source_path!=ffile.source_path or file.metadata!=ffile.metadata):
            file.state = 'outgo_change'
        if not ffile:
            file.state = 'outgo_add'

    if file.state=='income_add' or file.state=='income_change' or file.state=='income_del':
        pass
    
    if file.state=='outgo_add' or file.state=='outgo_change' or file.state=='outgo_del':
        if ffile and ( file.md5!=ffile.md5 or file.source_path!=ffile.source_path):
            file.state = 'outgo_change'
        if not ffile:
            file.state = 'outgo_add'

    if ffile and file.version and file.version<ffile.version:
        file.state = 'income_change'
    
    if ffile and not file.version:
        if file.md5==ffile.md5:
            file.version = ffile.version
        else:
            file.state = 'conflict_add'
            
    if file.state=='outgo_add':
        file.id = None
        file.version = None

    if file.state=='outgo_add' and ffile:
        if file.md5==ffile.md5:
            file.state = ''
        else:
            file.state = 'conflict_add'
    
    if file.state=='outgo_change' and ffile and file.version<ffile.version:       
        file.state = 'conflict_change'
    
    if file.state=='outgo_del' and (
            ( ffile and ffile.state==api.models.VersionedFileState.deleted ) 
            or 
            ( not ffile )):       
        file.state = 'conflict_del'
    
def synchronize_versioned_files(files=None, root_path=None):
    """
    synchronize_versioned_files
    Get synchronization status of a fileset
    :param files: File list to test synchronization
    :type files: list | bytes
    :param root_path: Path from which to synchronize
    :type root_path: str

    :rtype: List[VersionedFile]
    """
    sync_files = []

    if connexion.request.is_json:
        files = [VersionedFile.from_dict(d) for d in connexion.request.get_json()]


    exclude_id = []
    # check given files
    for file in files:
        if file.source_path:
            raise_on_error(update_file_state(file))
            sync_files.append(file)
            if file.id:
                exclude_id.append(file.id)
        
    # check files not in list
    ffile_request = api.models.VersionedFile.objects
    # limit to root_path
    if root_path:
        ffile_request = ffile_request.filter(source_path__startswith=root_path)
    # exclude files already given in input
    if len(exclude_id)>0:
        ffile_request = ffile_request.filter(~Q(id__in=exclude_id))
    # exclude deleted files
    ffile_request = ffile_request.exclude(state=api.models.VersionedFileState.deleted)
     
    for ffile in ffile_request.all(): 
        file = serialize_VersionedFile(ffile)
        file.state = 'income_add'
        sync_files.append(file)
    
    return sync_files

def commit_versioned_files(files, force=None):
    """
    commit_versioned_files
    Commit a fileset
    :param files: File list to commit
    :type files: list | bytes
    :param force: Force commit
    :type force: bool

    :rtype: List[VersionedFileStatus]
    """
    commit_files = []
    conflict_files = []
    
    if connexion.request.is_json:
        files = [VersionedFile.from_dict(d) for d in connexion.request.get_json()]
    print "---", files
    if force is None:
        force = False

    to_add = []
    to_change = []
    to_delete = []
    
    #  conflict_change
    #  conflict_del
    #  income_add
    #  income_change
    #  income_del
    #  outgo_add
    #  outgo_change
    #  outgo_del

    has_conflicts = False
    # check if given files are allowed to commit 
    for file in files:
        raise_on_error(update_file_state(file))
        if force==False and ( file.state=='conflict_change' or file.state=='conflict_del' or file.state=='conflict_add' ):
            has_conflicts = True
            conflict_files.append(file)
        elif file.state=='outgo_add' or file.state=='conflict_add':
            to_add.append(file)
        elif file.state=='outgo_change' or file.state=='conflict_change':
            to_change.append(file)
        elif file.state=='outgo_del' or file.state=='conflict_del':
            to_delete.append(file)
    
    if has_conflicts and force==False:
        # in case of a conflict return conflicted files
        return conflict_files, 403
    
    storage = api.versioned_file_storage.VersionedFileStorage()
    for file in to_add:
        # add file to file storage
        if not file.content is None:
            commit_files.append(storage.add_file(file))
        else:
            return [file], 403

    for file in to_change:
        # modify file to file storage
        if not file.content is None:
            commit_files.append(storage.add_file(file))
        else:
            return [file], 403
        
    for file in to_delete:
        # delete file to file storage
        commit_files.append(storage.delete_file(file))
    
    return commit_files 

def update_versioned_files(files, force=None):
    """
    update_versioned_files
    Update a fileset
    :param files: File list to update
    :type files: list | bytes

    :rtype: List[VersionedFile]
    """
    update_files = []
    conflict_files = []
    
    if connexion.request.is_json:
        files = [VersionedFile.from_dict(d) for d in connexion.request.get_json()]
    
    if force is None:
        force = False

    to_update = []
    to_delete = []
    
    #  conflict_change
    #  conflict_del
    #  income_add
    #  income_change
    #  income_del
    #  outgo_add
    #  outgo_change
    #  outgo_del

    has_conflicts = False
    # check if given files are allowed to commit 
    for file in files:
        raise_on_error(update_file_state(file))
        if force==False and ( file.state=='conflict_change' or file.state=='conflict_del' or file.state=='conflict_add' ):
            has_conflicts = True
            conflict_files.append(file)
        elif file.state=='conflict_add' or file.state=='outgo_add':
            file.state = 'income_add'
            to_update.append(file)
        elif file.state=='conflict_change' or file.state=='outgo_change':
            file.state = 'income_change'
            to_update.append(file)
        elif file.state=='conflict_del' or file.state=='outgo_del':
            file.state = 'income_del'
            to_update.append(file)
        elif file.state=='income_add':
            to_update.append(file)
        elif file.state=='income_change':
            to_update.append(file)
        elif file.state=='income_del':
            to_delete.append(file)
    
    if has_conflicts and force==False:
        # in case of a conflict return conflicted files
        return conflict_files, 403
    
    storage = api.versioned_file_storage.VersionedFileStorage()
    for file in to_update:
        ffile = api.models.VersionedFile.objects.get(id=file.id)
        file = serialize_VersionedFile(ffile, file)
        file.content = storage.get_file_content(file.id)
        update_files.append(file)
    
    for file in to_delete:
        update_files.append(file)

    print "----", update_files
    return update_files 
