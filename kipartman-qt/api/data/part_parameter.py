from PyQt6.QtCore import QRunnable, QThreadPool
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtCore import Qt

from api.treeview import TreeModel, Node, Column, QTreeViewData
from api.command import Command, CommandUpdateDatabaseField, commands
from api.event import events
import database.data.part
from database.models import Part


class HeaderNode(Node):
    def __init__(self, title, parent=None):
        super(HeaderNode, self).__init__(parent)
        self.title = title

class PartParameterNode(Node):
    def __init__(self, part_parameter, parent=None):
        super(PartParameterNode, self).__init__(parent)
        self.part_parameter = part_parameter

class PartMetaParameterNode(Node):
    def __init__(self, part_parameter, parent=None):
        super(PartParameterNode, self).__init__(parent)
        self.part_parameter = part_parameter

class PartParameterModel(TreeModel):
    def __init__(self):
        super(PartParameterModel, self).__init__()
        
        self.InsertColumn(Column("Parameter"))
        self.InsertColumn(Column("Value"))
        self.InsertColumn(Column("Description"))

        self.id_to_part_parameter = {}

        self.request = None
        
    def Fetch(self, parent):
        pass

    def HasChildren(self, parent):
        if isinstance(parent, HeaderNode):
            return True
        return False

    # def GetValue(self, node, column):
    #     if column==0:
    #         return node.part.id
    #     elif column==1:
    #         return node.part.name
    #     elif column==2:
    #         return node.part.description
    #
    # def GetFlags(self, node, column, flags):
    #     if column==0:
    #         return flags & ~Qt.ItemFlag.ItemIsEditable
    #     return flags
    #
    # def SetValue(self, node, column, value):
    #     field = {
    #         1: "name",
    #         2: "description"
    #     }
    #     if column in field and getattr(node.part, field[column])!=value:
    #         commands.Do(CommandUpatePart, part=node.part, field=field[column], value=value)
    #         return True
    #
    #     return False


class QPartParameterTreeView(QTreeViewData):
    def __init__(self, *args, **kwargs):
        super(QPartParameterTreeView, self).__init__(*args, **kwargs)
