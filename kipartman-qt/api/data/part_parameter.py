from PyQt6.QtCore import QRunnable, QThreadPool
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtCore import Qt

from api.treeview import TreeModel, Node, Column, ValidationError, QTreeViewData
from api.command import CommandUpdateDatabaseField, CommandAddDatabaseObject, CommandDeleteDatabaseObjects, commands
from api.event import events
from api.unit import ureg
import database.data.part_parameter
from database.models import PartParameter

class CommandUpatePartParameter(CommandUpdateDatabaseField):
    def __init__(self, part_parameter, field, value):
        super(CommandUpatePartParameter, self).__init__(object=part_parameter, field=field, value=value,
                                            description=f"change part parameter {field} to '{value}'")

class CommandAddPartParameter(CommandAddDatabaseObject):
    def __init__(self, part_parameter):
        super(CommandAddPartParameter, self).__init__(object=part_parameter,
                                            description=f"add new part parameter")

class CommandDeletePartParameters(CommandDeleteDatabaseObjects):
    def __init__(self, part_parameters):
        if isinstance(part_parameters, list) and len(parameters)>1:
            objects = part_parameters
            description = f"delete {len(part_parameters)} part parameters"
        elif isinstance(part_parameters, list) and len(part_parameters)==1:
            objects = part_parameters
            description = f"delete part parameter '{part_parameters[0].name}'"
        else:
            objects = [part_parameters]
            description = f"delete part parameter '{part_parameters.name}'"
        
        super(CommandDeletePartParameters, self).__init__(objects=objects,
                                            description=description)



class HeaderNode(Node):
    def __init__(self, title, parent=None):
        super(HeaderNode, self).__init__(parent)
        self.title = title

class PartParameterNode(Node):
    def __init__(self, part_parameter, parent=None):
        super(PartParameterNode, self).__init__(parent)
        self.part_parameter = part_parameter

    def GetValue(self, column):
        if column==0:
            if hasattr(self.part_parameter, 'parameter'):
                return self.part_parameter.parameter.name[0]
            return ""
        return None

    def SetValue(self, column, value):
        field = {
            0: "name",
            # 1: "unit",
            # 2: "value_type",
            # 3: "description"
        }
        if self.parameter.id is None:
            # item has not yet be commited at this point and have no id
            # set edited field value
            setattr(self.part_parameter, field[column], value)
            if self.parameter.name!="":
                # save object in database
                commands.Do(CommandAddPartParameter, part_parameter=self.part_parameter)
            return True
        else:
            print(getattr(self.part_parameter, field[column]), value, getattr(self.part_parameter, field[column])!=value)
            if column in field and getattr(self.part_parameter, field[column])!=value:
                commands.Do(CommandUpatePartParameter, part_parameter=self.part_parameter, field=field[column], value=value)
                return True
        return False

    def Validate(self, column, value):
        if column==0:
            if len(value)==0:
                return ValidationError("Name missing")
            # TODO check duplicates in database
        elif column==1:
            try:
                ureg.parse_expression(value)
            except Exception as e:
                return ValidationError(f"{e}")
        return None

class PartMetaParameterNode(Node):
    def __init__(self, part_parameter, parent=None):
        super(PartParameterNode, self).__init__(parent)
        self.part_parameter = part_parameter

class PartParameterModel(TreeModel):
    def __init__(self):
        super(PartParameterModel, self).__init__()
        
        self.InsertColumn(Column("Parameter"))
        self.InsertColumn(Column("Value"))
        self.InsertColumn(Column("Unit"))
        self.InsertColumn(Column("Description"))

        self.loaded = False
        self.id_to_part_parameter_node = {}
        

    def index_from_part_parameter(self, part_parameter):
        if part_parameter.id not in self.id_to_part_parameter_node:
            return QModelIndex()
        node = self.id_to_part_parameter_node[part_parameter.id]
        return self.index_from_node(node)

    def part_parameter_node_from_id(self, id):
        return self.id_to_part_parameter_node[id]

    def CanFetchMore(self, parent):
        return not self.loaded

    def Fetch(self, parent):
        # create a state
        nodes = self.node_to_id.copy()
        del nodes[self.rootNode] # remove root node
        
        for part_parameter in database.data.part_parameter.find():
            part_parameter_node = self.FindPartParameter(part_parameter)
            if part_parameter_node is None:
                part_parameter_node = self.AddPartParameter(part_parameter)
            else:
                del nodes[part_parameter_node]
        
        # remove remaining nodes
        self.RemoveNodes(list(nodes.keys()))
        self.loaded = True

    def FindPartParameter(self, part_parameter):
        for node in self.node_to_id:
            if isinstance(node, PartParameterNode) and node.part_parameter is part_parameter:
                return node
        return None

    def AddPartParameter(self, part_parameter, pos=None):
        node = PartParameterNode(part_parameter)
        self.loaded = True
        self.id_to_part_parameter_node[part_parameter.id] = node

        self.InsertNode(node, pos=pos)

    def RemovePartParameterId(self, id):
        node = self.part_parameter_node_from_id(id)
        self.loaded = False
        del self.id_to_part_parameter_node[id]
        self.RemoveNode(node)

    def RemovePartParameter(self, part_parameter):
        node = self.part_parameter_node_from_id(part_parameter.id)
        self.loaded = False
        del self.id_to_part_parameter_node[part_parameter.id]
        self.RemoveNode(node)

    def CreateEditNode(self, parent):
        return PartParameterNode(PartParameter())


class QPartParameterTreeView(QTreeViewData):
    def __init__(self, *args, **kwargs):
        super(QPartParameterTreeView, self).__init__(*args, **kwargs)
