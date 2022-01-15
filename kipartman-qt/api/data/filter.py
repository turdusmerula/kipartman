from PyQt6.QtCore import QObject, pyqtSignal, QSize
from PyQt6.QtCore import QModelIndex
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtWidgets import QTreeView, QHeaderView

from api.treeview import TreeModel, Node, Column, QTreeViewData
from api.command import CommandUpdateDatabaseField, CommandAddDatabaseObject, CommandDeleteDatabaseObjects, commands
from api.event import events
from api.filter import Filter


class GroupNode(Node):
    def __init__(self, group):
        super(GroupNode, self).__init__()
        self.group = group
        
        self.font = QFont()
        self.font.setBold(True)

        self.background = QColor(128, 128, 128)
        self.foreground = QColor(255, 255, 255)
        
    def GetValue(self, column):
        if column==0:
            return self.group.description
        return None

    def GetFlags(self, column, flags):
        return flags | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

    def GetFont(self, column):
        return self.font

    def GetBackground(self, column):
        return self.background

    def GetForeground(self, column):
        return self.foreground

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
        return not self.loaded
    
    def Fetch(self, parent=None):
        # create a state
        nodes = self.node_to_id.copy()
        del nodes[self.rootNode] # remove root node
        
        for group in self.filter.groups:
            if len(group.filters)>0:
                group_node = self.FindGroup(group)
                if group_node is None:
                    group_node = self.AddGroup(group)
                else:
                    del nodes[group_node]
                
                for filter in group.filters:
                    filter_node = self.FindFilter(filter)
                    if filter_node is None:
                        filter_node = self.AddFilter(filter, group)
                    else:
                        del nodes[filter_node]
        
        # remove remaining nodes
        self.RemoveNodes(list(nodes.keys()))
        self.loaded = True
    
    def SetValue(self, node, column, value):
        # model not editable
        return False

    def FindGroup(self, group):
        for node in self.node_to_id:
            if isinstance(node, GroupNode) and node.group is group:
                return node
        return None

    def FindFilter(self, filter):
        for node in self.node_to_id:
            if isinstance(node, FilterNode) and node.filter is filter:
                return node
        return None

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
        # we want the last column to be edited whatever item column is edited in first place 
        # as the last column contains the close button
        node = self.node_from_id(index.internalId())
        return self.index_from_node(node, column=1) 

    def Update(self):
        self.loaded = False
        self.layoutChanged.emit()
    
class QFilterTreeView(QTreeViewData):
    def __init__(self, *args, **kwargs):
        super(QFilterTreeView, self).__init__(*args, **kwargs)

    def setModel(self, model):
        super(QFilterTreeView, self).setModel(model)
        
        self.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)        
        
        self.setAlternatingRowColors(True)
        self.setIndentation(0)

    def rowsInserted(self, parent, first, last):
        if self.isExpanded(parent)==False:
            self.expand(parent)

        # span first column for group nodes to make a title line
        node = self.model().node_from_id(parent.internalId())
        if isinstance(node, GroupNode):
            parent_index = self.model().index_from_node(node.parent)
            self.setFirstColumnSpanned(node.parent.row_from_child(node), parent_index, True)
            
    def sizeHintForIndex(self, index):
        node = self.model().node_from_id(index.internalId())
        hint = super(QFilterTreeView, self).sizeHintForIndex(index)
        if isinstance(node, GroupNode):
            hint.setWidth(0)
        return hint
