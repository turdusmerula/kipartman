from PyQt6 import Qt6
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QEvent, pyqtSignal, QUrl
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import QAbstractItemView, QFrame

from api.data.octopart import OctopartModel, OctopartNode
from api.event import events
from api.filter import FilterSet, FilterGroup
from database.models import PartCategory
from helper.dialog import ShowErrorDialog
from ui.action_frame import QActionFrame


class QOctopartSearchWidget(QActionFrame):

    def __init__(self, *args, **kwargs):
        super(QOctopartSearchWidget, self).__init__(*args, **kwargs)
        uic.loadUi('ui/octopart_search_widget.ui', self)

        self.model = OctopartModel()
        self.treeView.setModel(self.model)
        self.treeView.selectionModel().selectionChanged.connect(self.treeViewSelectionChanged)
        self.treeView.doubleClicked.connect(self.treeViewDoubleClicked)

        self.toolButtonSearch.clicked.connect(self.toolButtonSearchClicked)
    #
    def treeViewSelectionChanged(self, selected, deselected):
        if len(self.treeView.selectionModel().selectedRows())>0:
            node = self.treeView.model().node_from_index(self.treeView.selectionModel().selectedRows()[0])
            self.currentResult.emit(node.part)
        else:
            self.currentResult.emit(None)
    
    def treeViewDoubleClicked(self, event):
        if len(self.treeView.selectionModel().selectedRows())>0:
            node = self.treeView.model().node_from_index(self.treeView.selectionModel().selectedRows()[0])
            self.validated.emit(node.part)
    #
    def toolButtonSearchClicked(self, action):
        print("search")
        
        self.webEngineView.load(QUrl("https://octopart.com/search?currency=EUR&q=resistor&specs=1&case_package=0603&tolerance=%28__0.1%29&sort=median_price_1000&sort-dir=asc&distributor_id=2401&distributor_id=459&distributor_id=819&resistance=%28100__100%29"))
        
