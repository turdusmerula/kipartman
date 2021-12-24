from PyQt6.QtCore import QRunnable, QThreadPool
from PyQt6.QtCore import QObject, pyqtSignal

from api.treeview import TreeModel, TreeItem, TreeAsyncLoader
from api.treeview import BaseTreeModel, BaseNode, BaseColumn
import database.data.part
from time import sleep

class PartAsyncLoader(TreeAsyncLoader):
    def run(self):
        items = []
        
        def emit(force=False):
            nonlocal items
            
            if len(items)==1000 or (force==True and len(items)>0):
                self.on_data.signal.emit(None, items)
                items = []
                emit()

        for part in database.data.part.find():
            items.append(part)

        emit(force=True)

class PartNode(BaseNode):
    def __init__(self, part, parent=None):
        super(PartNode, self).__init__(parent)
        self.part = part

class PartModel(BaseTreeModel):
    def __init__(self):
        super(PartModel, self).__init__(loader=PartAsyncLoader)
        
        self.InsertColumn(BaseColumn("ID"))
        self.InsertColumn(BaseColumn("Name"))
        self.InsertColumn(BaseColumn("Description"))
        
    def OnData(self, parent, items):
        nodes = []
        for part in items:
            nodes.append(PartNode(part))
        self.InsertNodes(nodes)
    
    def GetValue(self, node, column):
        if column==0:
            return node.part.id
        elif column==1:
            return node.part.name
        elif column==2:
            return node.part.description
        
part_model = PartModel()
