from PyQt6 import Qt6
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QEvent, pyqtSignal, QUrl
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import QAbstractItemView, QFrame

from diskcache import Cache
import os
import json
import yaml

from api.data.octopart import OctopartModel, OctopartNode
from api.event import events
from api.filter import FilterSet, FilterGroup
from api.log import log
from api.ndict import ndict
from api.octopart.queries import OctopartPartQuery
from database.models import PartCategory
from helper.dialog import ShowErrorDialog
from ui.action_frame import QActionFrame

class QOctopartSearchWidget(QActionFrame):

    def __init__(self, *args, **kwargs):
        super(QOctopartSearchWidget, self).__init__(*args, **kwargs)
        uic.loadUi('ui/octopart_search_widget.ui', self)

        self.cache = Cache(directory=os.path.expanduser('~/.kipartman/cache/octopart'))
        # self.cache.delete("previous_search")
        # self.cache.delete(f"search.ATSAMD21G18A")
        
        self.model = OctopartModel()
        self.treeView.setModel(self.model)
        self.treeView.selectionModel().selectionChanged.connect(self.treeViewSelectionChanged)
        self.treeView.doubleClicked.connect(self.treeViewDoubleClicked)

        self.query = OctopartPartQuery()
        # self.query.ClearCache()

        self.comboBox.lineEdit().returnPressed.connect(self.search)
        self.comboBox.currentIndexChanged.connect(self.comboBoxCurrentIndexChanged)
        self.comboBox.currentTextChanged.connect(self.update_widgets)
        self.toolButtonSearch.clicked.connect(self.toolButtonSearchClicked)
        self.toolButtonClear.clicked.connect(self.toolButtonClearClicked)
        self.spinBoxLimit.setValue(self.query.limit)
        
        self._prevent_recurse = 0
        
        self.load_previous_search()
        self.update_widgets()
        
    def update_widgets(self):
        if self.comboBox.currentText()=="":
            self.toolButtonSearch.setEnabled(False)
        else:
            self.toolButtonSearch.setEnabled(True)
        
        if self.model.rowCount()>0:
            self.toolButtonClear.setEnabled(True)
        else:
            self.toolButtonClear.setEnabled(False)
            
    def treeViewSelectionChanged(self, selected, deselected):
        if len(self.treeView.selectionModel().selectedRows())>0:
            parts = []
            for index in self.treeView.selectionModel().selectedRows():
                node = self.treeView.model().node_from_index(index)
                parts.append(node.part)
            node = self.treeView.model().node_from_index(self.treeView.selectionModel().selectedRows()[0])
            self.currentResult.emit(parts)
        else:
            self.currentResult.emit(None)
    
    def treeViewDoubleClicked(self, event):
        if len(self.treeView.selectionModel().selectedRows())>0:
            parts = []
            for index in self.treeView.selectionModel().selectedRows():
                node = self.treeView.model().node_from_index(index)
                parts.append(node.part)
            self.validated.emit(node.part)
    #
    def toolButtonSearchClicked(self, action):
        self.search()
        self.update_widgets()

    def toolButtonClearClicked(self, action):
        self.model.Clear()
        self.cache.delete(f"search.{self.comboBox.currentText()}")
        self.update_widgets()

    def comboBoxCurrentIndexChanged(self, index):
        if self._prevent_recurse>0:
            return 
        self._prevent_recurse += 1
        
        text = self.comboBox.itemText(index)
        if text in self.previous_search:
            self.previous_search.remove(text)
            self.previous_search.insert(1, text)
        else:
            self.previous_search.insert(1, text)
        self.save_previous_search()
        self.load_previous_search()
        
        status = ""
        if text!="":
            search = self.cache.get(f"search.{text}")
            if search is not None:
                search = json.loads(search)
                self.model.SetResults(search["results"])
                status = f"Shown {len(search['results'])} results / {search['hits']}" 
        self.labelState.setText(status)

        self.update_widgets()
        self._prevent_recurse -= 1
    
    def search(self):
        try:
            print("search", self.comboBox.currentText())
            if self.comboBox.currentText()=="":
                return ""
            
            if self.comboBox.currentText() in self.previous_search:
                self.previous_search.remove(self.comboBox.currentText())
                self.previous_search.insert(1, self.comboBox.currentText())
            else:
                self.previous_search.insert(1, self.comboBox.currentText())
            self.save_previous_search()
            self.load_previous_search()
                
            search = self.cache.get(f"search.{self.comboBox.currentText()}")
            if search is None:
                search = {
                    "name": self.comboBox.currentText(),
                    "start": 0,
                    "limit": int(self.spinBoxLimit.value()),
                    "hits": None,
                    "results": []
                }
            else:
                search = json.loads(search)
                search["start"] += int(search["limit"])
                search["limit"] = int(self.spinBoxLimit.value())
            
            res = self.query.SearchMpn(self.comboBox.currentText(), start=search["start"], limit=search["limit"])
            if res is not None:
                res = ndict(res)
                self.model.SetResults(res.search_mpn.results)
                search["hits"] = int(res.search_mpn.hits)
                search["results"] += res.search_mpn.results
    
                status = f"Shown {len(search['results'])} results / {search['hits']}" 
                self.cache.set(f"search.{self.comboBox.currentText()}", json.dumps(search), expire=self.query.ttl)
            else:
                status = f"No item were found" 
            
            self.labelState.setText(status)
            # hits = 
            # loaded = 
            # state = f"start: {search['start']}, limit: {search['limit']}, loaded: {"
        except Exception as e:
            log.error(f"{e}")
            ShowErrorDialog("Search failed", f"{e}")

    def save_previous_search(self):
        self.cache.set("previous_search", json.dumps(self.previous_search))
    
    def load_previous_search(self):
        self._prevent_recurse += 1
        
        # previous search is a list of searched items
        previous_search = self.cache.get("previous_search")
        if previous_search is not None:
            self.previous_search = json.loads(previous_search)
        else:
            self.previous_search = ['']

        while len(self.previous_search)>20:
            self.previous_search.pop(20)


        text = self.comboBox.currentText()
        self.comboBox.clear()
        for search in self.previous_search:
            self.comboBox.addItem(search)
        self.comboBox.setCurrentText(text)
                
        self._prevent_recurse -= 1
