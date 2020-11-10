from dialogs.panel_edit_part import PanelEditPart
from frames.select_footprint_frame import SelectFootprintFrame
from frames.select_symbol_frame import SelectSymbolFrame
from frames.select_part_frame import SelectPartFrame
from frames.part_parameters_frame import PartParametersFrame
import api.data.part
from frames.part_distributors_frame import PartDistributorsFrame
from frames.part_manufacturers_frame import PartManufacturersFrame
from frames.part_attachements_frame import PartAttachementsFrame
from frames.part_storages_frame import PartStoragesFrame
from frames.part_preview_data_frame import PartPreviewDataFrame
from frames.part_references_frame import PartReferencesFrame
from frames.search_provider_part_dialog import SelectProviderPartDialog, EVT_SELECT_PART_OK_EVENT
from frames.dropdown_frame import DropdownFrame
from providers.provider import Provider
from providers.part_import import provider_part_to_model_part
from frames.dropdown_menu import DropdownMenu
# from frames.select_octopart_frame import SelectOctopartFrame, EVT_SELECT_OCTOPART_OK_EVENT
# from octopart.extractor import OctopartExtractor
import wx.lib.newevent
import datetime
import os
from helper.exception import print_stack
import pytz
from helper.log import log
from helper import colors
import json

EditPartApplyEvent, EVT_EDIT_PART_APPLY_EVENT = wx.lib.newevent.NewEvent()
EditPartCancelEvent, EVT_EDIT_PART_CANCEL_EVENT = wx.lib.newevent.NewEvent()

def NoneValue(value, default):
    if value:
        return value
    return default

class EditPartFrame(PanelEditPart): 
    def __init__(self, parent):
        super(EditPartFrame, self).__init__(parent)
        
        self.edit_part_parameters = PartParametersFrame(self.notebook_part)
        self.notebook_part.AddPage(self.edit_part_parameters, "Parameters")
         
#         self.edit_part_preview_data = PartPreviewDataFrame(self.notebook_part)
#         self.notebook_part.AddPage(self.edit_part_preview_data, "Preview")
 
        self.edit_part_distributors = PartDistributorsFrame(self.notebook_part)
        self.notebook_part.AddPage(self.edit_part_distributors, "Distributors")
 
        self.edit_part_manufacturers = PartManufacturersFrame(self.notebook_part)
        self.notebook_part.AddPage(self.edit_part_manufacturers, "Manufacturers")
 
        self.edit_part_storages = PartStoragesFrame(self.notebook_part)
        self.notebook_part.AddPage(self.edit_part_storages, "Storages locations")
 
#         self.edit_part_attachements = PartAttachementsFrame(self.notebook_part)
#         self.notebook_part.AddPage(self.edit_part_attachements, "Attachements")
 
        self.edit_part_references = PartReferencesFrame(self.notebook_part)
        self.notebook_part.AddPage(self.edit_part_references, "References")

        self._category = None
        self._footprint = None
        self._symbol = None
        
        # set initial state
        self.SetPart(None)
        self._enable(False)
        self._init_providers()
        
    def SetPart(self, part):
        if part is None:
            self._footprint = None
            self._symbol = None
            self._category = None
        else:
            self._footprint = part.footprint
            self._symbol = part.symbol
            self._category = part.category
        self.part = part
        self._show_part(part)
        self.edit_part_parameters.SetPart(part)
        self.edit_part_distributors.SetPart(part)
        self.edit_part_manufacturers.SetPart(part)
        self.edit_part_storages.SetPart(part)
#         self.edit_part_attachements.SetPart(part)
#         self.edit_part_preview_data.SetPart(part)
        self.edit_part_references.SetPart(part)
        self._enable(False)
        

    def EditPart(self, part):
        if part is None:
            self._footprint = None
            self._symbol = None
            self._category = None
        else:
            self._footprint = part.footprint
            self._symbol = part.symbol
            self._category = part.category
        self.part = part
        self._show_part(part)
        self.edit_part_parameters.EditPart(part)
        self.edit_part_distributors.EditPart(part)
        self.edit_part_manufacturers.EditPart(part)
        self.edit_part_storages.EditPart(part)
#         self.edit_part_attachements.EditPart(part)
#         self.edit_part_preview_data.EditPart(part)
        self.edit_part_references.EditPart(part)
        self._enable(True)
        self._check()
            
    def AddPart(self, category):
        self._category = category
        self._footprint = None
        self._symbol = None
        self.part = api.data.part.create(category=category)
        self._show_part(self.part)
        self.edit_part_parameters.EditPart(self.part)
        self.edit_part_distributors.EditPart(self.part)
        self.edit_part_manufacturers.EditPart(self.part)
        self.edit_part_storages.EditPart(self.part)
#         self.edit_part_attachements.EditPart(self.part)
#         self.edit_part_preview_data.EditPart(self.part)
        self.edit_part_references.EditPart(self.part)
        self._enable(True)
        self._check()

    def AddMetaPart(self, category):
        self._category = category
        self._footprint = None
        self._symbol = None
        self._metapart = True
        self.part = api.data.part.create(category=category, metapart=True)
        self._show_part(self.part)
        self.edit_part_parameters.EditPart(self.part)
        self.edit_part_distributors.EditPart(self.part)
        self.edit_part_manufacturers.EditPart(self.part)
        self.edit_part_storages.EditPart(self.part)
#         self.edit_part_attachements.EditPart(self.part)
#         self.edit_part_preview_data.EditPart(self.part)
        self.edit_part_references.EditPart(self.part)
        self._enable(True)
        self._check()

    def _init_providers(self):
        for provider in Provider.providers:
            if provider.has_search_part:
                menu_item = wx.MenuItem( self.menu_search, wx.ID_ANY, provider.description, wx.EmptyString, wx.ITEM_NORMAL )
                self.menu_search.Append( menu_item )
#                 self.Bind( wx.EVT_MENU, self.onMenuSelection, id = self.m_menuItem1.GetId() )
        
    def _show_part(self, part):
        if part is not None:
            self.edit_part_name.Value = NoneValue(part.name, "")
            self.edit_part_description.Value = NoneValue(part.description, "")
            self.edit_part_comment.Value = NoneValue(part.comment, '')
            
            try:
                json_value = json.loads(part.value)
            except:
                json_value = json.loads("{}")
                json_value["pattern"] = part.value
            self.edit_part_value.Value = json_value["pattern"]
            self.show_part_value.Value = api.data.part.expanded_value(part, json_value["pattern"])
            
            if part.footprint is not None:
                self.button_part_footprint.Label = part.footprint.name
            else:
                self.button_part_footprint.Label = "<none>"
            if part.symbol is not None:
                self.button_part_symbol.Label = part.symbol.name
            else:
                self.button_part_symbol.Label = "<none>"
        else:
            self.edit_part_name.Value = ''
            self.edit_part_description.Value = ''
            self.edit_part_comment.Value = ''
            self.edit_part_value.Value = ''
            self.show_part_value.value = ''
            self.button_part_footprint.Label = "<none>"
            self.button_part_symbol.Label = "<none>"
            
    def _enable(self, enabled=True):
        self.edit_part_name.Enabled = enabled
        self.button_search.Enabled = enabled
        self.edit_part_description.Enabled = enabled
        self.edit_part_value.Enabled = enabled
        self.show_part_value.Enabled = enabled
        self.button_part_footprint.Enabled = enabled
        self.button_remove_part_footprint.Enabled = enabled
        self.button_part_symbol.Enabled = enabled
        self.button_remove_part_symbol.Enabled = enabled
        self.edit_part_comment.Enabled = enabled
        self.button_part_editApply.Enabled = enabled
        self.button_part_editCancel.Enabled = enabled
#         self.edit_part_parameters.enable(enabled)
#         self.edit_part_distributors.enable(enabled)
#         self.edit_part_manufacturers.enable(enabled)
#         self.edit_part_storages.enable(enabled)
#         self.edit_part_attachements.enable(enabled)
#         self.edit_part_references.enable(enabled)
       
    def _check(self):
        error = False
        
        if self.edit_part_name.Value=="":
            self.edit_part_name.SetBackgroundColour( colors.RED_ERROR )
            error = True
        else:
            self.edit_part_name.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        
        if error:
            self.button_part_editApply.Enabled = False
        else:
            self.button_part_editApply.Enabled = True

    def onButtonPartEditApply( self, event ):
        
        try:
            if self.part is None:
                self.part = api.data.part.create()

            self.part.name = self.edit_part_name.Value
            self.part.description = self.edit_part_description.Value
            self.part.value = self.edit_part_value.Value
            self.part.footprint = self._footprint
            self.part.symbol = self._symbol
            self.part.comment = self.edit_part_comment.Value

            self.part.category = self._category

            self.edit_part_parameters.Save(self.part)
#             self.edit_part_distributors.Save(self.part)
            self.edit_part_manufacturers.Save(self.part)
            self.edit_part_storages.Save(self.part)
#             self.edit_part_attachements.Save(self.part)
#             self.edit_part_references.Save(self.part)

            # save part
            api.data.part.save(self.part)

            # send result event
            wx.PostEvent(self, EditPartApplyEvent(part=self.part))
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Error renaming library', wx.OK | wx.ICON_ERROR)
        
        event.Skip()
         
    def onButtonPartEditCancel( self, event ):
        wx.PostEvent(self, EditPartCancelEvent())
        event.Skip()

    def onTextEditPartNameText( self, event ):
        self._check()
        event.Skip()
        
    def onTextEditPartDescriptionText( self, event ):
        self._check()
        event.Skip()
    
    def onTextEditPartValueText( self, event ):
        self._check()
        self.show_part_value.Value = api.data.part.expanded_value(self.part, self.edit_part_value.Value)
        event.Skip()

    def onButtonPartFootprintClick( self, event ):
        frame = DropdownFrame(self.button_part_footprint, SelectFootprintFrame, self._footprint)
        frame.Dropdown(self.onSetFootprintCallback)
        event.Skip()
     
    def onSetFootprintCallback(self, footprint):
        self.button_part_footprint.Label = footprint.Name
        self._footprint = footprint.footprint_model

    def onButtonRemovePartFootprintClick( self, event ):
        self._footprint = None
        self.button_part_footprint.Label = "<none>"
        event.Skip()

    def onButtonPartSymbolClick( self, event ):
        frame = DropdownFrame(self.button_part_footprint, SelectSymbolFrame, self._symbol)
        frame.Dropdown(self.onSetSymbolCallback)
        event.Skip()
     
    def onSetSymbolCallback(self, symbol):
        self.button_part_symbol.Label = symbol.Name
        self._symbol = symbol.symbol_model

    def onButtonRemovePartSymbolClick( self, event ):
        self._symbol = None
        self.button_part_symbol.Label = "<none>"
        event.Skip()

    def onTextEditPartCommentText( self, event ):
        self._check()
        event.Skip()

    def onButtonSearchClick( self, event ):
        self.context_menu_pos = self.button_search.ScreenToClient(wx.GetMousePosition())
        id = DropdownMenu(self.button_search, self.menu_search).Dropdown()
        menu = self.menu_search.FindItemById(id)
        if menu is not None:
            provider = Provider.get_provider(description=menu.ItemLabel)
            self.select_part_dialog = SelectProviderPartDialog(self, provider, self.edit_part_name.Value)
            self.select_part_dialog.Bind( EVT_SELECT_PART_OK_EVENT, self.onSelectProviderPartFrameOk )
            self.select_part_dialog.ShowModal() 
        event.Skip()

    def onSelectProviderPartFrameOk(self, event):
        for provider_part in event.data:
            provider_part_to_model_part(self.select_part_dialog, provider_part, self.part)
        
        self.EditPart(self.part)
        
        print(event.data)
    