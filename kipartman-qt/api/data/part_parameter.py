from PyQt6.QtCore import QRunnable, QThreadPool
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QAbstractItemView, QHeaderView

from api.treeview import TreeModel, Node, TreeColumn, ValidationError, QTreeViewData
from api.command import CommandUpdateDatabaseField, CommandAddDatabaseObject, CommandDeleteDatabaseObjects, commands
from api.event import events
from api.unit import ureg
import database.data.part_parameter
from database.models import PartParameter, ParameterType, PartInstance
from enum import Enum

class CommandUpatePartParameter(CommandUpdateDatabaseField):
    def __init__(self, part_parameter, field, value, other_fields):
        super(CommandUpatePartParameter, self).__init__(object=part_parameter, field=field, value=value, other_fields=other_fields,
                                            description=f"change part parameter {field} to '{value}'")

class CommandAddPartParameter(CommandAddDatabaseObject):
    def __init__(self, part_parameter):
        super(CommandAddPartParameter, self).__init__(object=part_parameter,
                                            description=f"add new part parameter")

class CommandDeletePartParameters(CommandDeleteDatabaseObjects):
    def __init__(self, part_parameters):
        if isinstance(part_parameters, list) and len(part_parameters)>1:
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
        
class Column():
    PARAMETER = 0
    OPERATOR = 1
    VALUE = 2
    UNIT = 3
    DESCRIPTION = 4

class HeaderNode(Node):
    def __init__(self, title, parent=None):
        super(HeaderNode, self).__init__(parent)
        self.title = title

class PartParameterNode(Node):
    def __init__(self, part_parameter, parent=None):
        super(PartParameterNode, self).__init__(parent)
        self.part_parameter = part_parameter

    def GetValue(self, column):
        if column==Column.PARAMETER:
            if hasattr(self.part_parameter, 'parameter'):
                return self.part_parameter.parameter.name[0]
            return ""
        elif column==Column.OPERATOR:
            pass
        elif column==Column.VALUE:
            if hasattr(self.part_parameter, 'parameter'):
                if self.part_parameter.parameter.value_type==ParameterType.INTEGER:
                    field = 'int_value'
                elif self.part_parameter.parameter.value_type==ParameterType.FLOAT:
                    field = 'float_value'
                elif self.part_parameter.parameter.value_type==ParameterType.TEXT:
                    field = 'text_value'
                else:
                    return ""
                return getattr(self.part_parameter, field)
        elif column==Column.UNIT:
            if self.part_parameter.unit is not None:
                return self.part_parameter.unit
            elif hasattr(self.part_parameter, 'parameter'):
                return self.part_parameter.parameter.unit
            return None
        elif column==Column.DESCRIPTION:
            if hasattr(self.part_parameter, 'parameter'):
                return self.part_parameter.parameter.description
            return ""
        return None

    def SetValue(self, column, value):
        field = {
            Column.PARAMETER: "parameter",
            Column.UNIT: "unit",
        }

        if column!=Column.PARAMETER and hasattr(self.part_parameter, 'parameter')==False:
            # can not set any value until parameter is set
            return False
        
        if column!=Column.PARAMETER:
            if self.part_parameter.parameter.value_type==ParameterType.INTEGER:
                field[1] = 'int_value'
            elif self.part_parameter.parameter.value_type==ParameterType.FLOAT:
                field[1] = 'float_value'
            elif self.part_parameter.parameter.value_type==ParameterType.TEXT:
                field[1] = 'text_value'
            
        if self.part_parameter.id is None:
            # item has not yet be commited at this point and have no id
            # set edited field value
            setattr(self.part_parameter, field[column], value)
            if hasattr(self.part_parameter, 'parameter'):
                # save object in database
                commands.Do(CommandAddPartParameter, part_parameter=self.part_parameter)
            return True
        else:
            if column in field and getattr(self.part_parameter, field[column])!=value:
                if column==Column.PARAMETER:
                    # in case parameter is set we reinit all other fields to None
                    commands.Do(CommandUpatePartParameter, part_parameter=self.part_parameter, 
                        field=field[column], value=value,
                        other_fields={
                            'int_value': None,
                            'float_value': None,
                            'text_value': None,
                            'unit': None
                        }
                    )
                else:
                    commands.Do(CommandUpatePartParameter, part_parameter=self.part_parameter, field=field[column], value=value)
                return True
        return False

    def Validate(self, column, value):
        if column==Column.PARAMETER:
            if value is None:
                return ValidationError("No parameter set")
            # TODO check duplicates in database
        elif column==Column.UNIT:
            try:
                # check unit consistency
                ureg.parse_expression(value)
            except Exception as e:
                return ValidationError(f"{e}")
        return None

    def GetFlags(self, column, flags):
        if hasattr(self.part_parameter, 'parameter')==False and column>0:
            # when parameter is not set we prevent edition of other fields 
            return flags & ~Qt.ItemFlag.ItemIsEditable
        if column==3:
            return flags & ~Qt.ItemFlag.ItemIsEditable            
        return flags

class PartMetaParameterNode(Node):
    def __init__(self, part_parameter, parent=None):
        super(PartParameterNode, self).__init__(parent)
        self.part_parameter = part_parameter

class PartParameterModel(TreeModel):
    def __init__(self):
        super(PartParameterModel, self).__init__()

        self.InsertColumn(TreeColumn("Parameter"))
        self.InsertColumn(TreeColumn("Operator"))
        self.InsertColumn(TreeColumn("Value"))
        self.InsertColumn(TreeColumn("Unit"))
        self.InsertColumn(TreeColumn("Description"))

        self.loaded = False
        self.id_to_part_parameter_node = {}
        
        self.part = None
    
    def SetPart(self, part):
        self.part = part

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
        
        if self.part is not None:
            for part_parameter in self.part.parameters.all():
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

    def CreateEditNode(self, parent, data):
        return PartParameterNode(PartParameter(part=self.part))

    def Clear(self):
        self.id_to_part_parameter_node = {}
        self.loaded = False
        super(PartParameterModel, self).Clear()
        

class QPartParameterTreeView(QTreeViewData):
    def __init__(self, *args, **kwargs):
        super(QPartParameterTreeView, self).__init__(*args, **kwargs)
    
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        
        self.endInsertEditNode.connect(self.OnEndInsertEditNode)

        events.objectUpdated.connect(self.OnObjectUpdated)
        events.objectAdded.connect(self.OnObjectAdded)
        events.objectDeleted.connect(self.OnObjectDeleted)

    def setModel(self, model):
        super(QPartParameterTreeView, self).setModel(model)
        
        self.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)        

    def SetPart(self, part):
        if part is None or part.instance!=PartInstance.METAPART:
            self.setColumnHidden(Column.OPERATOR, True)
        else:
            self.setColumnHidden(Column.OPERATOR, False)
        self.model().SetPart(part)

    def OnObjectUpdated(self, object):
        if isinstance(object, PartParameter)==False:
            return 
        part_parameter = object
        if part_parameter.id in self.model().id_to_part_parameter_node:
            self.model().id_to_part_parameter_node[part_parameter.id].part_parameter.refresh_from_db()
            self.model().layoutChanged.emit()

    def OnObjectAdded(self, object):
        if isinstance(object, PartParameter)==False:
            return 
        part_parameter = object
        if part_parameter.id not in self.model().id_to_part_parameter_node:
            self.model().AddPartParameter(part_parameter)
            
    def OnObjectDeleted(self, object, id):
        if isinstance(object, PartParameter)==False:
            return 
        part_parameter = object
        if id in self.model().id_to_part_parameter_node:
            node = self.model().id_to_part_parameter_node[id]
            self.model().RemovePartParameterId(id)

    def OnEndInsertEditNode(self, node):
        part_parameter = node.part_parameter
        self.setCurrentIndex(self.model().index_from_part_parameter(part_parameter))
        
        # add code to select item on redo in this current view only
        commands.LastUndo.done.connect(
            lambda treeView=self, part_parameter=part_parameter: 
                self.setCurrentIndex(treeView.model().index_from_part_parameter(part_parameter))
        )
    
