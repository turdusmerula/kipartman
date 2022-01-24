from PyQt6 import Qt6
from PyQt6 import QtWidgets, uic

from api.data.part_parameter import PartParameterModel
from ui.parameter_select_delegate import QParameterSelectDelegate

class QPartParameterListWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(QPartParameterListWidget, self).__init__(*args, **kwargs)
        uic.loadUi('ui/part_parameter_list_widget.ui', self)

        self.model = PartParameterModel()
        self.treeView.setModel(self.model)
        self.treeView.selectionModel().selectionChanged.connect(self.update_menus)

        self.parameterSelectDelegate = QParameterSelectDelegate(self.model)
        self.treeView.setItemDelegateForColumn(0, self.parameterSelectDelegate) 


        from ui.main_window import app
        app.focusChanged.connect(self.update_menus)

        self.update_menus()

    def update(self):
        # update treeview
        self.model.Update()
        super(QPartParameterListWidget, self).update()

    def update_menus(self):
        from ui.main_window import main_window
        if main_window is None:
            return
        
        main_window.actionParameterAdd.setEnabled(False)
        main_window.actionParameterDelete.setEnabled(False)

        main_window.actionSelectNone.setEnabled(False)
        main_window.actionSelectAll.setEnabled(False)

        if self.treeView.hasFocus()==False:
            return

            
        main_window.actionParameterAdd.setEnabled(True)
        try: main_window.actionParameterAdd.triggered.disconnect()
        except: pass
        main_window.actionParameterAdd.triggered.connect(self.OnActionParameterAddTriggered)
        
        if len(self.treeView.selectedIndexes())>0:
            main_window.actionParameterDelete.setEnabled(True)
        try: main_window.actionParameterDelete.triggered.disconnect()
        except: pass
        main_window.actionParameterDelete.triggered.connect(self.OnActionParameterDeleteTriggered)

        
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

    def OnActionParameterAddTriggered(self):
        self.treeView.editNew(parent=self.treeView.rootIndex())
        
    def OnActionParameterDeleteTriggered(self):
        pass
