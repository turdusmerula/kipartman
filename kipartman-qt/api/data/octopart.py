from PyQt6.QtCore import Qt, QObject, pyqtSignal
from PyQt6.QtWidgets import QTreeView, QHeaderView

from api.treeview import TreeModel, Node, TreeColumn, QTreeViewData
from api.event import events

class Column():
    MPN = 0
    NAME = 1
    ID = 2
    DESCRIPTION = 3
    SELLERS = 4
    
    _COUNT = 5
    
    def __init__(self):
        self.pos_to_name = {}
        self.name_to_pos = {}

    def AddColumn(self, name):
        pos = Column._COUNT+len(self.pos_to_name)
        self.pos_to_name[pos] = name
        self.name_to_pos[name] = pos
    
    def PosFromName(self, name):
        if name in self.name_to_pos:
            return self.name_to_pos[name]
        return None
        
    def NameFromPos(self, pos):
        if pos in self.pos_to_name:
            return self.pos_to_name[pos]
        return None

class OctopartNode(Node):
    def __init__(self, part, columns):
        super(OctopartNode, self).__init__()
        self.part = part
        self.columns = columns
        
    def GetValue(self, column):
        if column==Column.MPN:
            return self.part.get("mpn", "")
        elif column==Column.NAME:
            return self.part.get("name", "").strip()
        elif column==Column.ID:
            return self.part.get("id", "")
        elif column==Column.DESCRIPTION:
            return self.part.get("short_description", "").strip()
        elif column==Column.SELLERS:
            return len(self.part.get("sellers", ""))
        elif self.columns.NameFromPos(column) is not None:
            name = self.columns.NameFromPos(column)
            for spec in self.part.get("specs", ""):
                if spec["attribute"]["name"]==name:
                    return spec.get("display_value", "")
        return None

    def GetFlags(self, column, flags):
        return flags & ~Qt.ItemFlag.ItemIsEditable

class OctopartModel(TreeModel):
    def __init__(self):
        super(OctopartModel, self).__init__()
        
        self.InsertColumn(TreeColumn("MPN"))
        self.InsertColumn(TreeColumn("Name"))
        self.InsertColumn(TreeColumn("ID"))
        self.InsertColumn(TreeColumn("Description"))
        self.InsertColumn(TreeColumn("Sellers"))

        self.extra_columns = Column()
        self.loaded = False
        self.results = []
    
    def SetResults(self, results):
        for result in results:
            self.results.append(result)
        self.Update()

    def CanFetchMore(self, parent):
        return self.loaded==False

    def Fetch(self, parent):
        # with open("/home/seb/git/kipartman-v2/kipartman-qt/api/octopart/search-result.yaml", 'r') as stream:
        #     request = munchify(yaml.load(stream, Loader=yaml. FullLoader), DefaultMunch)
        
        # when we add columns a fetch is made before load finishes 
        self.loaded = True

        for part in self.results:
            node = self.FindPart(part["part"])
            if node is None:
                node = OctopartNode(part["part"], self.extra_columns)
                self.InsertNode(node)

            for spec in part["part"]["specs"]:
                if self.extra_columns.PosFromName(spec["attribute"]["name"]) is None:
                    self.extra_columns.AddColumn(spec["attribute"]["name"])
                    self.InsertColumn(TreeColumn(spec["attribute"]["name"]))
    
    
    def FindPart(self, part):
        for node in self.node_to_id:
            if isinstance(node, OctopartNode) and node.part["mpn"]==part["mpn"]:
                return node
        return None

    def Clear(self):
        super().Clear()
        self.results = []
        self.loaded = False

    def Update(self):
        self.loaded = False
        super().Update()

class QOctopartTreeView(QTreeViewData):
    def __init__(self, *args, **kwargs):
        super(QOctopartTreeView, self).__init__(*args, **kwargs)

    def setModel(self, model):
        super(QOctopartTreeView, self).setModel(model)
        
        self.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)        