from PyQt6 import Qt6
from PyQt6 import QtWidgets, uic

from api.data.part_parameter import PartParameterModel

class QPartParameterListWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(QPartParameterListWidget, self).__init__(*args, **kwargs)
        uic.loadUi('ui/part_parameter_list_widget.ui', self)

        self.model = PartParameterModel()
        self.treeView.setModel(self.model)
        
        self.update_menus()

    def update(self):
        # update treeview
        self.model.Update()
        super(QPartParameterListWidget, self).update()

    def update_menus(self):
        #update menus
        from ui.main_window import main_window
        # main_window.actionPartAddPart.setEnabled(True)
        # main_window.actionPartAddMetapart.setEnabled(True)
        # main_window.actionPartImportOctopart.setEnabled(True)
        # main_window.actionPartRemovePart.setEnabled(True)
