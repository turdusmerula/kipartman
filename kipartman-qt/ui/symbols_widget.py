from PyQt6 import Qt6
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMdiSubWindow, QTextEdit


# from ui.part_category_list_widget import PartCategoryListWidget
# from ui.part_list_widget import PartListWidget
class SymbolsWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        super(SymbolsWidget, self).__init__(parent)
        uic.loadUi('ui/symbols_widget.ui', self)

        # self.part_category_list = SymbolCategoryListWidget(self)
        # self.splitter.addWidget(self.part_category_list)
        #
        # self.part_list = SymbolListWidget(self)
        # self.splitter.addWidget(self.part_list)
        
        self.update_menus()

    def update(self):
        # self.part_category_list.update()
        # self.part_list.update()
        super(SymbolsWidget, self).update()
    
    def update_menus(self):
        # self.part_category_list.update_menus()
        # self.part_list.update_menus()
        pass
        