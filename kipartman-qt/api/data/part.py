from PyQt6.QtCore import QRunnable, QThreadPool
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtCore import Qt

from api.treeview import TreeModel, Node, Column
import database.data.part
from time import sleep

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

        self.id_to_category = {}
        self.id_to_part = {}
        self.loaded = {
            self.rootNode: False
        }
        self.has_child = {
            self.rootNode: True
        }

        self.request = None
        
    def CanFetchMore(self, parent):
        return not self.loaded[parent]

    def Fetch(self, parent):
        if self.request is None:
            self.request = database.data.part.find().iterator()
        
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

part_model = PartModel()
