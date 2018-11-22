from dialogs.panel_edit_module import PanelEditModule
import wx.lib.newevent
import os.path
import cfscrape
from configuration import Configuration
import json
from helper.exception import print_stack

EditModuleApplyEvent, EVT_EDIT_FOOTPRINT_APPLY_EVENT = wx.lib.newevent.NewEvent()
EditModuleCancelEvent, EVT_EDIT_FOOTPRINT_CANCEL_EVENT = wx.lib.newevent.NewEvent()

scraper = cfscrape.create_scraper()

none_image = os.path.abspath(os.path.join('resources', 'none-128x128.png'))

def NoneValue(value, default):
    if value:
        return value
    return default

def MetadataValue(metadata, value, default):
    if metadata is None:
        return default
    if value in metadata:
        return metadata[value]
    return default

class EditModuleFrame(PanelEditModule): 
    def __init__(self, parent):
        super(EditModuleFrame, self).__init__(parent)
        self.snapeda_uid = ''
        self.module_path = ''
        
    def SetModule(self, module):
        self.module = module
        self.ShowModule(module)

    def ShowModule(self, module):
        configuration = Configuration()
        
        # enable everything else
        if module:
            
            if module.metadata:
                metadata = json.loads(module.metadata)
            else:
                metadata = json.loads('{}')

            self.edit_module_name.Value = ''
            self.module_path = ''
            
            if NoneValue(module.source_path, '')!='':
                name = os.path.basename(module.source_path)
                self.edit_module_name.Value = name.replace(".module", "")
                self.module_path = os.path.dirname(NoneValue(module.source_path, ''))
                    
            self.edit_module_description.Value = MetadataValue(metadata, 'description', '')
            self.edit_module_comment.Value = MetadataValue(metadata, 'comment', '')
        else:
            self.edit_module_name.Value = ''
            self.edit_module_description.Value = ''
            self.edit_module_comment.Value = ''
        
    def enable(self, enabled=True):
        self.edit_module_name.Enabled = enabled
        self.edit_module_description.Enabled = enabled
        self.edit_module_comment.Enabled = enabled
        self.button_module_editApply.Enabled = enabled
        self.button_module_editCancel.Enabled = enabled
        
    def onButtonModuleEditApply( self, event ):
        module = self.module
        
        if module.metadata:
            metadata = json.loads(module.metadata)
        else:
            metadata = json.loads('{}')
        metadata['description'] = self.edit_module_description.Value
        metadata['comment'] = self.edit_module_comment.Value
                
        module.metadata = json.dumps(metadata)
            
        # send result event
        event = EditModuleApplyEvent(
            data=module,
            # source_path is not changed in the module as we only have the filename here, not the full path
            # the full path should be reconstructed by caller
            module_name=self.edit_module_name.Value+".module"
            )
        wx.PostEvent(self, event)
    
    def onButtonModuleEditCancel( self, event ):
        event = EditModuleCancelEvent()
        wx.PostEvent(self, event)
