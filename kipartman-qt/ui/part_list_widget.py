from PyQt6 import Qt6
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import pyqtSignal, QItemSelectionModel

from api.data.part import PartModel


class QPartListWidget(QtWidgets.QWidget):
    selectionChanged = pyqtSignal(QItemSelectionModel)

    def __init__(self, parent):
        super(QPartListWidget, self).__init__(parent)
        uic.loadUi('ui/part_list_widget.ui', self)

        self.model = PartModel()
        self.treeView.setModel(self.model)
        self.treeView.selectionModel().selectionChanged.connect(self.treeViewSelectionChanged)
        
        from ui.main_window import app
        app.focusChanged.connect(self.update_menus)

        self.update_menus()

    def update(self):
        # update treeview
        self.model.Update()
        super(QPartListWidget, self).update()

    def update_menus(self):
        from ui.main_window import main_window
        if main_window is None:
            return 
        
        main_window.actionPartAddPart.setEnabled(False)
        main_window.actionPartAddMetapart.setEnabled(False)
        main_window.actionPartImportOctopart.setEnabled(False)
        main_window.actionPartRemovePart.setEnabled(False)

        if self.treeView.hasFocus()==False:
            return
        
        main_window.actionPartAddPart.setEnabled(True)
        main_window.actionPartAddMetapart.setEnabled(True)
        main_window.actionPartImportOctopart.setEnabled(True)
        main_window.actionPartRemovePart.setEnabled(True)

    def SetFilters(self, filters):
        self.model.SetFilters(filters)

    def treeViewSelectionChanged(self):
        self.update_menus()
        self.selectionChanged.emit(self.treeView.selectionModel())
    