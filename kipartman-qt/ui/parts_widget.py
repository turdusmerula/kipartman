from PyQt6 import Qt6
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMdiSubWindow, QTextEdit

from ui.part_category_list_widget import PartCategoryListWidget
from ui.part_list_widget import PartListWidget

class PartsWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        super(PartsWidget, self).__init__(parent)
        uic.loadUi('ui/parts_widget.ui', self)

        self.part_category_list = PartCategoryListWidget(self)
        self.splitter.addWidget(self.part_category_list)

        self.part_list = PartListWidget(self)
        self.splitter.addWidget(self.part_list)

    def update(self):
        self.part_category_list.update()
        self.part_list.update()

    # def update(self):
    #     self.model.Update()
