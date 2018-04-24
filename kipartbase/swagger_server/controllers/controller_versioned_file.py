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
import pyrfc3339

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
    file.category = ffile.category
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
    ffile.category = file.category
    #ffile.state is private
    ffile.updated = file.updated
    return ffile

def file_changed(file, ffile):
    return file.md5!=ffile.md5 or \
        file.source_path!=ffile.source_path or \
        file.metadata!=ffile.metadata         

def file_updated(file, ffile):
    print "%%%%", file.updated, ffile.updated
    if file.updated:
        return pyrfc3339.parser.parse(file.updated)>ffile.updated
    return False

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
            ffile = api.models.VersionedFile.objects.filter(id=file.id).latest('id')
        else:
            # no id, check if file can be found by path 
            ffile = api.models.VersionedFile.objects.filter(source_path=file.source_path).latest('id')
    except Exception as e:
        print "Error: %s"%format(e)
        pass
    
    if file.state is None:
        file.state = ''
    
    if file.state=='conflict_add':
        file.state = 'outgo_add'
    
    if file.state=='conflict_change':
        file.state = 'outgo_change'
    
    if file.state=='conflict_del':
        file.state = 'outgo_del'
    
    if ffile:
        if file.id is None:
            # file is new
            if ffile.state==api.models.VersionedFileState.deleted:
                file.state = 'outgo_add'
            else:
                file.state = 'conflict_add'
        else:
            # file exists in database
            if file.version and file.version>ffile.version:
                # TODO error
                pass
                
            if file.state=='' and file_changed(file, ffile):
                if ffile.state==api.models.VersionedFileState.deleted:
                    file.state = 'outgo_add'
                else:
                    file.state = 'outgo_change'
                    
            if file.version and file.version<ffile.version:
                # if version  in database is greater it means that something was commited meanwhile
                if file_updated(file, ffile):
                    if ffile.state==api.models.VersionedFileState.deleted:
                        file.state = 'conflict_del'
                    else:
                        file.state = 'conflict_change'
                else:
                    if ffile.state==api.models.VersionedFileState.deleted:
                        file.state = 'income_del'
                    else:
                        file.state = 'income_change'
            elif file.version and file.version==ffile.version:
                if ffile.state==api.models.VersionedFileState.deleted:
                    if file.state=='outgo_del':
                        file.state = 'conflict_del'
                    else:
                        file.state = 'income_del'
                elif file_changed(file, ffile):
                    if file_updated(file, ffile):
                        file.state = 'outgo_change'
                    else:
                        file.state = 'income_change'
            elif not file.version:
                if ffile.state==api.models.VersionedFileState.deleted:
                    file.state = 'outgo_add'
                else:
                    file.state = 'conflict_change'
                
    else:
        file.state = 'outgo_add'
        
    if file.state=='outgo_add':
        file.version = None
        file.id = None

def synchronize_versioned_files(files, root_path=None, category=None):
    """
    synchronize_versioned_files
    Get synchronization status of a fileset
    :param files: File list to test synchronization
    :type files: list | bytes
    :param root_path: Path from which to synchronize
    :type root_path: str
    :param category: Category of files to see
    :type category: str

    :rtype: List[VersionedFile]
    """
    print "===> synchronize_versioned_files----"
    print "*", files
    sync_files = []

    if connexion.request.is_json:
        files = [VersionedFile.from_dict(d) for d in connexion.request.get_json()]


    exclude_id = []
    exclude_path = []
    # check given files
    for file in files:
        if file.source_path:
            #print "---", file
            raise_on_error(update_file_state(file))
            #print "+++", file
            sync_files.append(file)
            if file.id:
                exclude_id.append(file.id)
            else:
                exclude_path.append(file.source_path)
     
    #print "*",   exclude_id,  exclude_path
    # check files not in list
    ffile_request = api.models.VersionedFile.objects
    # limit to category
    if category:
        ffile_request = ffile_request.filter(category=category)
    # limit to root_path
    if root_path:
        ffile_request = ffile_request.filter(source_path__startswith=root_path)
    # exclude files already given in input
    if len(exclude_id)>0:
        ffile_request = ffile_request.filter(~Q(id__in=exclude_id))
    if len(exclude_path)>0:
        ffile_request = ffile_request.filter(~Q(source_path__in=exclude_path))
    # exclude deleted files
#    ffile_request = ffile_request.filter(state=api.models.VersionedFileState.created)
    ffile_request = ffile_request.exclude(state=api.models.VersionedFileState.deleted)
     
    for ffile in ffile_request.all():
        file = serialize_VersionedFile(ffile)
        file.id = ffile.id
        file.version = ffile.version
        #file.id = None
        #file.version = None
        file.state = 'income_add'
        sync_files.append(file)
    
    #print "%%%", sync_files
    #print "------------------------------------"
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
    #print "===> commit_versioned_files----"
    commit_files = []
    conflict_files = []
    
    if connexion.request.is_json:
        files = [VersionedFile.from_dict(d) for d in connexion.request.get_json()]
    #print "---", files
    if force is None:
        force = False

    print "***", files
    
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
        if force==True:
            if file.state=='outgo_add':
                to_add.append(file)
            elif file.state=='outgo_change':
                to_change.append(file)
            elif file.state=='outgo_del':
                to_delete.append(file)
            elif file.state=='conflict_add':
                to_change.append(file)
            elif file.state=='conflict_change':
                to_change.append(file)
            elif file.state=='conflict_del':
                to_delete.append(file)
            elif file.state=='income_add' or file.state=='income_change' or file.state=='income_del':
                to_change.append(file)
        else:  
            if file.state=='conflict_change' or file.state=='conflict_del' or file.state=='conflict_add':
                has_conflicts = True
                conflict_files.append(file)
            elif file.state=='outgo_add':
                to_add.append(file)
            elif file.state=='outgo_change':
                to_change.append(file)
            elif file.state=='outgo_del':
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
    
    #print "****", commit_files
    #print "------------------------------------"
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
        #print "*", file
        raise_on_error(update_file_state(file))
        #print "**", file
        if force:
            if file.state=='conflict_add' or file.state=='outgo_add':
                file.state = 'income_add'
                to_update.append(file)
            elif file.state=='conflict_change' or file.state=='outgo_change':
                file.state = 'income_change'
                to_update.append(file)
            elif file.state=='conflict_del':
                file.state = 'income_del'
                to_delete.append(file)
            elif file.state=='outgo_del':
                file.state = 'income_add'
                to_update.append(file)
            elif file.state=='income_add':
                to_update.append(file)
            elif file.state=='income_change':
                to_update.append(file)
            elif file.state=='income_del':
                to_delete.append(file)
        else:          
            if file.state=='conflict_change' or file.state=='conflict_del' or file.state=='conflict_add':
                has_conflicts = True
                conflict_files.append(file)
            if file.state=='income_add':
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
        if file.id:
            ffile = api.models.VersionedFile.objects.filter(id=file.id).latest('id')
        else:
            ffile = api.models.VersionedFile.objects.filter(source_path=file.source_path).latest('id')            
        file = serialize_VersionedFile(ffile, file)
        file.content = storage.get_file_content(file.id)
        file.id = ffile.id
        file.version = ffile.version
        
        update_files.append(file)
    
    for file in to_delete:
        file.storage_path = None
        update_files.append(file)

    #print "----", update_files
    return update_files 

def find_versioned_file(file_id):
    try:
        ffile = api.models.VersionedFile.objects.get(pk=file_id)
    except:
        return Error(code=1000, message='File %d does not exists'%file_id), 403
    
    try:
        file = serialize_VersionedFile(ffile)
    except ControllerError as e:
        return e.error, 403
    
    return file
