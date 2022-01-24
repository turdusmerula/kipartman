from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtCore import QModelIndex
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTreeView, QHeaderView, QAbstractItemView

from api.treeview import TreeModel, Node, Column, ValidationError, QTreeViewData
from api.command import CommandUpdateDatabaseField, CommandAddDatabaseObject, CommandDeleteDatabaseObjects, commands
from api.event import events
from api.unit import ureg
import database.data.parameter
from database.models import Parameter

class ParameterNode(Node):
    def __init__(self, parameter, alias):
        super(ParameterNode, self).__init__()
        self.parameter = parameter
        self.alias = alias
        
    def GetValue(self, column):
        if column==0:
            return self.alias
        elif column==1:
            return self.parameter.unit
        elif column==2:
            return self.parameter.value_type
        elif column==3:
            return self.parameter.description
        return None

    def GetFlags(self, column, flags):
        return flags & ~Qt.ItemFlag.ItemIsEditable

class ParameterModel(TreeModel):
    def __init__(self):
        super(ParameterModel, self).__init__()

        self.InsertColumn(Column("Name"))
        self.InsertColumn(Column("Unit"))
        self.InsertColumn(Column("Value type"))
        self.InsertColumn(Column("Description"))

        self.loaded = False

    def CanFetchMore(self, parent):
        return not self.loaded

    def Fetch(self, parent):
        # create a state
        nodes = self.node_to_id.copy()
        del nodes[self.rootNode] # remove root node
        
        for parameter in database.data.parameter.find():
            parameter_node = self.FindParameter(parameter)
            if parameter_node is None:
                parameter_node = self.AddParameter(parameter)
            else:
                del nodes[parameter_node]
        
        # remove remaining nodes
        self.RemoveNodes(list(nodes.keys()))
        self.loaded = True

    def FindParameter(self, parameter):
        for node in self.node_to_id:
            if isinstance(node, ParameterNode) and node.parameter is parameter:
                return node
        return None

    def AddParameter(self, parameter, pos=None):
        node = ParameterNode(parameter, parameter.name[0])
        self.InsertNode(node, pos=pos)
        
    def RemoveParameter(self, parameter):
        node = self.parameter_node_from_id(parameter.id)
        self.RemoveNode(node)

class QParameterTreeView(QTreeViewData):
    def __init__(self, *args, **kwargs):
        super(QParameterTreeView, self).__init__(*args, **kwargs)
    
    def setModel(self, model):
        super(QParameterTreeView, self).setModel(model)
        
        self.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)        
