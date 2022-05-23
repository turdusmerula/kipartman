from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtCore import QModelIndex
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTreeView, QHeaderView, QAbstractItemView

from api.treeview import TreeModel, Node, TreeColumn, ValidationError, QTreeViewData
from api.command import CommandUpdateDatabaseField, CommandAddDatabaseObject, CommandDeleteDatabaseObjects, commands
from api.event import events
from api.unit import ureg
import database.data.storage
from database.models import Storage
from enum import Enum

class CommandUpateStorage(CommandUpdateDatabaseField):
    def __init__(self, storage, field, value, other_fields):
        super(CommandUpateStorage, self).__init__(object=storage, field=field, value=value, other_fields=other_fields,
                                            description=f"change storage {field} to '{value}'")

class CommandAddStorage(CommandAddDatabaseObject):
    def __init__(self, storage):
        super(CommandAddStorage, self).__init__(object=storage,
                                            description=f"add new storage")

class CommandDeleteStorages(CommandDeleteDatabaseObjects):
    def __init__(self, storages):
        if isinstance(storages, list) and len(storages)>1:
            objects = storages
            description = f"delete {len(storages)} storages"
        elif isinstance(storages, list) and len(storages)==1:
            objects = storages
            description = f"delete storage '{storages[0].name}'"
        else:
            objects = [storages]
            description = f"delete storage '{storages.name}'"
        
        super(CommandDeleteStorages, self).__init__(objects=objects,
                                            description=description)

class StorageColumn():
    NAME = 0
    DESCRIPTION = 1

    
class StorageNode(Node):
    def __init__(self, storage):
        super(StorageNode, self).__init__()
        self.storage = storage

    def GetValue(self, column):
        if column==StorageColumn.NAME:
            return self.storage.name
        elif column==StorageColumn.DESCRIPTION:
            return self.storage.description
        return None

    def GetEditValue(self, column):
        return self.GetValue(column)

    def SetValue(self, column, value):
        field = {
            StorageColumn.NAME: "name",
            StorageColumn.DESCRIPTION: "description"
        }
        
        other_fields = {}
        
        if self.storage.id is None:
            # item has not yet be commited at this point and have no id
            # set edited field value
            setattr(self.storage, field[column], value)
            if self.storage.name!="":
                # save object in database
                commands.Do(CommandAddStorage, storage=self.storage)
            return True
        else:
            if column in field and getattr(self.storage, field[column])!=value:
                commands.Do(CommandUpateStorage, storage=self.storage, field=field[column], value=value, other_fields=other_fields)
                return True
        return False

    def Validate(self, column, value):
        if column==StorageColumn.NAME:
            if value!=self.storage.name and len(database.models.Storage.objects.filter(name=value).all())>0:
                return ValidationError(f"Storage '{value}' already exists")
        return None

class StorageModel(TreeModel):
    def __init__(self):
        super(StorageModel, self).__init__()

        self.InsertColumn(TreeColumn("Name"))
        self.InsertColumn(TreeColumn("Description"))

        self.loaded = False
        self.id_to_storage_node = {}

    def index_from_storage(self, storage):
        if storage.id not in self.id_to_storage_node:
            return QModelIndex()
        node = self.id_to_storage_node[storage.id]
        return self.index_from_node(node)

    def storage_node_from_id(self, id):
        return self.id_to_storage_node[id]

    def CanFetchMore(self, parent):
        return not self.loaded

    def Fetch(self, parent):
        # create a state
        nodes = self.node_to_id.copy()
        del nodes[self.rootNode] # remove root node
        
        for storage in database.data.storage.find():
            storage_node = self.FindStorage(storage)
            if storage_node is None:
                storage_node = self.AddStorage(storage)
            else:
                del nodes[storage_node]
        
        # remove remaining nodes
        self.RemoveNodes(list(nodes.keys()))
        self.loaded = True

    def FindStorage(self, storage):
        for node in self.node_to_id:
            if isinstance(node, StorageNode) and node.storage is storage:
                return node
        return None

    def AddStorage(self, storage, pos=None):
        node = StorageNode(storage)
        self.id_to_storage_node[storage.id] = node

        self.InsertNode(node, pos=pos)

    def RemoveStorageId(self, id):
        node = self.storage_node_from_id(id)
        del self.id_to_storage_node[id]
        self.RemoveNode(node)

    def RemoveStorage(self, storage):
        node = self.storage_node_from_id(storage.id)
        self.loaded = False
        del self.id_to_storage_node[storage.id]
        self.RemoveNode(node)

    def CreateEditNode(self, parent):
        return StorageNode(Storage())

class QStorageTreeView(QTreeViewData):
    def __init__(self, *args, **kwargs):
        super(QStorageTreeView, self).__init__(*args, **kwargs)
    
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        
        self.endInsertEditNode.connect(self.OnEndInsertEditNode)

    def setModel(self, model):
        super(QStorageTreeView, self).setModel(model)
        
        self.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)        

    def OnEndInsertEditNode(self, node):
        storage = node.storage
        self.setCurrentIndex(self.model().index_from_storage(storage))
        
        # add code to select item on redo in this current view only
        commands.LastUndo.done.connect(
            lambda treeView=self, storage=storage: 
                self.setCurrentIndex(treeView.model().index_from_storage(storage))
        )
    
