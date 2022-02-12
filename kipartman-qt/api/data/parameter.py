from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtCore import QModelIndex
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTreeView, QHeaderView, QAbstractItemView

from api.treeview import TreeModel, Node, TreeColumn, ValidationError, QTreeViewData
from api.command import CommandUpdateDatabaseField, CommandAddDatabaseObject, CommandDeleteDatabaseObjects, commands
from api.event import events
from api.unit import ureg
import database.data.parameter
from database.models import Parameter, ParameterType
from enum import Enum

class CommandUpateParameter(CommandUpdateDatabaseField):
    def __init__(self, parameter, field, value, other_fields):
        super(CommandUpateParameter, self).__init__(object=parameter, field=field, value=value, other_fields=other_fields,
                                            description=f"change parameter {field} to '{value}'")

class CommandAddParameter(CommandAddDatabaseObject):
    def __init__(self, parameter):
        super(CommandAddParameter, self).__init__(object=parameter,
                                            description=f"add new parameter")

class CommandDeleteParameters(CommandDeleteDatabaseObjects):
    def __init__(self, parameters):
        if isinstance(parameters, list) and len(parameters)>1:
            objects = parameters
            description = f"delete {len(parameters)} parameters"
        elif isinstance(parameters, list) and len(parameters)==1:
            objects = parameters
            description = f"delete parameter '{parameters[0].name}'"
        else:
            objects = [parameters]
            description = f"delete parameter '{parameters.name}'"
        
        super(CommandDeleteParameters, self).__init__(objects=objects,
                                            description=description)

class ParameterColumn():
    SHOW = 0
    NAME = 1
    UNIT = 2
    VALUE_TYPE = 3
    DESCRIPTION = 4

    
class ParameterNode(Node):
    def __init__(self, parameter):
        super(ParameterNode, self).__init__()
        self.parameter = parameter

    def GetValue(self, column):
        if column==ParameterColumn.NAME:
            return self.parameter.name
        elif column==ParameterColumn.UNIT:
            return self.parameter.unit
        elif column==ParameterColumn.VALUE_TYPE:
            return self.parameter.value_type
        elif column==ParameterColumn.NAME:
            return self.parameter.name
        elif column==ParameterColumn.DESCRIPTION:
            return self.parameter.description
        return None

    def GetEditValue(self, column):
        return self.GetValue(column)

    def GetFlags(self, column, flags):
        if column==ParameterColumn.SHOW:
            return ( flags | Qt.ItemFlag.ItemIsUserCheckable ) & ~Qt.ItemFlag.ItemIsEditable
        elif column==ParameterColumn.UNIT:
            if self.parameter.value_type not in [ParameterType.INTEGER, ParameterType.FLOAT]:
                return flags & ~Qt.ItemFlag.ItemIsEditable

        return flags

    def GetCheckState(self, column):
        if column==ParameterColumn.SHOW:
            if self.parameter.show:
                return Qt.CheckState.Checked
            else:
                return Qt.CheckState.Unchecked
        return None

    def SetValue(self, column, value):
        field = {
            ParameterColumn.SHOW: "show",
            ParameterColumn.NAME: "name",
            ParameterColumn.UNIT: "unit",
            ParameterColumn.VALUE_TYPE: "value_type",
            ParameterColumn.DESCRIPTION: "description"
        }
        
        other_fields = {}
        
        if column==ParameterColumn.UNIT:
            if value!="" and value is not None:
                unit = ureg.Quantity(value)
                if unit.dimensionless:
                    value = None
                else:
                    value = unit.u
        elif column==ParameterColumn.VALUE_TYPE:
            if value not in [ParameterType.INTEGER, ParameterType.FLOAT]:
                other_fields['unit'] = None
        
        if self.parameter.id is None:
            # item has not yet be commited at this point and have no id
            # set edited field value
            setattr(self.parameter, field[column], value)
            if self.parameter.name!="":
                # save object in database
                commands.Do(CommandAddParameter, parameter=self.parameter)
            return True
        else:
            if column in field and getattr(self.parameter, field[column])!=value:
                commands.Do(CommandUpateParameter, parameter=self.parameter, field=field[column], value=value, other_fields=other_fields)
                return True
        return False

    def SetCheckState(self, column, value):
        if column==ParameterColumn.SHOW:
            if Qt.CheckState(value)==Qt.CheckState.Checked:
                show = True
            else:
                show = False
            if show!=self.parameter.show:
                commands.Do(CommandUpateParameter, parameter=self.parameter, field='show', value=show, other_fields={})
                return True                
        return False

    def Validate(self, column, value):
        if column==ParameterColumn.NAME:
            if value!=self.parameter.name and len(database.models.Parameter.objects.filter(name=value).all())>0:
                return ValidationError(f"Parameter '{value}' already exists")
        elif column==ParameterColumn.UNIT:
            try:
                ureg.parse_expression(value)
            except Exception as e:
                return ValidationError(f"{e}")
        return None

class ParameterModel(TreeModel):
    def __init__(self):
        super(ParameterModel, self).__init__()

        self.InsertColumn(TreeColumn("Show"))
        self.InsertColumn(TreeColumn("Name"))
        self.InsertColumn(TreeColumn("Unit"))
        self.InsertColumn(TreeColumn("Value type"))
        # TODO implement list and boolean
        # TODO implement default value
        # self.InsertColumn(TreeColumn("Default"))
        self.InsertColumn(TreeColumn("Description"))

        self.loaded = False
        self.id_to_parameter_node = {}

    def index_from_parameter(self, parameter):
        if parameter.id not in self.id_to_parameter_node:
            return QModelIndex()
        node = self.id_to_parameter_node[parameter.id]
        return self.index_from_node(node)

    def parameter_node_from_id(self, id):
        return self.id_to_parameter_node[id]

    def CanFetchMore(self, parent):
        return not self.loaded

    def Fetch(self, parent):
        # create a state
        nodes = self.node_to_id.copy()
        del nodes[self.rootNode] # remove root node
        
        for parameter in database.data.parameter.find():
            parameter_node = self.FindParameter(parameter)
            if parameter_node is None:
                parameter_node = self.AddParameter(parameter)
            else:
                del nodes[parameter_node]
        
        # remove remaining nodes
        self.RemoveNodes(list(nodes.keys()))
        self.loaded = True

    def FindParameter(self, parameter):
        for node in self.node_to_id:
            if isinstance(node, ParameterNode) and node.parameter is parameter:
                return node
        return None

    def AddParameter(self, parameter, pos=None):
        node = ParameterNode(parameter)
        self.id_to_parameter_node[parameter.id] = node

        self.InsertNode(node, pos=pos)

    def RemoveParameterId(self, id):
        node = self.parameter_node_from_id(id)
        del self.id_to_parameter_node[id]
        self.RemoveNode(node)

    def RemoveParameter(self, parameter):
        node = self.parameter_node_from_id(parameter.id)
        self.loaded = False
        del self.id_to_parameter_node[parameter.id]
        self.RemoveNode(node)

    def CreateEditNode(self, parent):
        return ParameterNode(Parameter(value_type='float'))

class QParameterTreeView(QTreeViewData):
    def __init__(self, *args, **kwargs):
        super(QParameterTreeView, self).__init__(*args, **kwargs)
    
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        
        self.endInsertEditNode.connect(self.OnEndInsertEditNode)

        events.objectUpdated.connect(self.OnObjectUpdated)
        events.objectAdded.connect(self.OnObjectAdded)
        events.objectDeleted.connect(self.OnObjectDeleted)

    def setModel(self, model):
        super(QParameterTreeView, self).setModel(model)
        
        self.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)        

    def OnObjectUpdated(self, object):
        if isinstance(object, Parameter)==False:
            return 
        parameter = object
        if parameter.id in self.model().id_to_parameter_node:
            self.model().id_to_parameter_node[parameter.id].parameter.refresh_from_db()
            self.model().layoutChanged.emit()

    def OnObjectAdded(self, object):
        if isinstance(object, Parameter)==False:
            return 
        parameter = object
        if parameter.id not in self.model().id_to_parameter_node:
            self.model().AddParameter(parameter)
            
    def OnObjectDeleted(self, object, id):
        if isinstance(object, Parameter)==False:
            return 
        parameter = object
        if id in self.model().id_to_parameter_node:
            node = self.model().id_to_parameter_node[id]
            self.model().RemoveParameterId(id)

    def OnEndInsertEditNode(self, node):
        parameter = node.parameter
        self.setCurrentIndex(self.model().index_from_parameter(parameter))
        
        # add code to select item on redo in this current view only
        commands.LastUndo.done.connect(
            lambda treeView=self, parameter=parameter: 
                self.setCurrentIndex(treeView.model().index_from_parameter(parameter))
        )
    
