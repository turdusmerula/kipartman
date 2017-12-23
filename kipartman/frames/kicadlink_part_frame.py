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
        self.kicadGUImonitorProcess = True 
        self.compProperties = KEA.KicadEeschemaComponentProperties()
        self.compProperties.connect()

    def updateFromKicad(self, listen_to):
        if self.kicadGUImonitorProcess:
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

                        #Reset the new field to prevent erroneous carryover
                        self.kicad_part_value_new.Value = ''
                        self.kicad_part_footprint_new.Value = ''
                        self.kicad_part_model_new.Value = ''
                        self.kicad_part_SKU_new.Value = ''
                        self.kicad_part_MPN_new.Value = ''
                        self.kicad_part_MFR_new.Value = ''
                        self.kicad_part_SPN_new.Value = ''
                        self.kicad_part_SPR_new.Value = ''



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

    def onButtonKicadLinkPartSelect(self, event):
        #TODO: have this event triggered by selecting a part in the treeview
        selected_part = self.TopLevelParent.partsframe.panel_edit_part.edit_part_name #TODO: improve finding this control
        log('Selected Item:{}'.format(selected_part.Value))
        if self.checkBox_update_value.GetValue():
            self.kicad_part_value_new.Value = self.kicad_part_value.Value #TODO: SOMEFUNCtogetValue(selected_part.Value)
            pass #TODO : Implement value update

        if self.checkBox_update_footprint.GetValue():
            #self.kicad_part_footprint_new.Value = SOMEFUNCTIONof(selected_part) # TODO: Get footprint from ECADdata, for now just copy existing footprint for manual change
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
        self.kicadGUImonitorProcess = False 
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
        self.kicadGUImonitorProcess = True
        self.compProperties.refresh()
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

