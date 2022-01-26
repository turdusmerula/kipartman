from PyQt6 import Qt6
from PyQt6 import QtWidgets, uic

from api.data.part_parameter import PartParameterModel
from api.event import events
from ui.parameter_select_delegate import QParameterSelectDelegate
from ui.unit_delegate import QUnitDelegate

class QPartParameterListWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(QPartParameterListWidget, self).__init__(*args, **kwargs)
        uic.loadUi('ui/part_parameter_list_widget.ui', self)

        self.model = PartParameterModel()
        self.treeView.setModel(self.model)
        self.treeView.selectionModel().selectionChanged.connect(self.update_menus)

        self.parameterSelectDelegate = QParameterSelectDelegate(self.model)
        self.treeView.setItemDelegateForColumn(0, self.parameterSelectDelegate) 

        self.unitDelegate = QUnitDelegate(self.model)
        self.treeView.setItemDelegateForColumn(2, self.unitDelegate) 

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
        main_window.actionParameterAdd.triggered.connect(self.actionParameterAddTriggered)
        
        if len(self.treeView.selectedIndexes())>0:
            main_window.actionParameterDelete.setEnabled(True)
        try: main_window.actionParameterDelete.triggered.disconnect()
        except: pass
        main_window.actionParameterDelete.triggered.connect(self.actionParameterDeleteTriggered)

        
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
        self.model.Clear()

    def UnselectAll(self):
        self.treeView.clearSelection()
    
    def SelectAll(self):
        self.treeView.selectAll(selectChilds=True)

    def actionParameterAddTriggered(self):
        self.treeView.editNew(parent=self.treeView.rootIndex())
        
    def actionParameterDeleteTriggered(self):
        pass

    