from PyQt6 import Qt6, QtWidgets, uic
from PyQt6.QtGui import QWindowStateChangeEvent
from PyQt6.QtCore import pyqtSignal, QEvent
from PyQt6.QtWidgets import QMdiSubWindow, QTextEdit

from api.data.part_category import PartCategoryModel
from api.filter import FilterSet, FilterGroup
from database.data.part import FilterPartCategories
from ui.child_window import QChildWindow
from ui.part_category_list_widget import QPartCategoryListWidget
from ui.filter_list_widget import QFilterListWidget

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

        self.filterList = QFilterListWidget()
        self.partCategoryList = QPartCategoryListWidget()
        # self.part_parameter_list = 
        
        self.partCategoryList.selectionChanged.connect(self.OnPartCategorySelectionChanged)

        self.filters = self.filterList.filters
        self.category_filter_group = FilterGroupPartCategory()
        self.category_filter_group.filterChanged.connect(self.OnFilterChanged)
        self.filters.Append(self.category_filter_group)
        
        self.partList.SetFilters(self.filters)
        
        self.update_menus()
        self.activated()

    def update(self):
        # self.partCategoryListWidget.update()
        # self.partListWidget.update()
        # super(PartsWindow, self).update()
        pass
        
    def update_menus(self):
        # self.partCategoryListWidget.update_menus()
        # self.partListWidget.update_menus()
        pass

    def activated(self):
        from ui.main_window import main_window
        if main_window is None:
            return
        
        main_window.ChangeDockPartCategoryWidget(self.partCategoryList)
        main_window.ChangeDockFilterWidget(self.filterList)
    
    def deactivated(self):
        from ui.main_window import main_window
        if main_window is None:
            return
        
        main_window.ChangeDockPartCategoryWidget(None)
        main_window.ChangeDockFilterWidget(None)

    def OnPartCategorySelectionChanged(self, part_categories):
        from ui.main_window import main_window
        if main_window is None:
            return

        if len(part_categories)>0:
            self.category_filter_group.Append(FilterPartCategories(part_categories, main_window.actionSelectChildMode.isChecked()))
        else:
            self.category_filter_group.Clear()

    def OnFilterChanged(self):
        if self.category_filter_group.IsEmpty():
            self.partCategoryList.UnselectAll()
        
        self.partList.update()
