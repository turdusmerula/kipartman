from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtCore import QModelIndex
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTreeView, QHeaderView

from api.treeview import TreeModel, Node, Column, QTreeViewData
from api.command import CommandUpdateDatabaseField, CommandAddDatabaseObject, CommandDeleteDatabaseObjects, commands
from api.event import events
from api.filter import Filter


class GroupNode(Node):
    def __init__(self, group):
        super(GroupNode, self).__init__()
        self.group = group

    def GetValue(self, column):
        if column==0:
            return self.group.description
        return None

    def GetFlags(self, column, flags):
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

class FilterNode(Node):
    def __init__(self, filter):
        super(FilterNode, self).__init__()
        self.filter = filter
        
    def GetValue(self, column):
        if column==0:
            return self.filter.name
        elif column==1:
            return self.filter.description
        return None

    def GetFlags(self, column, flags):
        if column==0:
            flags |= Qt.ItemFlag.ItemIsUserCheckable
        return flags | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

class FilterModel(TreeModel):
    def __init__(self, filter):
        super(FilterModel, self).__init__()
        self.filter = filter

        self.InsertColumn(Column("Filter"))
        self.InsertColumn(Column("Content"))

        self.group_to_node = {}
        self.loaded = False
        
    def CanFetchMore(self, parent):
        """ Called each time user scrolls out of tree, overload to indicate if there is more data"""
        return not self.loaded
    
    def Fetch(self, parent=None):
        for group in self.filter.groups:
            if len(group.filters)>0:
                group_node = self.AddGroup(group)
                for filter in group.filters:
                    filter_node = self.AddFilter(filter, group)
        self.loaded = True
    
    def SetValue(self, node, column, value):
        # model not editable
        return False

    def AddGroup(self, group):
        node = GroupNode(group)
        self.group_to_node[group] = node 
        self.InsertNode(node)
        return node
    
    def AddFilter(self, filter, group):
        parent = self.group_to_node[group]
        node = FilterNode(filter)
        self.InsertNode(node, parent=parent)
        return node
    
    def Clear(self):
        self.group_to_node.clear()
        self.loaded = False
        super(FilterModel, self).Clear()

    def Buddy(self, index):
        # we want the last column to be edited whateved item is edited in first place 
        # as the last column contains the close button
        node = self.node_from_id(index.internalId())
        return self.index_from_node(node, column=1) 

class QFilterTreeView(QTreeViewData):
    def __init__(self, *args, **kwargs):
        super(QFilterTreeView, self).__init__(*args, **kwargs)

    def setModel(self, model):
        super(QFilterTreeView, self).setModel(model)
        
        self.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)        
        #self.setColumnWidth(0, 10)
