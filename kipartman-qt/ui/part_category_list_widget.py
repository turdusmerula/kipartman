from PyQt6 import Qt6
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QEvent, pyqtSignal
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import QAbstractItemView

from api.command import CommandUpdateDatabaseField, CommandAddDatabaseObject, CommandDeleteDatabaseObject, commands
from api.data.part_category import PartCategoryModel, PartCategoryNode, CommandDeletePartCategories, CommandAddPartCategory
from api.event import events
from api.filter import FilterSet, FilterGroup
from database.models import PartCategory
from helper.dialog import ShowErrorDialog


class QPartCategoryListWidget(QtWidgets.QWidget):
    selectionChanged = pyqtSignal(list)

    def __init__(self, *args, **kwargs):
        super(QPartCategoryListWidget, self).__init__(*args, **kwargs)
        uic.loadUi('ui/part_category_list_widget.ui', self)

        self.model = PartCategoryModel()
        self.treeView.setModel(self.model)
        self.treeView.selectionModel().selectionChanged.connect(self.treeViewSelectionChanged)

        events.focusChanged.connect(self.update_menus)

        self.update_menus()
        
    def update(self):
        # update treeview
        self.model.Update()
        super(QPartCategoryListWidget, self).update()

    def update_menus(self):
        from ui.main_window import main_window
        if main_window is None:
            return
        
        main_window.actionCategoryAdd.setEnabled(False)
        main_window.actionCategoryDelete.setEnabled(False)

        main_window.actionSelectNone.setEnabled(False)
        main_window.actionSelectAll.setEnabled(False)
        main_window.actionSelectChildMode.setEnabled(False)

        if self.treeView.hasFocus()==False:
            return

        main_window.actionCategoryAdd.setEnabled(True)
        if self.treeView.isSelectedRoot()==False:
            main_window.actionCategoryDelete.setEnabled(True)
            
        try: main_window.actionCategoryAdd.triggered.disconnect()
        except: pass
        main_window.actionCategoryAdd.triggered.connect(self.actionCategoryAddTriggered)
        
        try: main_window.actionCategoryDelete.triggered.disconnect()
        except: pass
        main_window.actionCategoryDelete.triggered.connect(self.actionCategoryDeleteTriggered)

        
        main_window.actionSelectNone.setEnabled(True)
        try: main_window.actionSelectNone.triggered.disconnect()
        except: pass
        main_window.actionSelectNone.triggered.connect(self.UnselectAll)

        main_window.actionSelectAll.setEnabled(True)
        try: main_window.actionSelectAll.triggered.disconnect()
        except: pass
        main_window.actionSelectAll.triggered.connect(self.SelectAll)

        main_window.actionSelectChildMode.setEnabled(True)
        try: main_window.actionSelectChildMode.triggered.disconnect()
        except: pass
        main_window.actionSelectChildMode.triggered.connect(self.actionSelectChildModeTriggered)

    def UnselectAll(self):
        self.treeView.clearSelection()
    
    def SelectAll(self):
        self.treeView.selectAll(selectChilds=True)

    def SelectedCategories(self):
        selection = []
        for index in self.treeView.selectionModel().selectedRows():
            node = self.treeView.model().node_from_id(index.internalId())
            if isinstance(node, PartCategoryNode) and node.part_category is not None:
                selection.append(node.part_category)
        return selection

    def actionCategoryAddTriggered(self):
        # add a new element in edit mode
        self.treeView.setFocus()
        self.treeView.editNew()
        
    def actionCategoryDeleteTriggered(self):
        nodes = []
        for index in self.treeView.selectionModel().selectedRows():
            node = self.treeView.model().node_from_id(index.internalId())
            if isinstance(node, PartCategoryNode) and node.part_category is not None:
                if node.part_category.has_dependencies()==True:
                    ShowErrorDialog("Remove failed", f"Part category '{node.part_category.name}' not empy")
                    return
                if node not in nodes:
                    nodes.append(node.part_category)
        if len(nodes)>0:
            commands.Do(CommandDeletePartCategories, part_categories=nodes)
            self.treeView.selectionModel().clearSelection()
            commands.LastUndo.done.connect(
                lambda treeView=self.treeView: 
                    treeView.selectionModel().clearSelection()
            )
        else:
            ShowWarningDialog("Remove failed", "No part category to remove")
    
    def treeViewSelectionChanged(self, selected, deselected):
        self.selectionChanged.emit(self.SelectedCategories())
        self.update_menus()
        

    def actionSelectChildModeTriggered(self, checked):
        self.treeView.setSelectChildMode(checked)
        self.treeViewSelectionChanged(None, None)
    