from helper.tree import TreeModel
import helper.tree
import wx

class TreeModelParameters(TreeModel):
    def __init__(self):
        super(TreeModelParameters, self).__init__()

    def GetColumnParameter(self, parameter):
        for column in self.columns_name:
            if self.columns_name[column]==parameter:
                return column
        return None
    
    def Compare(self, item1, item2, column, ascending):
        if self.columns_type[column]!='parameter':
            return super(TreeModelParameters, self).Compare(item1, item2, column, ascending)
        else:
            param1 = self.ItemToObject(item1)
            param2 = self.ItemToObject(item2)
            
            if not param1 and not param2:
                return super(TreeModelParameters, self).Compare(item1, item2, column, ascending)
            elif param1.HasValue(column)==False and param2.HasValue(column)==False:
                return super(TreeModelParameters, self).Compare(item1, item2, column, ascending)

            if not ascending: 
                param2, param1 = param1, param2

            if param1.HasValue(column)==False:
                return 1
            elif param2.HasValue(column)==False:
                return -1

            if param1.IsNumeric(column)==False or param2.IsNumeric(column)==False:
                return helper.tree.CompareString(param1.GetValue(column), param2.GetValue(column))

            if param1.GetUnit(column) and param2.GetUnit(column) and param1.GetUnit(column)!=param2.GetUnit(column):
                return helper.tree.CompareString(param1.GetValue(column), param2.GetValue(column))

            value1 = param1.GetNumericValue(column)                
            value2 = param2.GetNumericValue(column)
            
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
    