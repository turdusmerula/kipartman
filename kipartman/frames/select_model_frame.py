from dialogs.panel_select_model import PanelSelectModel
import helper.tree
import rest
import wx

class DataModelCategoryPath(helper.tree.TreeContainerItem):
    def __init__(self, category):
        super(DataModelCategoryPath, self).__init__()
        self.category = category
    
    def GetValue(self, col):
        if self.category:
            path = self.category.path
        else:
            path = "/"
        if col==0   :
            return path
        return ''

    def HasContainerColumns(self):
        return True

    def GetAttr(self, col, attr):
        if col==1:
            attr.Bold = True
            return True
        return False
    
class DataModelModel(helper.tree.TreeItem):
    def __init__(self, model):
        super(DataModelModel, self).__init__()
        self.model = model
            
    def GetValue(self, col):
        vMap = { 
            0 : self.model.name,
            1 : self.model.description,
        }
        return vMap[col]


class TreeManagerModels(helper.tree.TreeManager):
    def __init__(self, tree_view):
        super(TreeManagerModels, self).__init__(tree_view)

    def FindModel(self, model_id):
        for data in self.data:
            if isinstance(data, DataModelModel) and data.model.id==model_id:
                return data
        return None


class SelectModelFrame(PanelSelectModel):
    def __init__(self, parent, initial=None): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(SelectModelFrame, self).__init__(parent)
        
        # create models list
        self.tree_models_manager = TreeManagerModels(self.tree_models)
        self.tree_models_manager.AddTextColumn("Name")
        self.tree_models_manager.AddTextColumn("Description")
        
        self.search_filter = None
        self.search_model.Value = ''
        self.load()
        
        if initial:
            self.tree_models.Select(self.tree_models_manager.ObjectToItem(self.tree_models_manager.FindModel(initial.id)))
        
        # set result functions
        self.cancel = None
        self.result = None

    def load(self):
        try:
            self.loadModels()
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def loadModels(self):
        # clear all
        self.tree_models_manager.ClearItems()
        
        # load parts
        if self.search_filter:
            models = rest.api.find_models(search=self.search_filter)
        else:
            models = rest.api.find_models()
            
        # load categories
        categories = {}
        for model in models:
            if model.category:
                category_name = model.category.path
            else:
                category_name = "/"

            if categories.has_key(category_name)==False:
                categories[category_name] = DataModelCategoryPath(model.category)
                self.tree_models_manager.AppendItem(None, categories[category_name])
            self.tree_models_manager.AppendItem(categories[category_name], DataModelModel(model))
        
        for category in categories:
            self.tree_models_manager.Expand(categories[category])

    def SetResult(self, result, cancel=None):
        self.result = result
        self.cancel = cancel
        
    # Virtual event handlers, overide them in your derived class
    def onTreeModelsSelectionChanged( self, event ):
        event.Skip()
    
    def onButtonCancelClick( self, event ):
        if self.cancel:
            self.cancel()
    
    def onButtonOkClick( self, event ):
        model = self.tree_models_manager.ItemToObject(self.tree_models.GetSelection())
        if isinstance(model, DataModelModel) and self.result:
            self.result(model.model)

    def onSearchModelCancel( self, event ):
        self.search_filter = None
        self.load()
    
    def onSearchModelButton( self, event ):
        self.search_filter = self.search_model.Value
        self.load()
    
    def onSearchModelEnter( self, event ):
        self.search_filter = self.search_model.Value
        self.load()
