from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtCore import QModelIndex
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTreeView, QHeaderView, QAbstractItemView

from api.treeview import TreeModel, Node, TreeColumn, ValidationError, QTreeViewData
from api.command import CommandUpdateDatabaseField, CommandAddDatabaseObject, CommandDeleteDatabaseObjects, commands
from api.event import events
from api.unit import ureg
import database.data.parameter
from database.models import Parameter

class Column():
    NAME = 0
    UNIT = 1
    VALUE_TYPE = 2
    DESCRIPTION = 3

class ParameterNode(Node):
    def __init__(self, parameter):
        super(ParameterNode, self).__init__()
        self.parameter = parameter
        
    def GetValue(self, column):
        if column==Column.NAME:
            return self.parameter.name
        elif column==Column.UNIT:
            return self.parameter.unit
        elif column==Column.VALUE_TYPE:
            return self.parameter.value_type
        elif column==Column.DESCRIPTION:
            return self.parameter.description
        return None

    def GetFlags(self, column, flags):
        return flags & ~Qt.ItemFlag.ItemIsEditable

class ParameterModel(TreeModel):
    def __init__(self):
        super(ParameterModel, self).__init__()

        self.InsertColumn(TreeColumn("Name"))
        self.InsertColumn(TreeColumn("Unit"))
        self.InsertColumn(TreeColumn("Value type"))
        self.InsertColumn(TreeColumn("Description"))

        self.loaded = False
        self.filter = None
        
    def CanFetchMore(self, parent):
        return not self.loaded

    def Fetch(self, parent):
        # create a state
        nodes = self.node_to_id.copy()
        del nodes[self.rootNode] # remove root node
        
        for parameter in database.data.parameter.find():
            parameter_node = self.FindParameter(parameter)
            if parameter_node is None:
                if self.MatchFilter(parameter)==True:
                    parameter_node = self.AddParameter(parameter)
            else:
                del nodes[parameter_node]
        
        # remove remaining nodes
        self.RemoveNodes(list(nodes.keys()))
        self.loaded = True

    def MatchFilter(self, parameter):
        if self.filter is None:
            return True
        for name in parameter.name:
            if self.filter.casefold() in name.casefold():
                return True
        if self.filter.casefold() in parameter.description.casefold():
            return True
        return False
    
    def FindParameter(self, parameter):
        for node in self.node_to_id:
            if isinstance(node, ParameterNode) and node.parameter is parameter:
                return node
        return None

    def AddParameter(self, parameter, pos=None):
        node = ParameterNode(parameter)
        self.InsertNode(node, pos=pos)
        
    def RemoveParameter(self, parameter):
        node = self.parameter_node_from_id(parameter.id)
        self.RemoveNode(node)

    def SetFilter(self, filter):
        self.filter = filter
        self.loaded = False
        
class QParameterTreeView(QTreeViewData):
    def __init__(self, *args, **kwargs):
        super(QParameterTreeView, self).__init__(*args, **kwargs)
    
    def setModel(self, model):
        super(QParameterTreeView, self).setModel(model)
        
        self.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)        
