from PyQt6 import Qt6
from PyQt6 import QtWidgets, uic

from api.treeview import TreeManager
from api.data.part import part_model

class PartListWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        super(PartListWidget, self).__init__(parent)
        uic.loadUi('ui/part_list_widget.ui', self)

        self.manager = TreeManager(tree_view=self.treeView, model=part_model, context_menu=None)
        
        self.update_menus()
        self.load()

    def load(self):
        pass

    def update_menus(self):
        pass

