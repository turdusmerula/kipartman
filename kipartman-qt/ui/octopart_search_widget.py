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
        
        self.webEngineView.search()
       
