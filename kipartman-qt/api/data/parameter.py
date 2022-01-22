from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtCore import QModelIndex
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTreeView, QHeaderView, QAbstractItemView

from api.treeview import TreeModel, Node, Column, ValidationError, QTreeViewData
from api.command import CommandUpdateDatabaseField, CommandAddDatabaseObject, CommandDeleteDatabaseObjects, commands
from api.event import events
from api.unit import ureg
import database.data.parameter
from database.models import Parameter

class CommandUpateParameter(CommandUpdateDatabaseField):
    def __init__(self, parameter, field, value):
        super(CommandUpateParameter, self).__init__(object=parameter, field=field, value=value,
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

class ParameterNode(Node):
    def __init__(self, parameter):
        super(ParameterNode, self).__init__()
        self.parameter = parameter

    def GetValue(self, column):
        if column==0:
            if self.parameter.name is not None:
                return self.parameter.name[0]
            return ""
        elif column==1:
            return self.parameter.unit
        elif column==2:
            return self.parameter.value_type
        elif column==3:
            return self.parameter.description
        return None

    def GetEditValue(self, column):
        if column==0:
            if self.parameter.name is None:
                return []
            return self.parameter.name
        return self.GetValue(column)

    def SetValue(self, column, value):
        field = {
            0: "name",
            1: "unit",
            2: "value_type",
            3: "description"
        }
        if self.parameter.id is None:
            # item has not yet be commited at this point and have no id
            # set edited field value
            setattr(self.parameter, field[column], value)
            if self.parameter.name!="":
                # save object in database
                commands.Do(CommandAddParameter, parameter=self.parameter)
            return True
        else:
            print(getattr(self.parameter, field[column]), value, getattr(self.parameter, field[column])!=value)
            if column in field and getattr(self.parameter, field[column])!=value:
                commands.Do(CommandUpateParameter, parameter=self.parameter, field=field[column], value=value)
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

class ParameterModel(TreeModel):
    def __init__(self):
        super(ParameterModel, self).__init__()

        self.InsertColumn(Column("Name"))
        self.InsertColumn(Column("Unit"))
        self.InsertColumn(Column("Value type"))
        self.InsertColumn(Column("Description"))

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
        self.loaded = True
        self.id_to_parameter_node[parameter.id] = node

        self.InsertNode(node, pos=pos)

    def RemoveParameterId(self, id):
        node = self.parameter_node_from_id(id)
        self.loaded = False
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
    
