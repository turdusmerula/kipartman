from PyQt6 import Qt6
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QStandardItem, QStandardItemModel

from api.treeview import TreeManager
from api.data.part_category import PartCategoryModel

class PartCategoryListWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        super(PartCategoryListWidget, self).__init__(parent)
        uic.loadUi('ui/part_category_list_widget.ui', self)

        self.model = PartCategoryModel()
        self.manager = TreeManager(tree_view=self.treeView, model=self.model, context_menu=None)
        
        self.update_menus()
        self.load()

    def load(self):
        pass

    def update_menus(self):
        # if self.menu is None:
        #     self.menu = QtGui.QMenu(self)
        #     self.menu.addAction('Activate', lambda: self.changeStatus('table', 'Active'))
        #     self.menu.addAction('Ommit', lambda: self.changeStatus('table', 'Omitted'))
        #     self.menu.addAction('Delete', lambda: self.changeStatus('table', 'Delete'))
        pass

    def update(self):
        self.model.Update()
