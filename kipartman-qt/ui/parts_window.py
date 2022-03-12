from PyQt6 import Qt6, QtWidgets, uic
from PyQt6.QtCore import pyqtSignal, QEvent, QSettings
from PyQt6.QtGui import QWindowStateChangeEvent
from PyQt6.QtWidgets import QMdiSubWindow, QTextEdit

from api.data.part_category import PartCategoryModel
from api.filter import FilterSet, FilterGroup
from database.data.part import FilterPartCategories
from ui.child_window import QChildWindow
from ui.filter_list_widget import QFilterListWidget
from ui.part_category_list_widget import QPartCategoryListWidget
from ui.part_parameter_list_widget import QPartParameterListWidget


class FilterGroupPartCategory(FilterGroup):
    def __init__(self):
        super(FilterGroupPartCategory, self).__init__("part category", "Part category filters")
    
    def Append(self, filter):
        """ when we add a part category filter it will replace the previous one """
        self.filters.clear()
        self.filters.append(filter)
        self.filterChanged.emit()


class PartsWindow(QChildWindow):
    
    def __init__(self, parent):
        super(PartsWindow, self).__init__(parent)
        uic.loadUi('ui/parts_window.ui', self)

        self.filterList = QFilterListWidget(self)
        self.partCategoryList = QPartCategoryListWidget(self)
        self.partParameterList = QPartParameterListWidget(self)
        
        self.partCategoryList.selectionChanged.connect(self.partCategorySelectionChanged)

        self.filters = self.filterList.filters
        self.category_filter_group = FilterGroupPartCategory()
        self.category_filter_group.filterChanged.connect(self.filterChanged)
        self.filters.Append(self.category_filter_group)
        
        self.partList.SetFilters(self.filters)
        self.partList.selectionChanged.connect(self.partListSelectionChanged)

        self.parts = []
        self.part_categories = []
        
        self.update_menus()
        self.activated()

    def update(self):
        pass
        
    def update_menus(self):
        from ui.main_window import main_window

        if len(self.parts)>0:
            main_window.actionPartDelete.setEnabled(True)
        else:
            main_window.actionPartDelete.setEnabled(False)

        if len(self.part_categories)>1:
            main_window.actionPartAddPart.setEnabled(False)
            main_window.actionPartAddMetapart.setEnabled(False)
            main_window.actionPartImportOctopart.setEnabled(False)
        else:
            main_window.actionPartAddPart.setEnabled(True)
            main_window.actionPartAddMetapart.setEnabled(True)
            main_window.actionPartImportOctopart.setEnabled(True)

    def activated(self):
        print("PartsWindow.activated")
        from ui.main_window import main_window

        main_window.ChangeDockPartCategoryWidget(self.partCategoryList)
        main_window.ChangeDockFilterWidget(self.filterList)
        main_window.ChangeDockPartParameterWidget(self.partParameterList)
        # main_window.ChangeDockPartStoragesWidget(self.partStorageList)
        main_window.dockParameterWidget.setVisible(True)
        main_window.dockStorageWidget.setVisible(True)
    
        #  restore geometry
        main_window.loadWindowSettings("parts")

        self.update_menus()

    def deactivated(self):
        print("PartsWindow.deactivated")
        from ui.main_window import main_window
        
        main_window.saveWindowSettings("parts")

        main_window.ChangeDockPartCategoryWidget(None)
        main_window.ChangeDockFilterWidget(None)
        main_window.ChangeDockPartParameterWidget(None)
        # main_window.ChangeDockPartStoragesWidget(self.partStorageList)
        main_window.dockParameterWidget.setVisible(False)
        main_window.dockStorageWidget.setVisible(False)

        main_window.actionPartAddPart.setEnabled(False)
        main_window.actionPartAddMetapart.setEnabled(False)
        main_window.actionPartImportOctopart.setEnabled(False)
        main_window.actionPartDelete.setEnabled(False)

    def partCategorySelectionChanged(self, part_categories):
        from ui.main_window import main_window
        
        self.part_categories = part_categories
        
        if len(part_categories)>0:
            self.category_filter_group.Append(FilterPartCategories(part_categories, main_window.actionSelectChildMode.isChecked()))
            self.partList.SetOwnerCategory(part_categories[0])
        else:
            self.category_filter_group.Clear()
            self.partList.SetOwnerCategory(None)
        
        self.update_menus()
            
    def filterChanged(self):
        if self.category_filter_group.IsEmpty():
            self.partCategoryList.UnselectAll()
        
        self.partList.update()

    def partListSelectionChanged(self, parts):
        self.parts = parts

        if len(parts)==1:
            self.partParameterList.SetPart(parts[0])
        else:
            self.partParameterList.SetPart(None)
            # node = self.treeView.model().node_from_index(self.treeView.selectionModel().selectedRows()[0])
            # self.validated.emit(node.parameter)
                    