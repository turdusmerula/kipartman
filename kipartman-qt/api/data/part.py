from PyQt6.QtCore import Qt, QObject, pyqtSignal
from PyQt6.QtWidgets import QTreeView, QHeaderView

from api.filter import FilterSet
from api.treeview import TreeModel, Node, TreeColumn, QTreeViewData
from api.command import Command, CommandUpdateDatabaseField, commands, CommandAddDatabaseObject, CommandDeleteDatabaseObjects
from api.event import events
from api.log import log
from api.ndict import ndict
from api.octopart.queries import OctopartPartQuery
import database.data.part
from database.models import Part, PartInstance
from ui.metapart_load_widget import QMetapartLoadWidget
from PyQt6.QtGui import QColor

class CommandUpatePart(CommandUpdateDatabaseField):
    def __init__(self, part, field, value, other_fields):
        super(CommandUpatePart, self).__init__(object=part, field=field, value=value, other_fields=other_fields,
                                            description=f"change part {field} to '{value}'")

class CommandAddPart(CommandAddDatabaseObject):
    def __init__(self, part, fields):
        super(CommandAddPart, self).__init__(object=part, fields=fields,
                                            description=f"add new part")

class CommandDeleteParts(CommandDeleteDatabaseObjects):
    def __init__(self, parts):
        if isinstance(parts, list) and len(parts)>1:
            objects = parts
            description = f"delete {len(parts)} parts"
        elif isinstance(parts, list) and len(parts)==1:
            objects = parts
            description = f"delete part '{parts[0].name}'"
        else:
            objects = [parts]
            description = f"delete part '{parts.name}'"
        
        super(CommandDeleteParts, self).__init__(objects=objects,
                                            description=description)

class Column():
    ID = 0
    NAME = 1
    DESCRIPTION = 2
    
    _COUNT = 3
    
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


class PartNode(Node):
    def __init__(self, part, parent=None):
        super(PartNode, self).__init__(parent)
        self.part = part

    def GetValue(self, column):
        if column==Column.ID:
            return self.part.id
        elif column==Column.NAME:
            return self.part.name
        elif column==Column.DESCRIPTION:
            return self.part.description

    def GetFlags(self, column, flags):
        if column==Column.ID:
            return flags & ~Qt.ItemFlag.ItemIsEditable
        return flags

    def SetValue(self, column, value):
        field = {
            Column.NAME: "name",
            Column.DESCRIPTION: "description"
        }
        if column in field and getattr(self.part, field[column])!=value:
            commands.Do(CommandUpatePart, part=self.part, field=field[column], value=value, other_fields={})
            return True

        return False

    def HasChildren(self):
        return self.part.instance==PartInstance.METAPART

class OctopartNode(Node):
    def __init__(self, octopart, parent=None):
        super(OctopartNode, self).__init__(parent)
        self.part = octopart

    def GetValue(self, column):
        if column==Column.ID:
            return None
        elif column==Column.NAME:
            return self.part.mpn
        elif column==Column.DESCRIPTION:
            return self.part.short_description

    def GetFlags(self, column, flags):
        return flags & ~Qt.ItemFlag.ItemIsEditable

class LoadMoreNode(Node):
    def __init__(self, result, parent=None):
        super(LoadMoreNode, self).__init__(parent)
        self.result = result

    def GetValue(self, column):
        return None

    def GetFlags(self, column, flags):
        return flags & ~Qt.ItemFlag.ItemIsEditable

class ErrorNode(Node):
    def __init__(self, error, parent=None):
        super(ErrorNode, self).__init__(parent)
        self.error = error

    def GetValue(self, column):
        if column==Column.ID:
            return self.error
        return None
    
    def GetDecoration(self, column):
        return QColor(255, 0, 0)
    
    def GetFlags(self, column, flags):
        return flags & ~Qt.ItemFlag.ItemIsEditable

class PartCategoryNode(Node):
    def __init__(self, part, parent=None):
        super(PartCategoryNode, self).__init__(parent)
        self.category = category

class PartModel(TreeModel):
    def __init__(self):
        super(PartModel, self).__init__()
        
        self.InsertColumn(TreeColumn("ID"))
        self.InsertColumn(TreeColumn("Name"))
        self.InsertColumn(TreeColumn("Description"))

        self.filters = None

        self.id_to_part = {}
        self.loaded = {
            self.rootNode: False
        }
        self.octopart_loaded = {}
        
        self.metapart_request = None
        self.octopart_query = OctopartPartQuery()

    def SetFilters(self, filters: FilterSet):
        self.filters = filters 
    
    def CanFetchMore(self, parent):
        return not self.loaded[parent]

    def Fetch(self, parent):
        if parent is self.rootNode:
            self.FetchParts()
        elif parent.part.instance==PartInstance.METAPART:
            # set parent loaded now to avoid multiple call to Fetch
            self.loaded[parent] = True

            self.FetchMetapart(parent)
            self.FetchOctopart(parent)
            
    def FetchParts(self):
        if self.metapart_request is None:
            self.metapart_request = database.data.part.find(self.filters).iterator()
        
        nodes = []
        try:
            while(len(nodes)<10):
                part = next(self.metapart_request)
                node = PartNode(part)
                self.id_to_part[part.id] = node
                
                if part.instance==PartInstance.METAPART:
                    self.loaded[node] = False
                else:
                    self.loaded[node] = True

                nodes.append(node)
        except StopIteration:
            self.loaded[self.rootNode] = True
        self.InsertNodes(nodes)
    
    def FetchMetapart(self, metapart):
        # add database parts
        parts = database.data.part.find_metapart_childs(metapart.part)
        nodes = []
        for part in parts:
            node = self.FindMetapartPart(metapart, part)
            if node is None:
                node = PartNode(part)
                self.id_to_part[part.id] = node
                nodes.append(node)
            self.loaded[node] = True
        self.InsertNodes(nodes, parent=metapart)
    
    def FetchOctopart(self, metapart):
        if len(metapart.part.parameters.all())==0:
            return 

        to_remove = []
        for child in metapart.childs:
            if isinstance(child, ErrorNode) or isinstance(child, LoadMoreNode):
                to_remove.append(child)
        self.RemoveNodes(to_remove)
    
        # add octopart parts
        if metapart in self.octopart_loaded:
            query = self.octopart_loaded[metapart]
        else:
            query = {
                'start': 0,
                'limit': self.octopart_query.limit
            }
        
        error = None
        filters = {}
        for part_parameter in metapart.part.parameters.all():
            shortname = self.octopart_query.name_to_shortname(part_parameter.parameter.name)
            if shortname is None:
                error = f"parameter '{part_parameter.parameter.name}' not known for octopart"
                break
            filters[shortname] = part_parameter.decoded_value

        if error is not None:
            node = ErrorNode(error)
            self.InsertNode(node, parent=metapart)
            return
        
        res = self.octopart_query.Search(start=query['start'], limit=query['limit'], filters=filters)
        if res is not None:
            res = ndict(res)
            for part in res.search.results:
                node = OctopartNode(part.part)
                print("###", part)
                self.InsertNode(node, parent=metapart)
                
            query['start'] += len(res.search.results)
            self.octopart_loaded[metapart] = query

        # add loading node
        node = LoadMoreNode(res)
        self.InsertNode(node, parent=metapart)
        #     search["results"] += res.search_mpn.results
        #
        #     status = f"Shown {len(search['results'])} results / {search['hits']}" 
        #     self.cache.set(f"search.{self.comboBox.currentText()}", json.dumps(search), expire=self.query.ttl)
        # else:
        #     status = f"No item were found" 
        #
        # self.labelState.setText(status)
        
    
    def FindMetapartPart(self, metapart, part):
        for child in metapart.childs:
            if isinstance(child, PartNode) and child.part.id==part.id:
                return child
            elif isinstance(child, OctopartNode) and child.part.id==part.id:
                return child
        return None
    
    def Clear(self):
        self.id_to_part.clear()
        self.loaded.clear()
        self.metapart_request = None
        
        super(PartModel, self).Clear()

        self.loaded[self.rootNode] = False

    def Update(self):
        self.Clear()

    def CreateEditNode(self, parent, category, instance):
        return PartNode(Part(category=category, instance=instance))

class QPartTreeView(QTreeViewData):
    def __init__(self, *args, **kwargs):
        super(QPartTreeView, self).__init__(*args, **kwargs)

    def setModel(self, model):
        super(QPartTreeView, self).setModel(model)
        
        self.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)        

    def OnObjectUpdated(self, object):
        if isinstance(object, Part)==False:
            return 
        part = object
        if part.id in self.model().id_to_part_node:
            self.model().id_to_part_node[part.id].part.refresh_from_db()
            self.model().layoutChanged.emit()

    def OnObjectAdded(self, object):
        if isinstance(object, Part)==False:
            return 
        part = object
        if part.id not in self.model().id_to_part_node:
            self.model().AddPart(part)
            
    def OnObjectDeleted(self, object, id):
        if isinstance(object, Part)==False:
            return 
        part = object
        if id in self.model().id_to_part_node:
            node = self.model().id_to_part_node[id]
            self.model().RemovePartId(id)

    def OnEndInsertEditNode(self, node):
        part = node.part
        self.setCurrentIndex(self.model().index_from_part(part))
        
        # add code to select item on redo in this current view only
        commands.LastUndo.done.connect(
            lambda treeView=self, part=part: 
                self.setCurrentIndex(treeView.model().index_from_part(part))
        )
    

    def rowsInserted(self, parent, first, last):
        parent_node = self.model().node_from_index(parent)
        for row in range(first, last+1):
            index = self.model().index(row, Column.ID, parent=parent)
            node = self.model().node_from_index(index)
            if isinstance(node, LoadMoreNode):
                widget = QMetapartLoadWidget(self)
                widget.clicked.connect(lambda: self.loadMore(parent_node))
                self.setIndexWidget(index, widget)
                self.setFirstColumnSpanned(row, parent, True)
    
    def loadMore(self, parent):
        log.debug("loadMore")
        self.model().FetchOctopart(parent)
        
    def getItemWidget(self, index):
        node = self.model().node_from_index(index)
        if isinstance(node, LoadMoreNode):
            return QMetapartLoadWidget(self)
