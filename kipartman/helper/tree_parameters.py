from helper.tree import TreeModel
import helper.tree
import wx

class TreeModelParameters(TreeModel):
    def __init__(self):
        super(TreeModelParameters, self).__init__()

    def Compare(self, item1, item2, column, ascending):
        if self.columns_type[column]!='parameter':
            return super(TreeModelParameters, self).Compare(item1, item2, column, ascending)
        else:
            obj1 = self.ItemToObject(item1)
            obj2 = self.ItemToObject(item2)

            if obj1:
                param1 = obj1.GetParam(column)
            if obj2:
                param2 = obj2.GetParam(column)
            
            # none element are always treated inferior
            if not param1 and param2:
                return 1
            elif param1 and not param2:
                return -1
            elif not param1 and not param2:
                return super(TreeModelParameters, self).Compare(item1, item2, column, ascending)

            if not ascending: # swap sort order?
                param2, param1 = param1, param2

            
            if param1.numeric!=param2.numeric:
                return super(TreeModelParameters, self).Compare(item1, item2, column, ascending)

            if param1.numeric==False and param2.numeric==False:
                return helper.tree.CompareString(param1.text_value, param2.text_value)

            if param1.unit and param2.unit and param1.unit!=param2.unit:
                return helper.tree.CompareString(param1.unit.name, param2.unit.name)

            value1 = 0
            if param1.nom_value:
                value1 = param1.nom_value
            if param1.nom_prefix:
                value1 = value1*float(param1.nom_prefix.power)
                
            value2 = 0
            if param2.nom_value:
                value2 = param2.nom_value
            if param2.nom_prefix:
                value2 = value2*float(param2.nom_prefix.power)
            
            if value2>value1:
                return -1
            elif value1>value2:
                return 1
            return 0

class TreeManagerParameters(helper.tree.TreeManager):
    def __init__(self, tree_view, model=None, context_menu=None):
        model = TreeModelParameters()
        super(TreeManagerParameters, self).__init__(tree_view, model, context_menu)

    def AddParameterColumn(self, title):
        column = self.tree_view.AppendTextColumn(title, len(self.model.columns_type), width=wx.COL_WIDTH_AUTOSIZE)
        self.model.columns_type[column.GetModelColumn()] = 'parameter'
        self.model.columns_name[column.GetModelColumn()] = title
        self.model.sort_function[column.GetModelColumn()] = None
        column.Sortable = True
        column.Reorderable = True
        return column
    