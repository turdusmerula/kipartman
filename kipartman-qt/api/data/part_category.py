from PyQt6.QtCore import QRunnable, QThreadPool
from PyQt6.QtCore import QObject, pyqtSignal

from api.treeview import TreeModel, TreeItem, TreeAsyncLoader
from api.treeview import BaseTreeModel, BaseNode, BaseColumn
import database.data.part_category
from time import sleep

class PartCategoryAsyncLoader(TreeAsyncLoader):
    def run(self):
        to_load = []
        
        items = []
        for category in database.data.part_category.find_childs():
            items.append(category)
            to_load.append(category)
        self.on_data.signal.emit(None, items)
        
        while len(to_load)>0:
            items = []
            category = to_load.pop()
            for childcategory in database.data.part_category.find_childs(category):
                items.append(childcategory)
                to_load.append(childcategory)
            if len(items)>0:
                self.on_data.signal.emit(category, items)

class PartCategoryNode(BaseNode):
    def __init__(self, category):
        super(PartCategoryNode, self).__init__()
        self.category = category
    
class PartCategoryModel(BaseTreeModel):
    def __init__(self):
        super(PartCategoryModel, self).__init__(loader=PartCategoryAsyncLoader)

        self.InsertColumn(BaseColumn("ID"))
        self.InsertColumn(BaseColumn("Name"))
        self.InsertColumn(BaseColumn("Description"))

    def OnData(self, parent, items):
        nodes = []
        for category in items:
            nodes.append(PartCategoryNode(category))
        self.InsertNodes(nodes) #, parent=)
        
    def GetValue(self, node, column):
        if column==0:
            return node.category.id
        elif column==1:
            return node.category.name
        elif column==2:
            return node.category.description
        
    
part_category_model = PartCategoryModel()

