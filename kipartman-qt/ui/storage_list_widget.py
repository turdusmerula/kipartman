from PyQt6 import Qt6
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QEvent, pyqtSignal
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import QAbstractItemView, QMessageBox

from api.command import commands
from api.data.storage import StorageColumn, StorageModel, StorageNode, CommandDeleteStorages, CommandAddStorage
from api.event import events
from database.models import Storage
from helper.dialog import ShowDialog


class QStorageListWidget(QtWidgets.QWidget):
    selectionChanged = pyqtSignal(list)

    def __init__(self, *args, **kwargs):
        super(QStorageListWidget, self).__init__(*args, **kwargs)
        uic.loadUi('ui/storage_list_widget.ui', self)

        self.model = StorageModel()
        self.treeView.setModel(self.model)
        self.treeView.selectionModel().selectionChanged.connect(self.update_menus)

        events.focusChanged.connect(self.update_menus)

        self.update_menus()
        
    def update(self):
        # update treeview
        self.model.Update()
        super(QStorageListWidget, self).update()

    def update_menus(self):
        from ui.main_window import main_window
        if main_window is None:
            return
        
        if self.treeView.hasFocus()==False:
            return
            
        main_window.actionStorageAdd.setEnabled(True)
        try: main_window.actionStorageAdd.triggered.disconnect()
        except: pass
        main_window.actionStorageAdd.triggered.connect(self.actionStorageAddTriggered)
        
        if len(self.treeView.selectedIndexes())>0:
            main_window.actionStorageDelete.setEnabled(True)
        try: main_window.actionStorageDelete.triggered.disconnect()
        except: pass
        main_window.actionStorageDelete.triggered.connect(self.actionStorageDeleteTriggered)

        
        main_window.actionSelectNone.setEnabled(True)
        try: main_window.actionSelectNone.triggered.disconnect()
        except: pass
        main_window.actionSelectNone.triggered.connect(self.UnselectAll)

        main_window.actionSelectAll.setEnabled(True)
        try: main_window.actionSelectAll.triggered.disconnect()
        except: pass
        main_window.actionSelectAll.triggered.connect(self.SelectAll)

    def UnselectAll(self):
        self.treeView.clearSelection()
    
    def SelectAll(self):
        self.treeView.selectAll(selectChilds=True)

    def actionStorageAddTriggered(self):
        # add a new element in edit mode
        self.treeView.editNew(parent=self.treeView.rootIndex(), column=StorageColumn.NAME)
        
    def actionStorageDeleteTriggered(self):
        nodes = []
        for index in self.treeView.selectionModel().selectedRows():
            node = self.treeView.model().node_from_id(index.internalId())
            if isinstance(node, StorageNode):
                count = len(node.storage.part_storages.all())
                if count>0:
                    res = ShowDialog("Remove confirmation", f"Storage {node.storage.name} used by {count} part{'s' if count>1 else ''}, remove anyway?", icon=QMessageBox.Icon.Question, buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                    if res==QMessageBox.StandardButton.Yes:
                        nodes.append(node.storage)
        if len(nodes)>0:
            commands.Do(CommandDeleteStorages, storages=nodes)
            self.treeView.selectionModel().clearSelection()
            commands.LastUndo.done.connect(
                lambda treeView=self.treeView: 
                    treeView.selectionModel().clearSelection()
            )