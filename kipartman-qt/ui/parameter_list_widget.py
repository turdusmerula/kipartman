from PyQt6 import Qt6
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QEvent, pyqtSignal
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import QAbstractItemView

from api.command import CommandUpdateDatabaseField, CommandAddDatabaseObject, CommandDeleteDatabaseObject, commands
from api.data.parameter import ParameterModel, ParameterNode, CommandDeleteParameters, CommandAddParameter
from api.event import events
from database.models import Parameter
from helper.dialog import ShowErrorDialog
from ui.combobox_alias_delegate import ComboboxAliasDelegate
from ui.unit_delegate import QUnitDelegate
from ui.combobox_delegate import QComboboxDelegate


class QParameterListWidget(QtWidgets.QWidget):
    selectionChanged = pyqtSignal(list)

    def __init__(self, *args, **kwargs):
        super(QParameterListWidget, self).__init__(*args, **kwargs)
        uic.loadUi('ui/parameter_list_widget.ui', self)

        self.model = ParameterModel()
        self.treeView.setModel(self.model)
        self.treeView.selectionModel().selectionChanged.connect(self.update_menus)

        self.nameAliasDelegate = ComboboxAliasDelegate(self.model)
        self.treeView.setItemDelegateForColumn(0, self.nameAliasDelegate) 

        self.unitDelegate = QUnitDelegate(self.model)
        self.treeView.setItemDelegateForColumn(1, self.unitDelegate) 

        self.valueTypeDelegate = QComboboxDelegate(self.model, ["float", "integer", "text"])
        self.treeView.setItemDelegateForColumn(2, self.valueTypeDelegate) 

        from ui.main_window import app
        app.focusChanged.connect(self.update_menus)

        self.update_menus()
        
    def update(self):
        # update treeview
        self.model.Update()
        super(QParameterListWidget, self).update()

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
        # add a new element in edit mode
        self.treeView.editNew(parent=self.treeView.rootIndex())
        # node = self.manager.InsertEditNode()
        
        # # self.manager.CloseEditor()
        # self.i = 1000
        # from database.models import Parameter
        # parameter = Parameter(id=self.i, name="a")
        # self.i += 1
        # self.model.AddParameter(parameter, pos=1)
        # self.manager.tree_view.setCurrentIndex(self.model.index_from_parameter(parameter))
        # # self.manager.tree_view.rowsAboutToBeRemoved(self.manager.model.index_from_node(self.model.rootNode), 1, 1)
        # self.model.RemoveParameter(parameter)
        
    def OnActionParameterDeleteTriggered(self):
        # nodes = []
        # for index in self.treeView.selectionModel().selectedRows():
        #     node = self.treeView.model().node_from_id(index.internalId())
        #     if isinstance(node, PartCategoryNode) and node.part_category is not None:
        #         if node.part_category.has_dependencies()==True:
        #             ShowErrorDialog("Remove failed", f"Part category '{node.part_category.name}' not empy")
        #             return
        #         if node not in nodes:
        #             nodes.append(node.part_category)
        # if len(nodes)>0:
        #     commands.Do(CommandDeletePartCategories, part_categories=nodes)
        #     self.treeView.selectionModel().clearSelection()
        #     commands.LastUndo.done.connect(
        #         lambda treeView=self.treeView: 
        #             treeView.selectionModel().clearSelection()
        #     )
        # else:
        #     ShowWarningDialog("Remove failed", "No part category to remove")
        pass
