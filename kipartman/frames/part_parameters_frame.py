from dialogs.panel_part_parameters import PanelPartParameters
from frames.edit_part_parameter_frame import EditPartParameterFrame
from frames.dropdown_dialog import DropdownDialog
import wx.dataview
import api.queries

class PartParametersDataModel(wx.dataview.PyDataViewModel):
    def __init__(self, part):
        super(PartParametersDataModel, self).__init__()
        if part:
            self.data = part.parameters
        else:
            self.data = []
    def GetColumnCount(self):
        return 6

    def GetColumnType(self, col):
        mapper = { 
            0 : 'string',
            1 : 'string',
            2 : 'string',
            3 : 'string',
            4 : 'string',
            5 : 'string',
         }
        return mapper[col]

    def GetChildren(self, parent, children):
        # check root node
        if not parent:
            for octopart in self.data:
                children.append(self.ObjectToItem(octopart))
            return len(self.data)
        return 0
    
    def IsContainer(self, item):
        return False

    def HasContainerColumns(self, item):
        return True

    def GetParent(self, item):
        return wx.dataview.NullDataViewItem
    
    def GetValue(self, item, col):
        obj = self.ItemToObject(item)
        if obj.numeric==True:
            vMap = { 
                0 : obj.name,
                1 : obj.min_string(),
                2 : obj.nom_string(),
                3 : obj.max_string(),
                4 : obj.unit_string(),
                5 : obj.description,
            }
        else:
            vMap = { 
                0 : obj.name,
                1 : "",
                2 : obj.text_value,
                3 : "",
                4 : obj.unit_string(),
                5 : obj.description,
            }
            
        if vMap[col] is None:
            return ""
        return vMap[col]

    def SetValue(self, value, item, col):
        pass
    
    def GetAttr(self, item, col, attr):
        return False

#     def HasDefaultCompare(self):
#         return False
#     
#     def Compare(self, item1, item2, column, ascending):
        #TODO allow sort integer columns properly
            
class PartParametersFrame(PanelPartParameters):
    def __init__(self, parent): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(PartParametersFrame, self).__init__(parent)

        # create octoparts list
        self.parameters_model = PartParametersDataModel(None)
        self.tree_parameters.AssociateModel(self.parameters_model)
        # add default columns
        self.tree_parameters.AppendTextColumn("Parameter", 0, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_parameters.AppendTextColumn("Min Value", 1, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_parameters.AppendTextColumn("Nominal Value", 2, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_parameters.AppendTextColumn("Max Value", 3, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_parameters.AppendTextColumn("Unit", 4, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_parameters.AppendTextColumn("Description", 5, width=wx.COL_WIDTH_AUTOSIZE)
        for c in self.tree_parameters.Columns:
            c.Sortable = True

        # set result functions
        self.cancel = None
        self.result = None
        
    def SetResult(self, result, cancel=None):
        """
        Callbacks for parent dialog
        """
        self.result = result
        self.cancel = cancel
    
    def SetPart(self, part):
        # array of changes to apply
        self.create_list = []
        self.update_list = []
        self.remove_list = []

        self.part = part
        self._showParameters()
    
    def AddParameter(self, parameter):
        """
        Add a parameter to the part, or update if parameter already exists
        """
        # check if parameter exists
        if self.ExistParameter(parameter.name):
            # update existing parameter
            self.RemoveParameter(parameter.name)
        
        # add parameter
        self.part.parameters.append(parameter)
        self.create_list.append(parameter)
        self._showParameters()

    def ExistParameter(self, name):
        """
        Test if a parameter exists by its name
        """
        for param in self.part.parameters:
            if param.name==name:
                return True
        return False

    def RemoveParameter(self, name):
        """
        Remove a parameter using its name
        """
        for param in self.part.parameters:
            if param.name==name:
                if param.id!=-1:
                    self.remove_list.append(param)
                    self.part.parameters.remove(param)
                    # remove it from update list if present
                    try:
                        # remove it if already exists
                        self.update_list.remove(param)
                    except:
                        pass
                else:
                    self.part.parameters.remove(param)
                    

    def _showParameters(self):
        # apply new filter and reload
        self.parameters_model.Cleared()
        self.parameters_model = PartParametersDataModel(self.part)
        self.tree_parameters.AssociateModel(self.parameters_model)
    
    def ApplyChanges(self, part):
        for param in self.remove_list:
            param.part = part
            api.queries.PartParametersQuery().delete(param)
        self.remove_list = []

        # apply changes to current part
        for param in self.create_list:
            param.part = part
            api.queries.PartParametersQuery().create(param)
        self.create_list = []
        
        for param in self.update_list:
            param.part = part
            api.queries.PartParametersQuery().update(param)
        self.update_list = []
        
    def onButtonAddParameterClick( self, event ):
        parameter = EditPartParameterFrame(self).AddParameter(self.part)
        if not parameter is None:
            self.part.parameters.append(parameter)
            self.create_list.append(parameter)
        self._showParameters()
            
    def onButtonEditParameterClick( self, event ):
        parameter = self.parameters_model.ItemToObject(self.tree_parameters.GetSelection())
        if not parameter:
            return 
        if EditPartParameterFrame(self).EditParameter(self.part, parameter) and parameter.id!=-1:
            # set parameter to be updated
            try:
                # remove it from update list to avoid multiple update
                self.update_list.remove(parameter)
            except:
                pass
            self.update_list.append(parameter)
        self._showParameters()
    
    def onButtonRemoveParameterClick( self, event ):
        item = self.tree_parameters.GetSelection()
        if not item:
            return
        parameter = self.parameters_model.ItemToObject(item)
        self.part.parameters.remove(parameter)
        # set parameter to be removed
        if parameter.id!=-1:
            self.remove_list.append(parameter)
            try:
                # remove it from update list if present
                self.update_list.remove(parameter)
            except:
                pass

        self._showParameters()
