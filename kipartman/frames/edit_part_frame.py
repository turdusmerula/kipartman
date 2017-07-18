from dialogs.panel_edit_part import PanelEditPart
from frames.select_footprint_frame import SelectFootprintFrame
from frames.part_parameters_frame import PartParametersFrame
from frames.part_distributors_frame import PartDistributorsFrame
from frames.part_manufacturers_frame import PartManufacturersFrame
from frames.dropdown_frame import DropdownFrame
from frames.dropdown_dialog import DropdownDialog
from frames.select_octopart_frame import SelectOctopartFrame, EVT_SELECT_OCTOPART_OK_EVENT
import wx.lib.newevent
import datetime
import re
import rest

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
        
        self.edit_part_distributors = PartDistributorsFrame(self.notebook_part)
        self.notebook_part.AddPage(self.edit_part_distributors, "Distributors")

        self.edit_part_manufacturers = PartManufacturersFrame(self.notebook_part)
        self.notebook_part.AddPage(self.edit_part_manufacturers, "Manufacturers")

        self.edit_part_attachements = wx.Panel(self.notebook_part)
        self.notebook_part.AddPage(self.edit_part_attachements, "Attachements")

    def SetPart(self, part):
        self.part = part
        self.ShowPart(part)
        self.edit_part_parameters.SetPart(part)
        self.edit_part_distributors.SetPart(part)
        self.edit_part_manufacturers.SetPart(part)
        #self.edit_part_attachements.SetPart(part)
        
    def ShowPart(self, part):
        if part:
            self.edit_part_name.Value = NoneValue(part.name, "")
            self.edit_part_description.Value = NoneValue(part.description, "")
            self.edit_part_comment.Value = NoneValue(part.comment, '')
            if part.footprint:
                self.button_part_footprint.Label = NoneValue(part.footprint.name, "")
            else:
                self.button_part_footprint.Label = "<none>"
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
        self.button_part_model.Enabled = enabled
        self.edit_part_comment.Enabled = enabled
        self.button_part_editApply.Enabled = enabled
        self.button_part_editCancel.Enabled = enabled
        self.edit_part_parameters.enable(enabled)
        self.edit_part_distributors.enable(enabled)
        self.edit_part_manufacturers.enable(enabled)
        
    def onButtonPartFootprintClick( self, event ):
        footprint = self.part.footprint
        frame = DropdownFrame(self.button_part_footprint, SelectFootprintFrame, footprint)
        frame.Dropdown(self.onSetFootprintCallback)
    
    def onSetFootprintCallback(self, footprint):
        if footprint:
            self.button_part_footprint.Label = footprint.name
        else:
            self.button_part_footprint.Label = "<none>"
        self.part.footprint = footprint
        
    def onButtonPartEditApply( self, event ):
        part = self.part
        if not part:
            part = rest.model.PartNew()
        if part.name!=part.octopart:
            part.octopart = None
            
        # set part content
        part.name = str(self.edit_part_name.Value)
        part.description = str(self.edit_part_description.Value)
        part.comment = str(self.edit_part_comment.Value)
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

    def GetUnit(self, spec):
        symbol = self.GetUnitSymbol(spec)
        if spec.metadata().unit():
            try:
                return rest.api.find_units(symbol=symbol)[0]
            except Exception as e:
                wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
#            except Exception as e:
                #TODO create unit if not found
#                wx.MessageBox('%s: unit unknown' % (symbol), 'Warning', wx.OK | wx.ICON_EXCLAMATION)

        return None
    
    def GetUnitPrefix(self, spec):
        symbol = self.GetUnitPrefixSymbol(spec)
        if spec.metadata().unit():
            try:
#                print "---", symbol, rest.api.find_unit_prefixes(symbol=symbol)[0]
                return rest.api.find_unit_prefixes(symbol=symbol)[0]
            except Exception as e:
                wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
#            except:
#                wx.MessageBox('%s: unit prefix unknown' % (symbol), 'Warning', wx.OK | wx.ICON_EXCLAMATION)
        return None
        
    def GetUnitSymbol(self, spec):
        if spec.metadata().unit():
            return spec.metadata().unit().symbol().encode('utf8')
        return ""

    def GetUnitPrefixSymbol(self, spec):
        if spec.display_value() is None:
            return ""
        display_value = spec.display_value().split(" ")
        unit = self.GetUnitSymbol(spec)
        if len(display_value)<2:
            return ""   # there is only a value, no unit
        display_unit = display_value[1]
        # filter non alpha chars
        display_unit = re.sub('[ ,.;]', '', display_unit)
        prefix = display_unit[:-len(unit)]
        return prefix.encode('utf8')
    
    def GetPrefixedValue(self, value, prefix):
        if prefix is None:
            return float(value)
        return float(value)/float(prefix.power)
    
    def onSelectOctopartFrameOk(self, event):
        octopart = event.data
        if not octopart:
            return

        # convert octopart to part values
        print "octopart:", octopart.json
        
        # import part fields
        self.part.name = octopart.item().mpn()
        self.part.description = octopart.snippet()
        
        # set field octopart to indicatethat part was imported from octopart
        self.part.octopart = octopart.item().mpn()
        self.part.updated = datetime.datetime.now()
        
        # import parameters
        for spec_name in octopart.item().specs():
            parameter = rest.model.PartParameter()
            spec = octopart.item().specs()[spec_name]
            print "spec: ", spec.json
            parameter.name = spec_name
            parameter.description = spec.metadata().name()
            parameter.unit = self.GetUnit(spec)
            parameter.nom_prefix = self.GetUnitPrefix(spec)
            parameter.nom_value = None
            parameter.text_value = None
            if spec.value() and len(spec.value())>0:
                try:
                    if parameter.unit:
                        parameter.nom_value = self.GetPrefixedValue(spec.value()[0], parameter.nom_prefix)
                    else:
                        parameter.nom_value = float(spec.value()[0])
                    parameter.numeric = True
                except:
                    parameter.text_value = spec.value()[0]
                    parameter.numeric = False
            if spec.min_value():
                try:
                    if parameter.unit:
                        parameter.min_value = self.GetPrefixedValue(spec.min_value(), parameter.nom_prefix)
                    else:
                        parameter.min_value = float(spec.value()[0])
                    parameter.min_prefix = parameter.nom_prefix
                    parameter.numeric = True
                except:
                    parameter.numeric = False
            else:
                parameter.min_value = None
            if spec.max_value():
                try:
                    if parameter.unit:
                        parameter.max_value = self.GetPrefixedValue(spec.max_value(), parameter.nom_prefix)
                    else:
                        parameter.max_value = float(spec.value()[0])
                    parameter.numeric = True
                    parameter.max_prefix = parameter.nom_prefix
                except:
                    parameter.numeric = False
            else:
                parameter.max_value = None
            
            self.edit_part_parameters.AddParameter(parameter)

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
                    distributor = rest.api.add_distributor(distributor)
            except Exception as e:
                wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
#            except Exception as e:
#                wx.MessageBox('%s: unknown error retrieving distributor' % (distributor_name), 'Warning', wx.OK | wx.ICON_EXCLAMATION)
            
            # remove all offers from distributor prior to add new offers
            self.edit_part_distributors.RemoveDistributor(distributor_name)
            
            for price_name in offer.prices():
                for quantity in offer.prices()[price_name]:
                    part_offer = rest.model.PartDistributor()
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
            manufacturers = ManufacturersQuery(name=manufacturer_name).get()
            if len(manufacturers)>0:
                manufacturer = manufacturers[0]
            else:
                # distributor does not exists, create it
                manufacturer = models.Manufacturer()
                manufacturer.name = manufacturer_name
                manufacturer.website = octopart.item().manufacturer().homepage_url()
                manufacturer = ManufacturersQuery().create(manufacturer)
        except:
            wx.MessageBox('%s: unknown error retrieving manufacturer' % (manufacturer_name), 'Warning', wx.OK | wx.ICON_EXCLAMATION)
        # remove manufacturer prior to add new manufacturer
        self.edit_part_manufacturers.RemoveManufacturer(manufacturer_name)
        # add new manufacturer
        part_manufacturer = models.PartManufacturer()
        part_manufacturer.manufacturer = manufacturer
        part_manufacturer.part_name = self.part.name
        self.edit_part_manufacturers.AddManufacturer(part_manufacturer)

        self.ShowPart(self.part)

