from PyQt6 import Qt6
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QStandardItem, QStandardItemModel

from api.treeview import TreeManager
from api.data.part_category import part_category_model

    # ExpandableRole = QtCore.Qt.UserRole + 500

    # def hasChildren(self, index):
    #     if self.data(index, StandardItemModel.ExpandableRole):
    #         return True
    #     return super(StandardItemModel, self).hasChildren(index)

class PartCategoryListWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        super(PartCategoryListWidget, self).__init__(parent)
        uic.loadUi('ui/part_category_list_widget.ui', self)

        self.manager = TreeManager(tree_view=self.treeView, model=part_category_model, context_menu=None)
        
        self.update_menus()
        self.load()

    def load(self):
        self.manager.model.Load()

    def update_menus(self):
        pass

