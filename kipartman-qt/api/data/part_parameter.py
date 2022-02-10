from PyQt6.QtCore import QRunnable, QThreadPool, QModelIndex
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import QAbstractItemView, QHeaderView

from enum import Enum

from api.treeview import TreeModel, Node, TreeColumn, ValidationError, QTreeViewData
from api.command import CommandUpdateDatabaseField, CommandAddDatabaseObject, CommandDeleteDatabaseObjects, commands
from api.event import events
from api.unit import ureg
import database.data.part_parameter
from database.models import Part, Parameter, PartParameter, ParameterType, PartInstance
from ui.parameter_select_delegate import QParameterSelectDelegate
from ui.unit_delegate import QUnitDelegate

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
        
class PartParameterColumn():
    PARAMETER = 0
    OPERATOR = 1
    VALUE = 2
    UNIT = 3
    DESCRIPTION = 4

class KicadPartParameter():
    FOOTPRINT = "Footprint"
    SYMBOL = "Symbol"
    MODEL3D = "3D Model"
    VALUE = "Value"

class PartParameterGroup():
    KICAD = "Kicad"
    PARAMETER = "Parameters"

class PartParameterGroupNode(Node):
    def __init__(self, title, parent=None):
        super(PartParameterGroupNode, self).__init__(parent)
        self.title = title

        self.font = QFont()
        self.font.setBold(True)

        self.background = QColor(128, 128, 128)
        self.foreground = QColor(255, 255, 255)

    def GetValue(self, column):
        if column==PartParameterColumn.PARAMETER:
            return self.title
        return None
    
    def GetFlags(self, column, flags):
        return flags & ~Qt.ItemFlag.ItemIsEditable

    def GetFont(self, column):
        return self.font

    def GetBackground(self, column):
        return self.background

    def GetForeground(self, column):
        return self.foreground

class KicadPartParameterNode(Node):
    def __init__(self, part, kicad_part_parameter, parent=None):
        super(KicadPartParameterNode, self).__init__(parent)
        self.part = part
        self.kicad_part_parameter = kicad_part_parameter

    def GetValue(self, column):
        if column==PartParameterColumn.PARAMETER:
            return self.kicad_part_parameter
        elif column==PartParameterColumn.VALUE:
            if self.kicad_part_parameter==KicadPartParameter.FOOTPRINT:
                return self.part.footprint
            elif self.kicad_part_parameter==KicadPartParameter.SYMBOL:
                return self.part.symbol
            elif self.kicad_part_parameter==KicadPartParameter.MODEL3D:
                return self.part.model3d
            elif self.kicad_part_parameter==KicadPartParameter.VALUE:
                return self.part.value
            
    def GetFlags(self, column, flags):
        return flags & ~Qt.ItemFlag.ItemIsEditable

class PartParameterNode(Node):
    def __init__(self, part_parameter, parent=None):
        super(PartParameterNode, self).__init__(parent)
        self.part_parameter = part_parameter

    def GetValue(self, column):
        if column==PartParameterColumn.PARAMETER:
            if hasattr(self.part_parameter, 'parameter'):
                return self.part_parameter.parameter.name
        elif column==PartParameterColumn.OPERATOR:
            pass
        elif column==PartParameterColumn.VALUE:
            field = self.part_parameter.value_type_field
            if field is not None:
                return getattr(self.part_parameter, field)
        elif column==PartParameterColumn.UNIT:
            if self.part_parameter.unit is not None:
                return self.part_parameter.unit
            elif hasattr(self.part_parameter, 'parameter'):
                return self.part_parameter.parameter.unit
            return None
        elif column==PartParameterColumn.DESCRIPTION:
            if hasattr(self.part_parameter, 'parameter'):
                return self.part_parameter.parameter.description
            return ""
        return None

    def GetEditValue(self, column):
        if column==PartParameterColumn.PARAMETER:
            if hasattr(self.part_parameter, 'parameter'):
                return self.part_parameter.parameter
            else:
                return None
        return self.GetValue(column)

    def SetValue(self, column, value):
        
        if column!=PartParameterColumn.PARAMETER and hasattr(self.part_parameter, 'parameter')==False:
            # can not set any value until parameter is set
            return False
        
        field = {
            PartParameterColumn.PARAMETER: "parameter",
            PartParameterColumn.VALUE: self.part_parameter.value_type_field,
            PartParameterColumn.UNIT: "unit",
        }
            
        other_fields = {}
        
        if column==PartParameterColumn.PARAMETER:
            other_fields = {
                "unit": None,
                
                "int_value": None,
                "float_value": None,
                "text_value": None,
                "boolean_value": None,
                "list_value": None,
            }

        if self.part_parameter.id is None:
            # item has not yet been commited at this point and have no id
            # set edited field value
            setattr(self.part_parameter, field[column], value)
            if hasattr(self.part_parameter, 'parameter'):
                # save object in database
                commands.Do(CommandAddPartParameter, part_parameter=self.part_parameter)
            return True
        else:
            if column in field and getattr(self.part_parameter, field[column])!=value:
                commands.Do(CommandUpatePartParameter, part_parameter=self.part_parameter, field=field[column], value=value, other_fields=other_fields)
                return True
        return False

            
    def Validate(self, column, value):
        if column==PartParameterColumn.PARAMETER:
            if value is None:
                return ValidationError("No parameter set")
            # TODO check duplicates in database
        elif column==PartParameterColumn.UNIT:
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
        if column==PartParameterColumn.DESCRIPTION:
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
        self.part = None

        self.group_nodes = [PartParameterGroup.KICAD, PartParameterGroup.PARAMETER]
        self.kicad_nodes = [KicadPartParameter.FOOTPRINT, KicadPartParameter.MODEL3D, KicadPartParameter.SYMBOL, KicadPartParameter.VALUE]

    def SetPart(self, part):
        self.part = part

    def index_from_part_parameter_id(self, id):
        node = self.FindPartParameterNode(id)
        return self.index_from_node(node)
    
    def CanFetchMore(self, parent):
        return not self.loaded

    def Fetch(self, parent):
        print("PartParameterModel.Fetch")
        
        self.SaveState()
            
        # prevent recursive Fetch
        self.loaded = True

        if self.part is not None:
            for group in self.group_nodes:
                group_node = self.FindPartParameterGroupNode(group)
                if group_node is None:
                    group_node = PartParameterGroupNode(group)
                    self.InsertNode(group_node)
                else:
                    self.UpdateNode(group_node)

            for kicad_part_parameter in self.kicad_nodes:
                kicad_part_parameter_node = self.FindKicadPartParameterNode(kicad_part_parameter)
                if kicad_part_parameter_node is None:
                    kicad_part_parameter_node = KicadPartParameterNode(part=self.part, kicad_part_parameter=kicad_part_parameter)
                    self.InsertNode(kicad_part_parameter_node, parent=self.FindPartParameterGroupNode(PartParameterGroup.KICAD))
                else:
                    kicad_part_parameter_node.part = self.part
                    kicad_part_parameter_node.kicad_part_parameter = kicad_part_parameter
                    self.UpdateNode(kicad_part_parameter_node)
        
            for part_parameter in self.part.parameters.all():
                part_parameter_node = self.FindPartParameterNode(part_parameter.id)
                if part_parameter_node is None:
                    part_parameter_node = self.AddPartParameter(part_parameter, header=self.FindPartParameterGroupNode(PartParameterGroup.PARAMETER))
                else:
                    part_parameter_node.part_parameter = part_parameter
                    self.UpdateNode(part_parameter_node)
        
        # remove remaining nodes
        self.PurgeState()

    def Update(self):
        self.loaded = False
        super(PartParameterModel, self).Update()
        
    def Clear(self):
        self.loaded = False
        super(PartParameterModel, self).Clear()

    def CreateEditNode(self, parent):
        if self.part is None:
            return None
        
        if self.part.instance==PartInstance.PART:
            return PartParameterNode(PartParameter(part=self.part, metaparameter=False))
        elif self.part.instance==PartInstance.METAPART:
            return PartParameterNode(PartParameter(part=self.part, metaparameter=True))
        return None


    def FindPartParameterGroupNode(self, title):
        for node in self.node_to_id:
            if isinstance(node, PartParameterGroupNode) and node.title==title:
                return node
        return None
    
    def FindKicadPartParameterNode(self, kicad_part_parameter):
        for node in self.node_to_id:
            if isinstance(node, KicadPartParameterNode) and node.kicad_part_parameter==kicad_part_parameter:
                return node
        return None
        
    def FindPartParameterNode(self, id):
        for node in self.node_to_id:
            if isinstance(node, PartParameterNode) and node.part_parameter.id==id:
                return node
        return None

    def AddPartParameter(self, part_parameter, header, pos=None):
        node = PartParameterNode(part_parameter)
        self.InsertNode(node, pos=pos, parent=header)

    def RemovePartParameterId(self, id):
        node = self.part_parameter_node_from_id(id)
        self.RemoveNode(node)

    def RemovePartParameter(self, part_parameter):
        node = self.part_parameter_node_from_id(part_parameter.id)
        self.RemoveNode(node)


class QPartParameterTreeView(QTreeViewData):
    def __init__(self, *args, **kwargs):
        super(QPartParameterTreeView, self).__init__(*args, **kwargs)
    
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        
        self.endInsertEditNode.connect(self.OnEndInsertEditNode)

        events.objectUpdated.connect(self.objectChanged)
        events.objectAdded.connect(self.objectChanged)
        events.objectDeleted.connect(self.objectChanged)


    def setModel(self, model):
        super(QPartParameterTreeView, self).setModel(model)
        
        self.parameterSelectDelegate = QParameterSelectDelegate(model)
        self.setItemDelegateForColumn(PartParameterColumn.PARAMETER, self.parameterSelectDelegate) 

        self.unitDelegate = QUnitDelegate(model)
        self.setItemDelegateForColumn(PartParameterColumn.UNIT, self.unitDelegate) 

        self.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)        

        self.setAlternatingRowColors(True)
        self.setIndentation(0)

    def rowsInserted(self, parent, first, last):
        if self.isExpanded(parent)==False:
            self.expand(parent)
    
        # span first column for group nodes to make a title line
        node = self.model().node_from_id(parent.internalId())
        if isinstance(node, PartParameterGroupNode):
            parent_index = self.model().index_from_node(node.parent)
            self.setFirstColumnSpanned(node.parent.row_from_child(node), parent_index, True)

    def SetPart(self, part):
        print("QPartParameterTreeView.SetPart")
        if part is None or part.instance!=PartInstance.METAPART:
            self.setColumnHidden(PartParameterColumn.OPERATOR, True)
        else:
            self.setColumnHidden(PartParameterColumn.OPERATOR, False)
        self.model().SetPart(part)

    def objectChanged(self, object):
        if isinstance(object, PartParameter) or (isinstance(object, Part) and part==self.model().part) or isinstance(object, Parameter):
            self.model().Update()
            
    def OnEndInsertEditNode(self, node):
        part_parameter = node.part_parameter
        self.setCurrentIndex(self.model().index_from_part_parameter_id(part_parameter.id))
        
        # add code to select item on redo in this current view only
        commands.LastUndo.done.connect(
            lambda treeView=self, part_parameter=part_parameter: 
                self.setCurrentIndex(treeView.model().index_from_part_parameter_id(part_parameter.id))
        )
    
