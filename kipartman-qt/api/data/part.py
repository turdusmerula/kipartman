from PyQt6.QtCore import Qt, QObject, pyqtSignal
from PyQt6.QtWidgets import QTreeView, QHeaderView

from api.treeview import TreeModel, Node, Column, QTreeViewData
from api.command import Command, CommandUpdateDatabaseField, commands
from api.event import events
import database.data.part
from database.models import Part


class CommandUpatePart(CommandUpdateDatabaseField):
    def __init__(self, part, field, value):
        super(CommandUpatePart, self).__init__(object=part, field=field, value=value,
                                            description=f"change part {field} to '{value}'")


class PartNode(Node):
    def __init__(self, part, parent=None):
        super(PartNode, self).__init__(parent)
        self.part = part

class PartCategoryNode(Node):
    def __init__(self, part, parent=None):
        super(PartCategoryNode, self).__init__(parent)
        self.category = category

class PartModel(TreeModel):
    def __init__(self):
        super(PartModel, self).__init__()
        
        self.InsertColumn(Column("ID"))
        self.InsertColumn(Column("Name"))
        self.InsertColumn(Column("Description"))

        self.filters = None

        self.id_to_part = {}
        self.loaded = {
            self.rootNode: False
        }
        self.has_child = {
            self.rootNode: True
        }

        self.request = None
    
    def SetFilters(self, filters):
        self.filters = filters 
    
    def CanFetchMore(self, parent):
        return not self.loaded[parent]

    def Fetch(self, parent):
        if self.request is None:
            self.request = database.data.part.find(self.filters).iterator()
        
        nodes = []
        try:
            while(len(nodes)<10):
                part = next(self.request)
                node = PartNode(part)
                self.id_to_part[part.id] = node
                
                if part.metapart==True:
                    self.loaded[node] = False
                    self.has_child[node] = True
                else:
                    self.loaded[node] = True
                    self.has_child[node] = False

                nodes.append(node)
        except StopIteration:
            self.loaded[parent] = True
        self.InsertNodes(nodes)

    def HasChildren(self, parent):
        return self.has_child[parent]

    def GetValue(self, node, column):
        if column==0:
            return node.part.id
        elif column==1:
            return node.part.name
        elif column==2:
            return node.part.description

    def GetFlags(self, node, column, flags):
        if column==0:
            return flags & ~Qt.ItemFlag.ItemIsEditable
        return flags

    def SetValue(self, node, column, value):
        field = {
            1: "name",
            2: "description"
        }
        if column in field and getattr(node.part, field[column])!=value:
            commands.Do(CommandUpatePart, part=node.part, field=field[column], value=value)
            return True

        return False

    def Clear(self):
        self.id_to_part.clear()
        self.loaded.clear()
        self.has_child.clear()
        self.request = None
        
        super(PartModel, self).Clear()

        self.loaded[self.rootNode] = False
        self.has_child[self.rootNode] = True

    def Update(self):
        self.Clear()


class QPartTreeView(QTreeViewData):
    def __init__(self, *args, **kwargs):
        super(QPartTreeView, self).__init__(*args, **kwargs)

    def setModel(self, model):
        super(QPartTreeView, self).setModel(model)
        
        self.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)        
