import helper.tree
import api.data.part_parameter
from helper.unit import format_unit_prefix

class PartParameter(helper.tree.TreeContainerItem):
    def __init__(self, part, parameter):
        super(PartParameter, self).__init__()
        self.part = part
        self.part_parameter = parameter
    
    def GetValue(self, col):
        unit_symbol = ''
        if self.part_parameter.parameter.unit is not None:
            unit_symbol = self.part_parameter.parameter.unit.symbol
        
        if col==0:
            if self.part.value_parameter is not None and self.part.value_parameter==self.part_parameter.parameter.name:
                return True
            return False
        elif col==1:
            return self.part_parameter.parameter.name
        elif col==5:
            if self.part_parameter.parameter.unit:
                return self.part_parameter.parameter.unit.name
        elif col==6:
            return self.part_parameter.parameter.description
        
        if self.part_parameter.parameter.numeric==True:
            if col==2:
                if self.part_parameter.nom_value is not None:
                    return format_unit_prefix(self.part_parameter.nom_value, unit_symbol)
            elif col==3:
                if self.part_parameter.min_value is not None:
                    return format_unit_prefix(self.part_parameter.min_value, unit_symbol)
            elif col==4:
                if self.part_parameter.max_value is not None:
                    return format_unit_prefix(self.part_parameter.max_value, unit_symbol)
        else:
            if col==2:
                return self.part_parameter.text_value
            
        return ""

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
        
        self.AddToggleColumn("*")
        self.AddTextColumn("Parameter")
        self.AddTextColumn("Value")
        self.AddTextColumn("Min")
        self.AddTextColumn("Max")
        self.AddTextColumn("Unit")
        self.AddTextColumn("Description")
        
    def Load(self):
        
        self.SaveState()
        
        if self.part is not None:
            for parameter in self.part.parameters.all():
                parameterobj = self.FindParameter(parameter)
                if parameterobj is None:
                    parameterobj = PartParameter(parameter.part, parameter)
                    self.Append(None, parameterobj)
                else:
                    parameterobj.part = self.part
                    parameterobj.part_parameter = parameter
                    self.Update(parameterobj)

            # add not yet persisted data
            for parameter in self.part.parameters.pendings():
                parameterobj = self.FindParameter(parameter)
                if parameterobj is None:
                    parameterobj = PartParameter(parameter.part, parameter)
                    self.Append(None, parameterobj)
                else:
                    parameterobj.part = self.part
                    parameterobj.part_parameter = parameter
                    self.Update(parameterobj)
        
        self.PurgeState()
    
    def SetPart(self, part):
        self.part = part
        self.Load()
        
    def FindParameter(self, parameter):
        for data in self.data:
            if isinstance(data, PartParameter) and (data.part_parameter.id is not None and data.part_parameter.id==parameter.id) or data.part_parameter==parameter:
                return data
        return None
