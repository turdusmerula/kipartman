from PyQt6 import Qt6
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QStandardItem, QStandardItemModel

from api.treeview import TreeManager
from api.command import commands
from api.data.part_category import PartCategoryModel, PartCategoryNode, PartCategoryManager, CommandAddPartCategory
from database.models import PartCategory

class PartCategoryListWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        super(PartCategoryListWidget, self).__init__(parent)
        uic.loadUi('ui/part_category_list_widget.ui', self)

        self.model = PartCategoryModel()
        self.manager = PartCategoryManager(tree_view=self.treeView, model=self.model, context_menu=None)
        
        self.update_menus()
        
    def update(self):
        # update treeview
        self.model.Update()
        super(PartCategoryListWidget, self).update()

    def update_menus(self):
        #update menus
        from ui.main_window import main_window
        main_window.actionCategoryAdd.setEnabled(True)
        main_window.actionCategoryDelete.setEnabled(True)

        try: main_window.actionCategoryAdd.triggered.disconnect()
        except: pass
        main_window.actionCategoryAdd.triggered.connect(self.OnActionCategoryAddTriggered)
        
        try: main_window.actionCategoryDelete.triggered.disconnect()
        except: pass
        main_window.actionCategoryDelete.triggered.connect(self.OnActionCategoryDeleteTriggered)
        
    def OnActionCategoryAddTriggered(self):
        # add a new element in edit mode
        node = self.manager.InsertEditNode()

    def OnActionCategoryDeleteTriggered(self):
        pass
