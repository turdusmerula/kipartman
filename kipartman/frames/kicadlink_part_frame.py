from dialogs.panel_kicadlink_part import PanelKicadLinkPart
from frames.select_footprint_frame import SelectFootprintFrame
from frames.select_model_frame import SelectModelFrame
from frames.part_parameters_frame import PartParametersFrame
from frames.part_ecaddata_frame import PartEcadDataFrame
from frames.part_distributors_frame import PartDistributorsFrame
from frames.part_manufacturers_frame import PartManufacturersFrame
from frames.part_attachements_frame import PartAttachementsFrame
from frames.part_storages_frame import PartStoragesFrame
from frames.dropdown_frame import DropdownFrame
from frames.dropdown_dialog import DropdownDialog
from frames.select_octopart_frame import SelectOctopartFrame, EVT_SELECT_OCTOPART_OK_EVENT
import wx.lib.newevent
from wx.lib.pubsub import pub
import datetime, logging
import re
import rest
from octopart.extractor import OctopartExtractor
import kicadGUI.KicadEeschemaAutomation as KEA

EditPartApplyEvent, EVT_EDIT_PART_APPLY_EVENT = wx.lib.newevent.NewEvent()
EditPartCancelEvent, EVT_EDIT_PART_CANCEL_EVENT = wx.lib.newevent.NewEvent()

def log(msg):
    if 'logging' in globals(): logging.debug(
        "{:%H:%M:%S.%f}:{}".format(
            datetime.datetime.now(),
            msg
        ))


def NoneValue(value, default):
    if value:
        return value
    return default

class KicadLinkPartFrame(PanelKicadLinkPart): 
    def __init__(self, parent):
        super(KicadLinkPartFrame, self).__init__(parent)
        #TODO Remove Notebook leaves we don't require
        #TODO Remove methods not required
        # self.edit_part_parameters = PartParametersFrame(self.notebook_part)
        # self.notebook_part.AddPage(self.edit_part_parameters, "Parameters")
        
        # self.edit_part_ecaddata = PartEcadDataFrame(self.notebook_part)
        # self.notebook_part.AddPage(self.edit_part_ecaddata, "ECADdata")
        
        # self.edit_part_distributors = PartDistributorsFrame(self.notebook_part)
        # self.notebook_part.AddPage(self.edit_part_distributors, "Distributors")

        # self.edit_part_manufacturers = PartManufacturersFrame(self.notebook_part)
        # self.notebook_part.AddPage(self.edit_part_manufacturers, "Manufacturers")

        # self.edit_part_storages = PartStoragesFrame(self.notebook_part)
        # self.notebook_part.AddPage(self.edit_part_storages, "Storages locations")

        # self.edit_part_attachements = PartAttachementsFrame(self.notebook_part)
        # self.notebook_part.AddPage(self.edit_part_attachements, "Attachements")

        #
        #Subscribe to the Kicad GUI event monitor announcements
        pub.subscribe(self.updateFromKicad, "kicad.change.status")

        self.compProperties = KEA.KicadEeschemaComponentProperties()
        self.compProperties.connect()

    def updateFromKicad(self, listen_to):
        if listen_to == 'Eeschema.Foreground':
            self.m_checkBoxKcEeschemaRunning.SetValue(True)
        elif listen_to == 'Eeschema.Background':
            self.m_checkBoxKcEeschemaRunning.SetValue(False)

        if 'Eeschema.ComponentProperties.' in listen_to:
            self.m_checkBoxComponentEdit.SetValue(
                {'Entered':True
                , 'Exited':False
                }[listen_to.split('.')[-1]]
            )
            if listen_to=='Eeschema.ComponentProperties.Entered':
                self.m_checkBoxKcEeschemaRunning.SetValue(True) #HACK, status not always displayed, dependent on window switch,
                #TODO: # maybe this above hack should be in the kicad_gui_monitor
                log('-----------------000000000000000----------Trying to fetch values')
                if self.compProperties.windowComponentProperties():
                    log('-----------------000000000000000----------Trying to fetch values ----------- Window Detected')
                    self.compProperties.refresh()
                    log('-----------------000000000000000----------Trying to fetch values ----------- Refreshed')

                    log('-----------------000000000000000----------Trying to fetch values :FOUND {} : {}'.format(
                        self.compProperties.get_field('Value'),
                        self.compProperties.get_field('Footprint')
                    ))
                    self.kicad_part_value.Value = self.compProperties.get_field('Value')
                    self.kicad_part_reference.Value = self.compProperties.get_field('Reference')
                    self.kicad_part_id.Value = self.compProperties.componentID
                    self.kicad_part_footprint.Value = self.compProperties.get_field('Footprint')
                    self.kicad_part_SKU.Value = self.compProperties.get_field('SKU')
                    self.kicad_part_MPN.Value = self.compProperties.get_field('MPN')
                    self.kicad_part_MFR.Value = self.compProperties.get_field('MFR')
                    self.kicad_part_SPN.Value = self.compProperties.get_field('SPN')
                    self.kicad_part_SPR.Value = self.compProperties.get_field('SPR')

                    # initiate Search
                    #if self.kicad_autosearch checkbox checked #TODO: implement autosearch control
                    if self.checkBox_search_auto.GetValue():
                        self.search_format()


                else:
                    pass
            else:
                pass
        if 'Eeschema.ComponentAdd.' in listen_to:
            self.m_checkBoxEeschemaComponentAdd.SetValue(
               {'Entered':True
                , 'Exited':False
                }[listen_to.split('.')[-1]]
            )
            pass
            
        log("Kicadlink_part_frame----XXXXXX-------XXXXXXX--------XXXXXX-------SUBSCRIBED EVENT RECIEVED:{}".format(listen_to))




    def SetPart(self, part):
        self.part = part
        self.ShowPart(part)
        self.edit_part_parameters.SetPart(part)
        self.edit_part_ecaddata.SetPart(part)
        self.edit_part_distributors.SetPart(part)
        self.edit_part_manufacturers.SetPart(part)
        self.edit_part_storages.SetPart(part)
        self.edit_part_attachements.SetPart(part)
        
    def ShowPart(self, part):
        if part:
            self.edit_part_name.Value = NoneValue(part.name, "")
            self.edit_part_description.Value = NoneValue(part.description, "")
            self.edit_part_comment.Value = NoneValue(part.comment, '')
            if part.footprint:
                self.button_part_footprint.Label = NoneValue(part.footprint.name, "")
            else:
                self.button_part_footprint.Label = "<none>"
            if part.model:
                self.button_part_model.Label = NoneValue(part.model.name, "")
            else:
                self.button_part_model.Label = "<none>"
        else:
            self.edit_part_name.Value = ''
            self.edit_part_description.Value = ''
            self.edit_part_comment.Value = ''
            self.button_part_footprint.Label = "<none>"

    def enable(self, enabled=True):
        self.edit_part_comment.Enabled = enabled
        #TODO: decide what to do with this?
        self.button_part_editApply.Enabled = enabled
        self.button_part_editCancel.Enabled = enabled
        #TODO: Remove
        # self.edit_part_name.Enabled = enabled

        # self.button_octopart.Enabled = enabled
        # self.edit_part_description.Enabled = enabled
        # self.button_part_footprint.Enabled = enabled
        # self.button_part_model.Enabled = enabled

        # self.edit_part_parameters.enable(enabled)
        # self.edit_part_distributors.enable(enabled)
        # self.edit_part_manufacturers.enable(enabled)
        # self.edit_part_storages.enable(enabled)
        # self.edit_part_attachements.enable(enabled)

    #TODO:Remove        
    # def onButtonPartFootprintClick( self, event ):
    #     footprint = self.part.footprint
    #     frame = DropdownFrame(self.button_part_footprint, SelectFootprintFrame, footprint)
    #     frame.Dropdown(self.onSetFootprintCallback)
    
    # def onSetFootprintCallback(self, footprint):
    #     if footprint:
    #         self.button_part_footprint.Label = footprint.name
    #     else:
    #         self.button_part_footprint.Label = "<none>"
    #     self.part.footprint = footprint
        
    # def onButtonPartModelClick( self, event ):
    #     model = self.part.model
    #     frame = DropdownFrame(self.button_part_footprint, SelectModelFrame, model)
    #     frame.Dropdown(self.onSetModelCallback)
    
    # def onSetModelCallback(self, model):
    #     if model:
    #         self.button_part_model.Label = model.name
    #     else:
    #         self.button_part_model.Label = "<none>"
    #     self.part.model = model

    #TODO: Decide what to do with onButtonPartEditApply
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

    #TODO: Decide what to do with onButtonPartEditCancel
    def onButtonPartEditCancel( self, event ):
        event = EditPartCancelEvent()
        wx.PostEvent(self, event)

    def onButtonKicadLinkPartSelect(self, event):
        #TODO: have this event triggered by selecting a part in the treeview
        selected_part = self.TopLevelParent.partsframe.panel_edit_part.edit_part_name #TODO: improve finding this control
        log('Selected Item:{}'.format(selected_part.Value))
        if self.checkBox_update_value.GetValue():
            self.kicad_part_value_new.Value = self.kicad_part_value.Value #TODO: SOMEFUNCtogetValue(selected_part.Value)
            pass #TODO : Implement value update

        if self.checkBox_update_footprint.GetValue():
            #self.kicad_part_footprint_new.Value = SOMEFUNCTIONof(selected_part) # TODO: Get from ECADdata
            self.kicad_part_footprint_new.Value = self.kicad_part_footprint.Value #TODO: SOMEFUNCtogetFootprint(selected_part.Value)

        if self.checkBox_update_SKU.GetValue():
            self.kicad_part_SKU_new.Value = selected_part.Value

        if self.checkBox_update_MPN.GetValue():
            self.kicad_part_MPN_new.Value = selected_part.Value

        if self.checkBox_update_MFR.GetValue():
            #TODO: Detect MFR
            # self.kicad_part_MFR_new.Value = selected_part.Value
            pass

        if self.checkBox_update_SPN.GetValue():
            pass #TODO: should not really have SPN in schematic, Decide what ?
        if self.checkBox_update_SPR.GetValue():
            pass #TODO: should not really have SPR in schematic, Decide what ?
        pass

    def onButtonKicadLinkFieldsUpdateClick(self, event):
        #TODO: 17W50 Suppress Receiving GUI events Whilst updating, Put up a dialog
        #TODO: Furtherimplement selection
        selected_part = self.TopLevelParent.partsframe.panel_edit_part.edit_part_name #TODO: improve finding this control
        log('Selected Item:{}'.format(selected_part.Value))
        if self.checkBox_update_value.GetValue() and len(self.kicad_part_value_new.Value)!=0:
            self.compProperties.update_field('Value', self.kicad_part_value_new.Value )
            pass #TODO : Implement value update

        if self.checkBox_update_footprint.GetValue() and len(self.kicad_part_footprint_new.Value)!=0:
            self.compProperties.update_field('Footprint', self.kicad_part_footprint_new.Value )

        if self.checkBox_update_SKU.GetValue() and len(self.kicad_part_SKU_new.Value)!=0:
            self.compProperties.update_field('SKU', self.kicad_part_SKU_new.Value )

        if self.checkBox_update_MPN.GetValue() and len(self.kicad_part_MPN_new.Value)!=0:
            self.compProperties.update_field('MPN', self.kicad_part_MPN_new.Value )


        if self.checkBox_update_SPN.GetValue() and len(self.kicad_part_SPN_new.Value)!=0:
            pass #TODO: should not really have SPN in schematic, Decide what ?
        if self.checkBox_update_SPR.GetValue() and len(self.kicad_part_SPR_new.Value)!=0:
            pass #TODO: should not really have SPR in schematic, Decide what ?
        pass

    def onButtonKicadLinkComponentSearchClick(self, event):
        self.search_format()

    def search_format(self):
            if self.checkBox_search_value.GetValue(): self.search('Value')
            elif self.checkBox_search_SKU.GetValue(): self.search('SKU')
            elif self.checkBox_search_MPN.GetValue(): self.search('MPN')
            elif self.checkBox_search_SPN.GetValue(): self.search('SPN')

            else:
                pass #TODO:implement other searches, including multelement and refactor this into a more generic serch handler possibly fuzzy or best match

    def search(self,fieldName):
                search_parts = self.TopLevelParent.partsframe.search_parts #TODO: improve finding this control
                search_parts.SetValue(self.compProperties.get_field(fieldName))
                evt = wx.PyCommandEvent(wx.EVT_TEXT_ENTER.typeId, search_parts.GetId())
                wx.PostEvent(search_parts, evt)


    #TODO: Remove
    # def onButtonOctopartClick( self, event ):
    #     # create an octopart frame
    #     # dropdown frame
    #     dropdown = DropdownDialog(self.button_octopart, SelectOctopartFrame, self.edit_part_name.Value)
    #     dropdown.panel.Bind( EVT_SELECT_OCTOPART_OK_EVENT, self.onSelectOctopartFrameOk )
    #     dropdown.Dropdown()

    
    # def onSelectOctopartFrameOk(self, event):
    #     octopart = event.data
    #     if not octopart:
    #         return

    #     # convert octopart to part values
    #     print "octopart:", octopart.json
    #     octopart_extractor = OctopartExtractor(octopart)
        
    #     # import part fields
    #     self.part.name = octopart.item().mpn()
    #     self.part.description = octopart.snippet()
    #     # set field octopart to indicatethat part was imported from octopart
    #     self.part.octopart = octopart.item().mpn()
    #     self.part.octopart_uid = octopart.item().uid()
    #     self.part.updated = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        
    #     # import parameters
    #     for spec_name in octopart.item().specs():
    #         parameter = octopart_extractor.ExtractParameter(spec_name)            
    #         self.edit_part_parameters.AddParameter(parameter)

    #     # remove all offers from distributor prior to add new offers
    #     for offer in octopart.item().offers():
    #         distributor_name = offer.seller().name()
    #         self.edit_part_distributors.RemoveDistributor(distributor_name)

    #     # import distributors
    #     for offer in octopart.item().offers():
            
    #         distributor_name = offer.seller().name()
    #         distributor = None
    #         try:
    #             distributors = rest.api.find_distributors(name=distributor_name)
    #             if len(distributors)>0:
    #                 distributor = distributors[0]
    #             else:
    #                 # distributor does not exists, create it
    #                 distributor = rest.model.DistributorNew()
    #                 distributor.name = offer.seller().name()
    #                 distributor.website = offer.seller().homepage_url()
    #                 distributor.allowed = True
    #                 distributor = rest.api.add_distributor(distributor)
    #         except Exception as e:
    #             wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
                        
    #         for price_name in offer.prices():
    #             for quantity in offer.prices()[price_name]:
    #                 part_offer = rest.model.PartOffer()
    #                 part_offer.name = distributor_name
    #                 part_offer.distributor = distributor
    #                 part_offer.currency = price_name
    #                 if offer.moq():
    #                     part_offer.packaging_unit = offer.moq()
    #                 else:
    #                     part_offer.packaging_unit = 1
    #                 part_offer.quantity = quantity[0]
    #                 part_offer.unit_price = float(quantity[1])
    #                 part_offer.sku = offer.sku()
    #                 self.edit_part_distributors.AddOffer(part_offer)
        
    #     # import manufacturer
    #     manufacturer_name = octopart.item().manufacturer().name()
    #     manufacturer = None
    #     try:
    #         manufacturers = rest.api.find_manufacturers(name=manufacturer_name)
    #         if len(manufacturers)>0:
    #             manufacturer = manufacturers[0]
    #         else:
    #             # distributor does not exists, create it
    #             manufacturer = rest.model.ManufacturerNew()
    #             manufacturer.name = manufacturer_name
    #             manufacturer.website = octopart.item().manufacturer().homepage_url()
    #             manufacturer = rest.api.add_manufacturer(manufacturer)

    #         # remove manufacturer prior to add new manufacturer
    #         self.edit_part_manufacturers.RemoveManufacturer(manufacturer_name)

    #         # add new manufacturer
    #         part_manufacturer = rest.model.PartManufacturer()
    #         part_manufacturer.name = manufacturer.name
    #         part_manufacturer.part_name = self.part.name
    #         self.edit_part_manufacturers.AddManufacturer(part_manufacturer)
    #     except:
    #         wx.MessageBox('%s: unknown error retrieving manufacturer' % (manufacturer_name), 'Warning', wx.OK | wx.ICON_EXCLAMATION)

    #     self.ShowPart(self.part)

