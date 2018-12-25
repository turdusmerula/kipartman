from dialogs.panel_part_references import PanelPartReferences
import helper.tree

class DataModelPartReference(helper.tree.TreeContainerItem):
    def __init__(self, part, reference):
        super(DataModelPartReference, self).__init__()
        self.part = part
        self.reference = reference

    def GetValue(self, col):
            
        vMap = {
            0 : self.reference.type,
            1 : self.reference.manufacturer,
            2 : self.reference.name,
            3 : self.reference.description,
            4 : self.reference.uid,
        }
        return vMap[col]

    def IsContainer(self):
        return False

class PartReferencesFrame(PanelPartReferences):
    def __init__(self, parent): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(PartReferencesFrame, self).__init__(parent)

        # create references list
        self.tree_references_manager = helper.tree.TreeManager(self.tree_references, context_menu=self.menu_reference)
        self.tree_references_manager.AddTextColumn("Provider")
        self.tree_references_manager.AddTextColumn("Manufacturer")
        self.tree_references_manager.AddTextColumn("Name")
        self.tree_references_manager.AddTextColumn("Description")
        self.tree_references_manager.AddTextColumn("UID")
        self.tree_references_manager.OnItemBeforeContextMenu = self.onTreeReferencesBeforeContextMenu
        
        self.enable(False)
            
    def SetPart(self, part):
        self.part = part
        self.showReferences()
    
    def enable(self, enabled=True):
        self.enabled = enabled
    
    def AddReference(self, reference):
        """
        Add a reference to the part, or update if reference already exists
        """
        # check if reference exists
        if self.ExistReference(reference.name):
            # update existing reference
            self.RemoveReference(reference.name)
        
        # add reference
        if self.part.references is None:
            self.part.references = []
        self.part.references.append(reference)
        self.tree_references_manager.AppendItem(None, DataModelPartReference(self.part, reference))

    def ExistReference(self, name):
        """
        Test if a reference exists by its name
        """
        if not self.part.references:
            return False
        for param in self.part.references:
            if param.name==name:
                return True
        return False

    def FindReference(self, name):
        for data in self.tree_references_manager.data:
            if data.reference.name==name:
                return data
        return None
        

    def RemoveReference(self, name):
        """
        Remove a reference using its name
        """
        if not self.part.references:
            return False
        
        referenceobj = self.FindReference(name)
        self.part.references.remove(referenceobj.reference)
        self.tree_references_manager.DeleteItem(None, referenceobj)

    def showReferences(self):
        self.tree_references_manager.ClearItems()
    
        if self.part and self.part.references:
            for reference in self.part.references:
                self.tree_references_manager.AppendItem(None, DataModelPartReference(self.part, reference))

    def onTreeReferencesBeforeContextMenu( self, event ):
        self.menu_reference_remove_reference.Enable(True)
        if len(self.tree_references.GetSelections())==0:
            self.menu_reference_remove_reference.Enable(False)
        
        if self.enabled==False:
            self.menu_reference_remove_reference.Enable(False)
            
    def onMenuReferenceRemoveReference( self, event ):
        references = []
        for item in self.tree_references.GetSelections():
            obj = self.tree_references_manager.ItemToObject(item)
            if isinstance(obj, DataModelPartReference):
                references.append(obj)
        for referenceobj in references:
            self.part.references.remove(referenceobj.reference)
            self.tree_references_manager.DeleteItem(None, referenceobj)
