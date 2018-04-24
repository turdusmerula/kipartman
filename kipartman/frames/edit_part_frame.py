from dialogs.panel_edit_part import PanelEditPart
from frames.select_footprint_frame import SelectFootprintFrame
from frames.select_symbol_frame import SelectSymbolFrame
from frames.part_parameters_frame import PartParametersFrame
from frames.part_distributors_frame import PartDistributorsFrame
from frames.part_manufacturers_frame import PartManufacturersFrame
from frames.part_attachements_frame import PartAttachementsFrame
from frames.part_storages_frame import PartStoragesFrame
from frames.part_preview_data_frame import PartPreviewDataFrame
from frames.dropdown_frame import DropdownFrame
from frames.dropdown_dialog import DropdownDialog
from frames.select_octopart_frame import SelectOctopartFrame, EVT_SELECT_OCTOPART_OK_EVENT
import wx.lib.newevent
import datetime
import re
import rest
from octopart.extractor import OctopartExtractor
import os

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

    def SetPart(self, part):
        self.part = part
        self.ShowPart(part)
        self.edit_part_parameters.SetPart(part)
        self.edit_part_distributors.SetPart(part)
        self.edit_part_manufacturers.SetPart(part)
        self.edit_part_storages.SetPart(part)
        self.edit_part_attachements.SetPart(part)
        self.edit_part_preview_data.SetPart(part)
        
    def ShowPart(self, part):
        if part:
            self.edit_part_name.Value = NoneValue(part.name, "")
            self.edit_part_description.Value = NoneValue(part.description, "")
            self.edit_part_comment.Value = NoneValue(part.comment, '')
            if part.footprint:
                self.button_part_footprint.Label = os.path.basename(part.footprint.source_path).replace(".kicad_mod", "")
            else:
                self.button_part_footprint.Label = "<none>"
            if part.symbol:
                self.button_part_symbol.Label = os.path.basename(part.symbol.source_path).replace(".mod", "")
            else:
                self.button_part_symbol.Label = "<none>"
        else:
            self.edit_part_name.Value = ''
            self.edit_part_description.Value = ''
            self.edit_part_comment.Value = ''
            self.button_part_footprint.Label = "<none>"

    def enable(self, enabled=True):
        self.edit_part_name.Enabled = enabled
        self.button_octopart.Enabled = enabled
        self.edit_part_description.Enabled = enabled
        self.button_part_footprint.Enabled = enabled
        self.button_part_symbol.Enabled = enabled
        self.edit_part_comment.Enabled = enabled
        self.button_part_editApply.Enabled = enabled
        self.button_part_editCancel.Enabled = enabled
        self.edit_part_parameters.enable(enabled)
        self.edit_part_distributors.enable(enabled)
        self.edit_part_manufacturers.enable(enabled)
        self.edit_part_storages.enable(enabled)
        self.edit_part_attachements.enable(enabled)
        
    def onButtonPartFootprintClick( self, event ):
        footprint = self.part.footprint
        frame = DropdownFrame(self.button_part_footprint, SelectFootprintFrame, footprint)
        frame.Dropdown(self.onSetFootprintCallback)
    
    def onSetFootprintCallback(self, footprint):
        if footprint:
            self.button_part_footprint.Label = os.path.basename(footprint.source_path).replace('.kicad_mod', '')
        else:
            self.button_part_footprint.Label = "<none>"
        self.part.footprint = footprint
        
    def onButtonPartSymbolClick( self, event ):
        symbol = self.part.symbol
        frame = DropdownFrame(self.button_part_footprint, SelectSymbolFrame, symbol)
        frame.Dropdown(self.onSetSymbolCallback)
    
    def onSetSymbolCallback(self, symbol):
        if symbol:
            self.button_part_symbol.Label = os.path.basename(symbol.source_path).replace('.mod', '')
        else:
            self.button_part_symbol.Label = "<none>"
        self.part.symbol = symbol

    def onButtonPartEditApply( self, event ):
        part = self.part
        if not part:
            part = rest.model.PartNew()
        if part.name!=part.octopart:
            part.octopart = None
            
        # set part content
        part.name = self.edit_part_name.Value
        part.description = self.edit_part_description.Value
        part.comment = self.edit_part_comment.Value
        # send result event
        event = EditPartApplyEvent(data=part)
        wx.PostEvent(self, event)
        
    def onButtonPartEditCancel( self, event ):
        event = EditPartCancelEvent()
        wx.PostEvent(self, event)


    def onButtonOctopartClick( self, event ):
        # create an octopart frame
        # dropdown frame
        dropdown = DropdownDialog(self.button_octopart, SelectOctopartFrame, self.edit_part_name.Value)
        dropdown.panel.Bind( EVT_SELECT_OCTOPART_OK_EVENT, self.onSelectOctopartFrameOk )
        dropdown.Dropdown()

    
    def onSelectOctopartFrameOk(self, event):
        octopart = event.data
        if not octopart:
            return

        # convert octopart to part values
        print "octopart:", octopart.json
        octopart_extractor = OctopartExtractor(octopart)

        # TODO: THis looks something similar to def octopart_to_part(self, octopart, part): in parts_frame \
        # explore if this can be rationalized under module octopart. \
        # The code is complex, there could be change sync issues
        
        # import part fields
        self.part.name = octopart.item().mpn()
        self.part.description = octopart.snippet()
        # set field octopart to indicatethat part was imported from octopart
        self.part.octopart = octopart.item().mpn()
        self.part.octopart_uid = octopart.item().uid()
        self.part.updated = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # import parameters
        for spec_name in octopart.item().specs():
            parameter = octopart_extractor.ExtractParameter(spec_name)            
            self.edit_part_parameters.AddParameter(parameter)

        # remove all offers from distributor prior to add new offers
        for offer in octopart.item().offers():
            distributor_name = offer.seller().name()
            self.edit_part_distributors.RemoveDistributor(distributor_name)

        # import distributors
        for offer in octopart.item().offers():
            
            distributor_name = offer.seller().name()
            distributor = None
            try:
                distributors = rest.api.find_distributors(name=distributor_name)
                if len(distributors)>0:
                    distributor = distributors[0]
                else:
                    # distributor does not exists, create it
                    distributor = rest.model.DistributorNew()
                    distributor.name = offer.seller().name()
                    distributor.website = offer.seller().homepage_url()
                    distributor.allowed = True
                    distributor = rest.api.add_distributor(distributor)
            except Exception as e:
                wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
                        
            for price_name in offer.prices():
                for quantity in offer.prices()[price_name]:
                    part_offer = rest.model.PartOffer()
                    part_offer.name = distributor_name
                    part_offer.distributor = distributor
                    part_offer.currency = price_name
                    if offer.moq():
                        part_offer.packaging_unit = offer.moq()
                    else:
                        part_offer.packaging_unit = 1
                    part_offer.quantity = quantity[0]
                    part_offer.unit_price = float(quantity[1])
                    part_offer.sku = offer.sku()
                    self.edit_part_distributors.AddOffer(part_offer)
        
        # import manufacturer
        manufacturer_name = octopart.item().manufacturer().name()
        manufacturer = None
        try:
            manufacturers = rest.api.find_manufacturers(name=manufacturer_name)
            if len(manufacturers)>0:
                manufacturer = manufacturers[0]
            else:
                # distributor does not exists, create it
                manufacturer = rest.model.ManufacturerNew()
                manufacturer.name = manufacturer_name
                manufacturer.website = octopart.item().manufacturer().homepage_url()
                manufacturer = rest.api.add_manufacturer(manufacturer)

            # remove manufacturer prior to add new manufacturer
            self.edit_part_manufacturers.RemoveManufacturer(manufacturer_name)

            # add new manufacturer
            part_manufacturer = rest.model.PartManufacturer()
            part_manufacturer.name = manufacturer.name
            part_manufacturer.part_name = self.part.name
            self.edit_part_manufacturers.AddManufacturer(part_manufacturer)
        except:
            wx.MessageBox('%s: unknown error retrieving manufacturer' % (manufacturer_name), 'Warning', wx.OK | wx.ICON_EXCLAMATION)

        self.ShowPart(self.part)

