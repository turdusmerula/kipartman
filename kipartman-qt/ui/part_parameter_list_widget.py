from PyQt6 import Qt6
from PyQt6 import QtWidgets, uic

from api.command import commands
from api.data.part_parameter import PartParameterColumn, PartParameterModel, PartParameterGroup, KicadPartParameterNode, PartParameterNode, CommandDeletePartParameters
from api.event import events

class QPartParameterListWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(QPartParameterListWidget, self).__init__(*args, **kwargs)
        uic.loadUi('ui/part_parameter_list_widget.ui', self)

        self.model = PartParameterModel()
        self.treeView.setModel(self.model)
        self.treeView.selectionModel().selectionChanged.connect(self.update_menus)

        events.focusChanged.connect(self.update_menus)

        self.update_menus()

    def update(self):
        # update treeview
        self.model.Update()
        super(QPartParameterListWidget, self).update()

    def update_menus(self):
        from ui.main_window import main_window
        if main_window is None:
            return
        
        if self.treeView.hasFocus()==False:
            return
            
        main_window.actionParameterAdd.setEnabled(True)
        try: main_window.actionParameterAdd.triggered.disconnect()
        except: pass
        main_window.actionParameterAdd.triggered.connect(self.actionPartParameterAddTriggered)
        
        if len(self.treeView.selectedIndexes())>0:
            main_window.actionParameterDelete.setEnabled(True)
        try: main_window.actionParameterDelete.triggered.disconnect()
        except: pass
        main_window.actionParameterDelete.triggered.connect(self.actionPartParameterDeleteTriggered)

        
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

    def actionPartParameterAddTriggered(self):
        parent = self.treeView.model().FindPartParameterGroupNode(PartParameterGroup.PARAMETER)
        self.treeView.editNew(parent=self.treeView.model().index_from_node(parent))
        
    def actionPartParameterDeleteTriggered(self):
        nodes = []
        for index in self.treeView.selectionModel().selectedRows():
            node = self.treeView.model().node_from_id(index.internalId())
            if isinstance(node, PartParameterNode):
                nodes.append(node.part_parameter)

        if len(nodes)>0:
            commands.Do(CommandDeletePartParameters, part_parameters=nodes)
            self.treeView.selectionModel().clearSelection()
            commands.LastUndo.done.connect(
                lambda treeView=self.treeView: 
                    treeView.selectionModel().clearSelection()
            )
    