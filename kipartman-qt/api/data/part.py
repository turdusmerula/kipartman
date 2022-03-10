from PyQt6.QtCore import Qt, QObject, pyqtSignal
from PyQt6.QtWidgets import QTreeView, QHeaderView

from api.treeview import TreeModel, Node, TreeColumn, QTreeViewData
from api.command import Command, CommandUpdateDatabaseField, commands, CommandAddDatabaseObject, CommandDeleteDatabaseObjects
from api.event import events
import database.data.part
from database.models import Part, PartInstance

class CommandUpatePart(CommandUpdateDatabaseField):
    def __init__(self, part, field, value, other_fields):
        super(CommandUpatePart, self).__init__(object=part, field=field, value=value, other_fields=other_fields,
                                            description=f"change part {field} to '{value}'")

class CommandAddPart(CommandAddDatabaseObject):
    def __init__(self, part, fields):
        super(CommandAddPart, self).__init__(object=part, fields=fields,
                                            description=f"add new part")

class CommandDeleteParts(CommandDeleteDatabaseObjects):
    def __init__(self, parts):
        if isinstance(parts, list) and len(parts)>1:
            objects = parts
            description = f"delete {len(parts)} parts"
        elif isinstance(parts, list) and len(parts)==1:
            objects = parts
            description = f"delete part '{parts[0].name}'"
        else:
            objects = [parts]
            description = f"delete part '{parts.name}'"
        
        super(CommandDeleteParts, self).__init__(objects=objects,
                                            description=description)


class PartNode(Node):
    def __init__(self, part, parent=None):
        super(PartNode, self).__init__(parent)
        self.part = part

    def GetValue(self, column):
        if column==0:
            return self.part.id
        elif column==1:
            return self.part.name
        elif column==2:
            return self.part.description

    def GetFlags(self, column, flags):
        if column==0:
            return flags & ~Qt.ItemFlag.ItemIsEditable
        return flags

    def SetValue(self, column, value):
        field = {
            1: "name",
            2: "description"
        }
        if column in field and getattr(self.part, field[column])!=value:
            commands.Do(CommandUpatePart, part=self.part, field=field[column], value=value)
            return True

        return False

    def HasChildren(self):
        return self.part.instance==PartInstance.METAPART

class OctopartNode(Node):
    def __init__(self, octopart, parent=None):
        super(OctopartNode, self).__init__(parent)
        self.part = part

    def GetValue(self, column):
        return None

    def GetFlags(self, column, flags):
        return flags & ~Qt.ItemFlag.ItemIsEditable

class LoadMoreNode(Node):
    def __init__(self, parent=None):
        super(LoadMoreNode, self).__init__(parent)

class PartCategoryNode(Node):
    def __init__(self, part, parent=None):
        super(PartCategoryNode, self).__init__(parent)
        self.category = category

class PartModel(TreeModel):
    def __init__(self):
        super(PartModel, self).__init__()
        
        self.InsertColumn(TreeColumn("ID"))
        self.InsertColumn(TreeColumn("Name"))
        self.InsertColumn(TreeColumn("Description"))

        self.filters = None

        self.id_to_part = {}
        self.loaded = {
            self.rootNode: False
        }

        self.request = None
    
    def SetFilters(self, filters):
        self.filters = filters 
    
    def CanFetchMore(self, parent):
        return not self.loaded[parent]

    def Fetch(self, parent):
        if parent is self.rootNode:
            self.FetchParts()
        elif parent.part.instance==PartInstance.METAPART:
            self.FetchMetapart(parent)
    
    def FetchParts(self):
        if self.request is None:
            self.request = database.data.part.find(self.filters).iterator()
        
        nodes = []
        try:
            while(len(nodes)<10):
                part = next(self.request)
                node = PartNode(part)
                self.id_to_part[part.id] = node
                
                if part.instance==PartInstance.METAPART:
                    self.loaded[node] = False
                else:
                    self.loaded[node] = True

                nodes.append(node)
        except StopIteration:
            self.loaded[self.rootNode] = True
        self.InsertNodes(nodes)
    
    def FetchMetapart(self, metapart):
        # add database parts
        
        # add octopart parts
        
        # add loading node
        pass
    
    def Clear(self):
        self.id_to_part.clear()
        self.loaded.clear()
        self.request = None
        
        super(PartModel, self).Clear()

        self.loaded[self.rootNode] = False

    def Update(self):
        self.Clear()

    def CreateEditNode(self, parent, category, instance):
        return PartNode(Part(category=category, instance=instance))

class QPartTreeView(QTreeViewData):
    def __init__(self, *args, **kwargs):
        super(QPartTreeView, self).__init__(*args, **kwargs)

    def setModel(self, model):
        super(QPartTreeView, self).setModel(model)
        
        self.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)        

    def OnObjectUpdated(self, object):
        if isinstance(object, Part)==False:
            return 
        part = object
        if part.id in self.model().id_to_part_node:
            self.model().id_to_part_node[part.id].part.refresh_from_db()
            self.model().layoutChanged.emit()

    def OnObjectAdded(self, object):
        if isinstance(object, Part)==False:
            return 
        part = object
        if part.id not in self.model().id_to_part_node:
            self.model().AddPart(part)
            
    def OnObjectDeleted(self, object, id):
        if isinstance(object, Part)==False:
            return 
        part = object
        if id in self.model().id_to_part_node:
            node = self.model().id_to_part_node[id]
            self.model().RemovePartId(id)

    def OnEndInsertEditNode(self, node):
        part = node.part
        self.setCurrentIndex(self.model().index_from_part(part))
        
        # add code to select item on redo in this current view only
        commands.LastUndo.done.connect(
            lambda treeView=self, part=part: 
                self.setCurrentIndex(treeView.model().index_from_part(part))
        )
    
