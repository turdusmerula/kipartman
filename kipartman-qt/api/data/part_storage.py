from PyQt6.QtCore import QRunnable, QThreadPool, QModelIndex
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import QAbstractItemView, QHeaderView

from enum import Enum

from api.treeview import TreeModel, Node, TreeColumn, ValidationError, QTreeViewData
from api.command import CommandUpdateDatabaseField, CommandAddDatabaseObject, CommandDeleteDatabaseObjects, commands
from api.event import events
from api.unit import ureg, Quantity
import database.data.part_storage
from database.models import Part, Storage, PartStorage
from ui.combobox_delegate import QComboboxDelegate

class CommandUpatePartStorage(CommandUpdateDatabaseField):
    def __init__(self, part_storage, field, value, other_fields):
        super(CommandUpatePartStorage, self).__init__(object=part_storage, field=field, value=value, other_fields=other_fields,
                                            description=f"change part storage {field} to '{value}'")

class CommandAddPartStorage(CommandAddDatabaseObject):
    def __init__(self, part_storage, fields):
        super(CommandAddPartStorage, self).__init__(object=part_storage, fields=fields,
                                            description=f"add new part storage")

class CommandDeletePartStorages(CommandDeleteDatabaseObjects):
    def __init__(self, part_storages):
        if isinstance(part_storages, list) and len(part_storages)>1:
            objects = part_storages
            description = f"delete {len(part_storages)} part storages"
        elif isinstance(part_storages, list) and len(part_storages)==1:
            objects = part_storages
            description = f"delete part storage '{part_storages[0].storage.name}'"
        else:
            objects = [part_storages]
            description = f"delete part storage '{part_storages.storage.name}'"
        
        super(CommandDeletePartStorages, self).__init__(objects=objects,
                                            description=description)


class PartStorageColumn():
    STORAGE = 0
    QUANTITY = 1

class PartStorageNode(Node):
    def __init__(self, part_storage, parent=None):
        super(PartStorageNode, self).__init__(parent)
        self.part_storage = part_storage

    def GetValue(self, column):
        if column==PartStorageColumn.STORAGE:
            if hasattr(self.part_storage, 'storage'):
                return self.part_storage.storage.name
        elif column==PartStorageColumn.QUANTITY:
            return self.part_storage.quantity
        return None

    def GetEditValue(self, column):
        if column==PartStorageColumn.STORAGE:
            if hasattr(self.part_storage, 'storage'):
                return self.part_storage.storage
            else:
                return None
        elif column==PartStorageColumn.QUANTITY:
            return self.part_storage.quantity
        return self.GetValue(column)

    def SetValue(self, column, value):
        field = {
            PartStorageColumn.STORAGE: "storage",
            PartStorageColumn.QUANTITY: "quantity",
        }

        other_fields = {}

        if self.part_storage.id is None:
            # item has not yet been commited at this point and have no id
            # set edited field value
            setattr(self.part_storage, field[column], value)
            if hasattr(self.part_storage, 'storage'):
                # save object in database
                commands.Do(CommandAddPartStorage, part_storage=self.part_storage, fields=other_fields)
            return True
        else:
            if column in field and getattr(self.part_storage, field[column])!=value:
                commands.Do(CommandUpatePartStorage, part_storage=self.part_storage, field=field[column], value=value, other_fields=other_fields)
                return True
        return False

            
    def Validate(self, column, value):
        if column==PartStorageColumn.QUANTITY:
            if value<0:
                return ValidationError(f"Quantity must be greater than 0")
        return None

class PartStorageModel(TreeModel):
    def __init__(self):
        super(PartStorageModel, self).__init__()

        # TODO remove Unit and merge it with value
        self.InsertColumn(TreeColumn("Storage"))
        self.InsertColumn(TreeColumn("Quantity"))

        self.loaded = False        
        self.part = None

    def SetPart(self, part):
        self.part = part

    def index_from_part_storage_id(self, id):
        node = self.FindPartStorageNode(id)
        return self.index_from_node(node)
    
    def CanFetchMore(self, parent):
        return not self.loaded

    def Fetch(self, parent):
        print("PartStorageModel.Fetch")
        
        self.SaveState()
            
        # prevent recursive Fetch
        self.loaded = True

        if self.part is not None:
            for part_storage in self.part.storages.all():
                part_storage_node = self.FindPartStorageNode(part_storage.id)
                if part_storage_node is None:
                    part_storage_node = self.AddPartStorage(part_storage, header=self.FindPartStorageGroupNode(PartStorageGroup.PARAMETER))
                else:
                    part_storage_node.part_storage = part_storage
                    self.UpdateNode(part_storage_node)
        
        # remove remaining nodes
        self.PurgeState()

    def Update(self):
        self.loaded = False
        super(PartStorageModel, self).Update()
        
    def Clear(self):
        self.loaded = False
        super(PartStorageModel, self).Clear()

    def CreateEditNode(self, parent):
        if self.part is None:
            return None
        
        if self.part.instance==PartInstance.PART:
            return PartStorageNode(PartStorage(part=self.part, metastorage=False))
        elif self.part.instance==PartInstance.METAPART:
            return PartStorageNode(PartStorage(part=self.part, metastorage=True))
        return None

    def FindPartStorageNode(self, id):
        for node in self.node_to_id:
            if isinstance(node, PartStorageNode) and node.part_storage.id==id:
                return node
        return None

    def AddPartStorage(self, part_storage, header, pos=None):
        node = PartStorageNode(part_storage)
        self.InsertNode(node, pos=pos, parent=header)

    def RemovePartStorageId(self, id):
        node = self.part_storage_node_from_id(id)
        self.RemoveNode(node)

    def RemovePartStorage(self, part_storage):
        node = self.part_storage_node_from_id(part_storage.id)
        self.RemoveNode(node)


class QPartStorageTreeView(QTreeViewData):
    def __init__(self, *args, **kwargs):
        super(QPartStorageTreeView, self).__init__(*args, **kwargs)
    
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        
        self.endInsertEditNode.connect(self.OnEndInsertEditNode)

        events.objectUpdated.connect(self.objectChanged)
        events.objectAdded.connect(self.objectChanged)
        events.objectDeleted.connect(self.objectChanged)


    def setModel(self, model):
        super(QPartStorageTreeView, self).setModel(model)
        
        self.storageSelectDelegate = QComboboxDelegate(model, items=[])


    def SetPart(self, part):
        self.model().SetPart(part)

    def getItemDelegate(self, index):
        if self.model() is None:
            return None
        
        node = self.model().node_from_index(index)
        
        if index.column()==PartStorageColumn.STORAGE:
            return self.storageSelectDelegate
            
        return None

    def objectChanged(self, object):
        if isinstance(object, PartStorage) or (isinstance(object, Part) and object==self.model().part) or isinstance(object, Storage):
            self.model().Update()
            
    def OnEndInsertEditNode(self, node):
        part_storage = node.part_storage
        self.setCurrentIndex(self.model().index_from_part_storage_id(part_storage.id))
        
        # add code to select item on redo in this current view only
        commands.LastUndo.done.connect(
            lambda treeView=self, part_storage=part_storage: 
                self.setCurrentIndex(treeView.model().index_from_part_storage_id(part_storage.id))
        )
    
