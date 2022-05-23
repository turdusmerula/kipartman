from PyQt6 import Qt6
from PyQt6 import QtWidgets, uic

from api.command import commands
from api.data.part_storage import PartStorageColumn, PartStorageModel, PartStorageNode, CommandDeletePartStorages
from api.event import events

class QPartStorageListWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(QPartStorageListWidget, self).__init__(*args, **kwargs)
        uic.loadUi('ui/part_storage_list_widget.ui', self)

        self.model = PartStorageModel()
        self.treeView.setModel(self.model)
        self.treeView.selectionModel().selectionChanged.connect(self.update_menus)

        events.focusChanged.connect(self.update_menus)

        self.update_menus()

    def update(self):
        # update treeview
        self.model.Update()
        super(QPartStorageListWidget, self).update()

    def update_menus(self):
        from ui.main_window import main_window
        if main_window is None:
            return
        
        if self.treeView.hasFocus()==False:
            return
            
        main_window.actionPartStorageAdd.setEnabled(True)
        try: main_window.actionPartStorageAdd.triggered.disconnect()
        except: pass
        main_window.actionPartStorageAdd.triggered.connect(self.actionPartStorageAddTriggered)
        
        if len(self.treeView.selectedIndexes())>0:
            main_window.actionPartStorageDelete.setEnabled(True)
        try: main_window.actionPartStorageDelete.triggered.disconnect()
        except: pass
        main_window.actionPartStorageDelete.triggered.connect(self.actionPartStorageDeleteTriggered)

        
        main_window.actionSelectNone.setEnabled(True)
        try: main_window.actionSelectNone.triggered.disconnect()
        except: pass
        main_window.actionSelectNone.triggered.connect(self.UnselectAll)

        main_window.actionSelectAll.setEnabled(True)
        try: main_window.actionSelectAll.triggered.disconnect()
        except: pass
        main_window.actionSelectAll.triggered.connect(self.SelectAll)

    def SetPart(self, part):
        self.treeView.SetPart(part)
        self.model.Update()

    def UnselectAll(self):
        self.treeView.clearSelection()
    
    def SelectAll(self):
        self.treeView.selectAll(selectChilds=True)

    def actionPartStorageAddTriggered(self):
        parent = self.treeView.model().FindPartStorageGroupNode(PartStorageGroup.PARAMETER)
        self.treeView.editNew(parent=self.treeView.model().index_from_node(parent))
        
    def actionPartStorageDeleteTriggered(self):
        nodes = []
        for index in self.treeView.selectionModel().selectedRows():
            node = self.treeView.model().node_from_id(index.internalId())
            if isinstance(node, PartStorageNode):
                nodes.append(node.part_storage)

        if len(nodes)>0:
            commands.Do(CommandDeletePartStorages, part_storages=nodes)
            self.treeView.selectionModel().clearSelection()
            commands.LastUndo.done.connect(
                lambda treeView=self.treeView: 
                    treeView.selectionModel().clearSelection()
            )
    