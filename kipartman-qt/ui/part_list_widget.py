from PyQt6 import Qt6
from PyQt6 import QtWidgets, uic

from api.treeview import TreeManager
from api.data.part import PartModel

class PartListWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        super(PartListWidget, self).__init__(parent)
        uic.loadUi('ui/part_list_widget.ui', self)

        self.model = PartModel()
        self.manager = TreeManager(tree_view=self.treeView, model=self.model, context_menu=None)
        
        self.update_menus()

    def update(self):
        # update treeview
        self.model.Update()
        super(PartListWidget, self).update()

    def update_menus(self):
        #update menus
        from ui.main_window import main_window
        main_window.actionPartAddPart.setEnabled(True)
        main_window.actionPartAddMetapart.setEnabled(True)
        main_window.actionPartImportOctopart.setEnabled(True)
        main_window.actionPartRemovePart.setEnabled(True)
