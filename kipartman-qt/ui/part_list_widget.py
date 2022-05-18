from PyQt6 import Qt6
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import pyqtSignal, QItemSelectionModel

from api.data.part import PartModel, PartNode
from api.event import events
from api.octopart.imports import import_octopart
from helper.dialog import ShowDialog, ShowErrorDialog
from ui.modal_dialog import QModalDialog
from ui.octopart_search_widget import QOctopartSearchWidget
from PyQt6.QtWidgets import QMessageBox


class QPartListWidget(QtWidgets.QWidget):
    selectionChanged = pyqtSignal(list)

    def __init__(self, parent):
        super(QPartListWidget, self).__init__(parent)
        uic.loadUi('ui/part_list_widget.ui', self)

        self.model = PartModel()
        self.treeView.setModel(self.model)
        self.treeView.selectionModel().selectionChanged.connect(self.treeViewSelectionChanged)
        
        self.owner_category = None
        
        events.focusChanged.connect(self.update_menus)

        self.update_menus()

    def update(self):
        # update treeview
        self.model.Update()
        super(QPartListWidget, self).update()

    def update_menus(self):
        from ui.main_window import main_window
        if main_window is None:
            return 

        if self.treeView.hasFocus()==False:
            return
        
        try: main_window.actionPartAddPart.triggered.disconnect()
        except: pass
        main_window.actionPartAddPart.triggered.connect(self.actionPartAddPartTriggered)

        try: main_window.actionPartAddMetapart.triggered.disconnect()
        except: pass
        main_window.actionPartAddMetapart.triggered.connect(self.actionPartAddMetapartTriggered)

        try: main_window.actionPartImportOctopart.triggered.disconnect()
        except: pass
        main_window.actionPartImportOctopart.triggered.connect(self.actionPartImportOctopartTriggered)

        try: main_window.actionPartDelete.triggered.disconnect()
        except: pass
        main_window.actionPartDelete.triggered.connect(self.actionPartDeleteTriggered)

    def SetFilters(self, filters):
        self.model.SetFilters(filters)

    def SetOwnerCategory(self, category):
        self.owner_category = category
        
    def SelectedParts(self):
        selection = []
        for index in self.treeView.selectionModel().selectedRows():
            node = self.treeView.model().node_from_id(index.internalId())
            if isinstance(node, PartNode) and node.part is not None:
                selection.append(node.part)
        return selection

    def treeViewSelectionChanged(self):
        self.selectionChanged.emit(self.SelectedParts())
        self.update_menus()


    def actionPartAddPartTriggered(self, value):
        # add a new element in edit mode
        self.treeView.setFocus()
        self.treeView.editNew(parent=self.treeView.rootIndex(), category=self.owner_category, instance='part', column=1)

    def actionPartAddMetapartTriggered(self, value):
        self.treeView.editNew(category=self.owner_category, instance='metapart', column=1)
    
    def actionPartImportOctopartTriggered(self, value):
        dialog = QModalDialog(self, title="Octopart search") 
        widget = QOctopartSearchWidget(dialog)
        dialog.setWidget(widget)
        dialog.validated.connect(self.dialogOctopartSearchValidated)
        dialog.show()

    def dialogOctopartSearchValidated(self, octoparts):
        print("---", self.owner_category)
        imported = []
        for octopart in octoparts:
            try:
                part = import_octopart(octopart, self.owner_category)
                if part is not None:
                    imported.append(part)
            except Exception as e:
                ShowErrorDialog("Import from octopart", text=f"Import failed for part '{octopart['mpn']}'", detailed_text=f"{e}")
        ShowDialog("Import from octopart", text=f"{len(imported)}/{len(octoparts)} parts imported", buttons=QMessageBox.StandardButton.Ok)
        # self.parameter = object
        # self.widget.lineEdit.setText(self.parameter.name[0])

    def actionPartDeleteTriggered(self, value):
        pass