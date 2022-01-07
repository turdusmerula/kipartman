from PyQt6 import Qt6
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QEvent, pyqtSignal
from PyQt6.QtGui import QStandardItem, QStandardItemModel

from api.command import commands
from api.event import events
from api.data.part_category import PartCategoryModel, PartCategoryNode, CommandDeletePartCategories, CommandAddPartCategory
from api.filter import FilterSet, FilterGroup
from database.models import PartCategory
from helper.dialog import ShowErrorDialog
from api.command import CommandUpdateDatabaseField, CommandAddDatabaseObject, CommandDeleteDatabaseObject, commands



class QPartCategoryListWidget(QtWidgets.QWidget):
    selectionChanged = pyqtSignal(list)

    def __init__(self, *args, **kwargs):
        super(QPartCategoryListWidget, self).__init__(*args, **kwargs)
        uic.loadUi('ui/part_category_list_widget.ui', self)

        self.model = PartCategoryModel()
        self.treeView.setModel(self.model)
        self.treeView.selectionModel().selectionChanged.connect(self.OnSelectionChanged)

        commands.beforeDo.connect(self.OnCommandBeforeDo)
        commands.done.connect(self.OnCommandDone)
        commands.beforeUndo.connect(self.OnCommandBeforeUndo)
        commands.undone.connect(self.OnCommandUndone)
        
        from ui.main_window import app
        app.focusChanged.connect(self.update_menus)

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
        
        if self.treeView.hasFocus()==False:
            return

        main_window.actionCategoryAdd.setEnabled(True)
        if self.treeView.isSelectedRoot()==False:
            main_window.actionCategoryDelete.setEnabled(True)
            
        try: main_window.actionCategoryAdd.triggered.disconnect()
        except: pass
        main_window.actionCategoryAdd.triggered.connect(self.OnActionCategoryAddTriggered)
        
        try: main_window.actionCategoryDelete.triggered.disconnect()
        except: pass
        main_window.actionCategoryDelete.triggered.connect(self.OnActionCategoryDeleteTriggered)

    
    def OnActionCategoryAddTriggered(self):
        # add a new element in edit mode
        self.treeView.editNew()
        # node = self.manager.InsertEditNode()
        
        # # self.manager.CloseEditor()
        # self.i = 1000
        # from database.models import PartCategory
        # part_category = PartCategory(id=self.i, name="a")
        # self.i += 1
        # self.model.AddPartCategory(part_category, pos=1)
        # self.manager.tree_view.setCurrentIndex(self.model.index_from_part_category(part_category))
        # # self.manager.tree_view.rowsAboutToBeRemoved(self.manager.model.index_from_node(self.model.rootNode), 1, 1)
        # self.model.RemovePartCategory(part_category)
        
    def OnActionCategoryDeleteTriggered(self):
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

        # def print_index(name, index):
        #     try:
        #         print(name, index, index.row(), index.column(), index.data())
        #     except Exception as e:
        #         print(name, "error")
        # print_index("currentIndex", self.treeView.selectionModel().currentIndex())
        # i = 0
        # for index in self.treeView.selectionModel().selectedIndexes():
        #     print_index(f"index {i}", index)
        #     i += 1
    
    def OnSelectionChanged(self, selected, deselected):
        selection = []
        for index in self.treeView.selectionModel().selectedRows():
            node = self.treeView.model().node_from_id(index.internalId())
            if isinstance(node, PartCategoryNode) and node.part_category is not None:
                selection.append(node.part_category)
        self.selectionChanged.emit(selection)
        
        self.update_menus()


    def OnCommandBeforeDo(self, command):
        # if isinstance(command, CommandDeletePartCategories) or isinstance(command, CommandDeletePartCategories):
        #     # revert previous state
        #     command.undone.connect(
        #         lambda treeView=self.treeView, state=self.treeView.saveState(): 
        #             treeView.loadState(state)
        #     )
        pass
    
    def OnCommandDone(self, command):
        pass
    
    def OnCommandBeforeUndo(self, command):
        # if isinstance(command, CommandAddPartCategory) or isinstance(command, CommandDeletePartCategories):
        #     # revert previous state
        #     command.undone.connect(
        #         lambda treeView=self.treeView, state=self.treeView.saveState(): 
        #             treeView.loadState(state)
        #     )
        pass

    def OnCommandUndone(self, command):
        # if isinstance(command, CommandDeletePartCategories) or isinstance(command, CommandDeletePartCategories):
        #     # revert previous state
        #     command.undone.connect(
        #         lambda treeView=self.treeView, state=self.treeView.saveState(): 
        #             treeView.loadState(state)
        #     )
        pass
    