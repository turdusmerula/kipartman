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
from frames.search_provider_part_dialog import SelectProviderPartDialog
from frames.dropdown_frame import DropdownFrame
from providers.provider import Provider
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
         
        self.edit_part_preview_data = PartPreviewDataFrame(self.notebook_part)
        self.notebook_part.AddPage(self.edit_part_preview_data, "Preview")
 
        self.edit_part_distributors = PartDistributorsFrame(self.notebook_part)
        self.notebook_part.AddPage(self.edit_part_distributors, "Distributors")
 
        self.edit_part_manufacturers = PartManufacturersFrame(self.notebook_part)
        self.notebook_part.AddPage(self.edit_part_manufacturers, "Manufacturers")
 
        self.edit_part_storages = PartStoragesFrame(self.notebook_part)
        self.notebook_part.AddPage(self.edit_part_storages, "Storages locations")
 
        self.edit_part_attachements = PartAttachementsFrame(self.notebook_part)
        self.notebook_part.AddPage(self.edit_part_attachements, "Attachements")
 
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
        self._category = None
        if part is None:
            self._footprint = None
            self._symbol = None
        else:
            self._footprint = part.footprint
            self._symbol = part.symbol
        self.part = part
        self._show_part(part)
        self.edit_part_parameters.SetPart(part)
        self.edit_part_distributors.SetPart(part)
        self.edit_part_manufacturers.SetPart(part)
        self.edit_part_storages.SetPart(part)
        self.edit_part_attachements.SetPart(part)
        self.edit_part_preview_data.SetPart(part)
        self.edit_part_references.SetPart(part)
        self._enable(False)
        

    def EditPart(self, part):
        self._category = None
        if part is None:
            self._footprint = None
            self._symbol = None
        else:
            self._footprint = part.footprint
            self._symbol = part.symbol
        self.part = part
        self._show_part(part)
        self.edit_part_parameters.EditPart(part)
#         self.edit_part_distributors.EditPart(part)
#         self.edit_part_manufacturers.EditPart(part)
#         self.edit_part_storages.EditPart(part)
#         self.edit_part_attachements.EditPart(part)
#         self.edit_part_preview_data.EditPart(part)
#         self.edit_part_references.EditPart(part)
        self._enable(True)
        self._check()
            
    def AddPart(self, category):
        self._category = category
        self._footprint = None
        self._symbol = None
        self.part = None
        self._show_part(None)
        self.edit_part_parameters.EditPart(None)
#         self.edit_part_distributors.EditPart(None)
#         self.edit_part_manufacturers.EditPart(None)
#         self.edit_part_storages.EditPart(None)
#         self.edit_part_attachements.EditPart(None)
#         self.edit_part_preview_data.EditPart(None)
#         self.edit_part_references.EditPart(None)
        self._enable(True)
        self._check()

    def _init_providers(self):
        for provider in Provider.providers:
            if provider.has_search_part:
                menu_item = wx.MenuItem( self.menu_search, wx.ID_ANY, provider.name, wx.EmptyString, wx.ITEM_NORMAL )
                self.menu_search.Append( menu_item )
#                 self.Bind( wx.EVT_MENU, self.onMenuSelection, id = self.m_menuItem1.GetId() )
        
    def _show_part(self, part):
        if part is not None:
            self.edit_part_name.Value = NoneValue(part.name, "")
            self.edit_part_description.Value = NoneValue(part.description, "")
            self.edit_part_comment.Value = NoneValue(part.comment, '')
            self.edit_part_value.Value = part.value
#             self.show_part_value.value = part.value_content
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

    def _get_expanded_value(self, value):
#         parameters = {}
#         for parameter in api.data.part_parameter.find([api.data.part_parameter.FilterPart(part)]).all():
#             parameters[parameter.parameter.name] = parameter
#         
#         res = ""
#         token = None
#         for c in part.value:
#             if c=="{":
#                 token = ""
#             elif c=="}":
#                 if token=="name":
#                     res += part.name
#                 if token in parameters:
#                     res += ""
#                 token = None
#             else:
#                 if token is None:
#                     res += c
#                 else:
#                     token += c
        return ""

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

            self.edit_part_parameters.Save(self.part)
#             self.edit_part_distributors.Save(self.part)
#             self.edit_part_manufacturers.Save(self.part)
#             self.edit_part_storages.Save(self.part)
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
        self.show_part_value.Value = self._get_expanded_value(self.edit_part_value.Value)
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
            provider = Provider.get_provider(menu.ItemLabel)
            select_part_dialog = SelectProviderPartDialog(self, provider)
#             dropdown.panel.Bind( EVT_SELECT_OCTOPART_OK_EVENT, self.onSelectOctopartFrameOk )
            select_part_dialog.Show()
        event.Skip()

#     def onButtonOctopartClick( self, event ):
#         # create an octopart frame
#         # dropdown frame
#         dropdown = DropdownDialog(self.button_octopart, SelectOctopartFrame, self.edit_part_name.Value)
#         dropdown.panel.Bind( EVT_SELECT_OCTOPART_OK_EVENT, self.onSelectOctopartFrameOk )
#         dropdown.Dropdown()
# 
#     def addReferenceFromOctopart(self, octopart):
#         octopart_extractor = OctopartExtractor(octopart)
# 
#         reference = octopart_extractor.ExtractReference()
#         if octopart_extractor.has_error():
#             wx.MessageDialog(self, octopart_extractor.get_error_message(), "Octopart processing error", wx.OK | wx.ICON_WARNING)
# 
#         # add references in current part
#         if self.part.references is None:
#             self.part.references = []
#         part_reference =  next((p for p in self.part.references if p.type==reference['type'] and p.uid==reference['uid']), None)
#         if part_reference is None:
#             part_reference = rest.model.PartReference()
#             self.part.references.append(part_reference)
#         part_reference.type = reference['type']
#         part_reference.name = reference['name']
#         part_reference.uid = reference['uid']
#         part_reference.manufacturer = reference['manufacturer']
#         part_reference.description = reference['description']
#          
#     def addParametersFromOctopart(self, octopart):
#         octopart_extractor = OctopartExtractor(octopart)
# 
#         if self.part.parameters is None:
#             self.part.parameters = []
# 
#         # import parameters
#         for spec_name in octopart.item().specs():
#             parameter = octopart_extractor.ExtractParameter(spec_name)            
#             
#             part_parameter = next((p for p in self.part.parameters if p.name==spec_name), None)
#             if part_parameter is None:
#                 part_parameter = rest.model.PartParameter()
#                 self.part.parameters.append(part_parameter)
#             part_parameter.name = parameter['name']
#             part_parameter.description = parameter['description']
#             
#             part_parameter.unit = None
#             if parameter['unit']:
#                 units = []
#                 try:
#                     units = rest.api.find_units(symbol=parameter['unit']['symbol'])
#                 except Exception as e:
#                     print_stack()
#                     wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
#                 unit = None
#                 if len(units)==0:
#                     res = wx.MessageBox("Unit symbol '%s' does not exists, create it?" % (parameter['unit']['symbol']), 'Warning', wx.YES_NO | wx.ICON_QUESTION) 
#                     if res==wx.YES:
#                         try:
#                             unit = rest.model.Unit()
#                             unit.name = parameter['unit']['name']
#                             unit.symbol = parameter['unit']['symbol']
#                             unit = rest.api.add_unit(unit)
#                         except:
#                             print_stack()
#                             wx.MessageBox('%s: error creating unit' % (parameter['unit']['name']), 'Warning', wx.OK | wx.ICON_ERROR)
#                 else:
#                     unit = units[0]
#                 part_parameter.unit = unit        
#             
#             part_parameter.numeric = True
#             if (parameter['min_value'] and parameter['min_value']['numeric']==False) or \
#                 (parameter['nom_value'] and parameter['nom_value']['numeric']==False) or \
#                 (parameter['max_value'] and parameter['max_value']['numeric']==False):
#                 part_parameter.numeric = False
#             
#             part_parameter.min_prefix = None
#             part_parameter.nom_prefix = None
#             part_parameter.max_prefix = None
#             part_parameter.min_value = None            
#             part_parameter.nom_value = None            
#             part_parameter.max_value = None
#             part_parameter.text_value = None   
#             if part_parameter.numeric:
#                 if parameter['min_value']:
#                     part_parameter.min_prefix = None # TODO
#                     part_parameter.min_value = parameter['min_value']['value']
#                 if parameter['nom_value']:
#                     part_parameter.nom_value = None # TODO
#                     part_parameter.nom_value = parameter['nom_value']['value']
#                 if parameter['max_value']:
#                     part_parameter.max_value = None # TODO
#                     part_parameter.max_value = parameter['max_value']['value']
#                 part_parameter.text_value = parameter['display_value']   
#             else:
#                 if parameter['nom_value']:
#                     part_parameter.text_value = parameter['nom_value']['value']
#                 else:
#                     part_parameter.text_value = parameter['display_value']   
#             
#     def addDistributorsFromOctopart(self, octopart):
#         octopart_extractor = OctopartExtractor(octopart)
# 
#         if self.part.distributors is None:
#             self.part.distributors = []
# 
#         octopart_distributors = octopart_extractor.ExtractDistributors()
#         for distributor_name in octopart_distributors:
#             part_distributor = next((p for p in self.part.distributors if p.name==distributor_name), None)
#             if part_distributor is None:
#                 try:
#                     distributors = rest.api.find_distributors(name=distributor_name)
#                     if len(distributors)>0:
#                         distributor = distributors[0]
#                     else:
#                         # distributor does not exists, create it
#                         new_distributor = rest.model.DistributorNew()
#                         new_distributor.name = distributor_name
#                         new_distributor.website = octopart_distributors[distributor_name]['website']
#                         new_distributor.allowed = True
#                         new_distributor = rest.api.add_distributor(new_distributor)
#                 except Exception as e:
#                     print_stack()
#                     wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
#                 
#                 part_distributor = rest.model.PartDistributor()
#                 part_distributor.name = distributor_name
#                 part_distributor.offers = []
#                 self.part.distributors.append(part_distributor)
#             
#             for offer in octopart_distributors[distributor_name]['offers']:
#                 part_offer = next((p for p in part_distributor.offers if p.sku==offer['sku'] and p.quantity==offer['quantity'] and p.packaging_unit==offer['packaging_unit']), None)
#                 if part_offer is None:
#                     part_offer = rest.model.PartOffer()
#                     part_distributor.offers.append(part_offer)
#                 part_offer.packaging_unit = offer['packaging_unit']
#                 part_offer.quantity = offer['quantity']
#                 part_offer.min_order_quantity = offer['min_order_quantity']
#                 part_offer.unit_price = offer['unit_price']
#                 part_offer.available_stock = offer['available_stock']
#                 part_offer.packaging = offer['packaging']
#                 part_offer.currency = offer['currency']
#                 part_offer.sku = offer['sku']
#                 part_offer.updated = offer['updated']
#          
#         # Cleanup old offers
#         for distributor in self.part.distributors:
#             offers_to_remove = []
#             for offer in distributor.offers:
#                 utc = pytz.UTC
#                 try:
#                     if offer.updated<utc.localize(datetime.datetime.now()-datetime.timedelta(days=30)):
#                         offers_to_remove.append(offer)
#                 except:
#                     offers_to_remove.append(offer)
#             for offer in offers_to_remove:
#                 distributor.offers.remove(offer)
# 
#         distributors_to_remove = []
#         for distributor in self.part.distributors:
#             if len(distributor.offers)==0:
#                 distributors_to_remove.append(distributor)
#         for distributor in distributors_to_remove:
#             self.part.distributors.remove(distributor)
#     
#     def addManufacturerFromOctopart(self, octopart):
#         octopart_extractor = OctopartExtractor(octopart)
# 
#         reference = octopart_extractor.ExtractReference()
#         manufacturer_name = reference['manufacturer']
#         
#         manufacturer = None 
#         try:
#             manufacturers = rest.api.find_manufacturers(name=manufacturer_name)
#             if len(manufacturers)>0:
#                 manufacturer = manufacturers[0]
#         except:
#             print_stack()
#             wx.MessageBox('%s: error retrieving manufacturer' % (manufacturer_name), 'Warning', wx.OK | wx.ICON_EXCLAMATION)
#         if manufacturer is None:
#             res = wx.MessageBox("Manufacturer '%s' does not exists, create it?" % (manufacturer_name), 'Warning', wx.YES_NO | wx.ICON_QUESTION) 
#             if res==wx.YES:
#                 try:
#                     manufacturer = rest.model.ManufacturerNew()
#                     manufacturer.name = manufacturer_name
#                     manufacturer.website = octopart.item().manufacturer().homepage_url()
#                     manufacturer = rest.api.add_manufacturer(manufacturer)
#                 except:
#                     manufacturer = None
#                     print_stack()
#                     wx.MessageBox('%s: error creating manufacturer' % (manufacturer_name), 'Warning', wx.OK | wx.ICON_ERROR)
#         if manufacturer:
#             if self.part.manufacturers is None:
#                 self.part.manufacturers = []
# 
#             part_manufacturer = next((p for p in self.part.manufacturers if p.name==manufacturer_name), None)
#             if part_manufacturer is None:
#                 part_manufacturer = rest.model.PartManufacturer()
#                 self.part.manufacturers.append(part_manufacturer)
#             part_manufacturer.name = manufacturer.name
#             part_manufacturer.part_name = manufacturer_name
#     
#     def onSelectOctopartFrameOk(self, event):
#         octoparts = event.data
#         if not octoparts:
#             return
# 
#         import_choice = wx.MultiChoiceDialog(self, "Items to import", "Octopart", 
#             ["Parameters", 
#              "Distributors and prices",
#              "Attachements",
#              "Manufacturers"])
#         import_choice.SetSelections([0, 1, 2, 3])
#         if import_choice.ShowModal()!=wx.ID_OK:
#             return
#         choices = import_choice.GetSelections()
#         
#         octopart_parts = []
#         for octopart in octoparts:
#             # convert octopart to part
#             log.debug("octopart:", octopart.json)
#             
#             # update reference
#             self.addReferenceFromOctopart(octopart)
#             
#             if 0 in choices:
#                 self.addParametersFromOctopart(octopart)
#                 
#             if 1 in choices:
#                 self.addDistributorsFromOctopart(octopart)
# 
#             if 3 in choices:
#                 # update manufacturer
#                 self.addManufacturerFromOctopart(octopart)
# 
#         # update part
#         if len(self.part.references)==1:
#             self.part.name = self.part.references[0].name
#             self.part.description = self.part.references[0].description
#         else:
#             self.part.name = self.edit_part_name.Value
#             self.part.description = self.edit_part_description.Value
#             
#         self.SetPart(self.part)

