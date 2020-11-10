import helper.tree
import api.data.part_parameter
from helper.unit import format_unit_prefix, format_float

class PartParameter(helper.tree.TreeContainerItem):
    def __init__(self, part, parameter):
        super(PartParameter, self).__init__()
        self.part = part
        self.part_parameter = parameter
    
    def GetValue(self, col):
        if col==0:
            return self.part_parameter.parameter.name
        elif col==1:
            value = api.data.part_parameter.expanded_parameter_value(self.part_parameter, with_operator=True)
            if value is not None:
                return value
        elif col==2:
            if self.part_parameter.parameter.unit:
                return self.part_parameter.parameter.unit.name
        elif col==3:
            return self.part_parameter.parameter.description
        
        return "-"

    def GetAttr(self, col, attr):
        res = False
        if self.part_parameter.id is None:
            attr.SetColour(helper.colors.GREEN_NEW_ITEM)
            res = True
        if self.part_parameter.removed_pending():
            attr.SetStrikethrough(True)
            res = True
        return res
    
class TreeManagerPartParameter(helper.tree.TreeManager):

    def __init__(self, tree_view, *args, **kwargs):
        super(TreeManagerPartParameter, self).__init__(tree_view, *args, **kwargs)

        self.part = None
        
        self.AddTextColumn("parameter")
        self.AddTextColumn("value")
        self.AddTextColumn("unit")
        self.AddTextColumn("description")
        
    def Load(self):
        
        self.SaveState()
        
        if self.part is not None:
            for parameter in self.part.parameters.all():
                parameterobj = self.FindParameter(parameter)
                if parameterobj is None:
                    parameterobj = PartParameter(parameter.part, parameter)
                    self.Append(None, parameterobj)
                else:
                    # all() extracts from database, fields are not updated to avoid discarding changes
                    self.Update(parameterobj)

            # add not yet persisted data
            for parameter in self.part.parameters.pendings():
                parameterobj = self.FindParameter(parameter)
                if parameterobj is None:
                    parameterobj = PartParameter(parameter.part, parameter)
                    self.Append(None, parameterobj)
                else:
                    self.Update(parameterobj)
        
        self.PurgeState()
    
    def SetPart(self, part):
        self.part = part

        self.Clear()
        self.Load()
        
    def FindParameter(self, parameter):
        for data in self.data:
            if isinstance(data, PartParameter) and (data.part_parameter.id is not None and data.part_parameter.id==parameter.id) or data.part_parameter==parameter:
                return data
        return None
