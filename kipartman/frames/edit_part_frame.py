from dialogs.panel_edit_part import PanelEditPart
from frames.select_footprint_frame import SelectFootprintFrame
from frames.part_parameters_frame import PartParametersFrame
from frames.part_distributors_frame import PartDistributorsFrame
from frames.dropdown_frame import DropdownFrame
from frames.dropdown_dialog import DropdownDialog
from frames.select_octopart_frame import SelectOctopartFrame, EVT_SELECT_OCTOPART_OK_EVENT
import wx.lib.newevent
from api import models
from api.queries import UnitsQuery, UnitPrefixesQuery, DistributorsQuery

EditPartApplyEvent, EVT_EDIT_PART_APPLY_EVENT = wx.lib.newevent.NewEvent()
EditPartCancelEvent, EVT_EDIT_PART_CANCEL_EVENT = wx.lib.newevent.NewEvent()

class EditPartFrame(PanelEditPart): 
    def __init__(self, parent):
        super(EditPartFrame, self).__init__(parent)
        
        self.edit_part_parameters = PartParametersFrame(self.notebook_part)
        self.notebook_part.AddPage(self.edit_part_parameters, "Parameters")
        
        self.edit_part_distributors = PartDistributorsFrame(self.notebook_part)
        self.notebook_part.AddPage(self.edit_part_distributors, "Distributors")

        self.edit_part_manufacturers = wx.Panel(self.notebook_part)
        self.notebook_part.AddPage(self.edit_part_manufacturers, "Manufacturers")

        self.edit_part_attachements = wx.Panel(self.notebook_part)
        self.notebook_part.AddPage(self.edit_part_attachements, "Attachements")

    def SetPart(self, part):
        self.part = part
        self.ShowPart(part)
        self.edit_part_parameters.SetPart(part)
        self.edit_part_distributors.SetPart(part)
    
    def ShowPart(self, part):
        if part:
            self.edit_part_name.Value = part.name
            self.edit_part_description.Value = part.description
            self.edit_part_comment.Value = part.comment
            if part.footprint:
                self.button_part_footprint.Label = part.footprint.name
            else:
                self.button_part_footprint.Label = "<none>"
            self.button_part_footprint.Value = part.footprint
        else:
            self.edit_part_name.Value = ''
            self.edit_part_description.Value = ''
            self.edit_part_comment.Value = ''
            self.button_part_footprint.Label = "<none>"

    def ApplyChanges(self, part):
        self.edit_part_parameters.ApplyChanges(part)
        self.edit_part_distributors.ApplyChanges(part)
#        self.edit_part_manufacturers.ApplyChanges(part)
#        self.edit_part_attachements.ApplyChanges(part)

    def enable(self, enabled=True):
        self.edit_part_name.Enabled = enabled
        self.button_octopart.Enabled = enabled
        self.edit_part_description.Enabled = enabled
        self.button_part_footprint.Enabled = enabled
        self.edit_part_comment.Enabled = enabled
        self.button_part_editApply.Enabled = enabled
        self.button_part_editCancel.Enabled = enabled
        self.edit_part_parameters.enable(enabled)
        self.edit_part_distributors.enable(enabled)
        
    def onButtonPartFootprintClick( self, event ):
        footprint = self.button_part_footprint.Value
        frame = DropdownFrame(self.button_part_footprint, SelectFootprintFrame, footprint)
        frame.Dropdown(self.onSetFootprintCallback)
    
    def onSetFootprintCallback(self, footprint):
        if footprint:
            self.button_part_footprint.Label = footprint.name
        else:
            self.button_part_footprint.Label = "<none>"
        self.button_part_footprint.Value = footprint
        
    def onButtonPartEditApply( self, event ):
        part = self.part
        if not part:
            part = models.Part()
        # set part content
        part.name = self.edit_part_name.Value
        part.description = self.edit_part_description.Value
        part.comment = self.edit_part_comment.Value
        part.footprint = self.button_part_footprint.Value
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
        if spec.metadata().unit():
            try:
                return UnitsQuery(symbol=self.GetUnitSymbol(spec))[0]
            except:
                pass #TODO create unit if not found
        return None
    
    def GetUnitPrefix(self, spec):
        symbol = self.GetUnitPrefixSymbol(spec)
        if spec.metadata().unit():
            try:
                return UnitPrefixesQuery(symbol=symbol)[0]
            except:
                wx.MessageBox('%s: unit prefix unknown' % (symbol), 'Warning', wx.OK | wx.ICON_EXCLAMATION)
        return None
        
    def GetUnitSymbol(self, spec):
        if spec.metadata().unit():
            return spec.metadata().unit().symbol()
        return ""

    def GetUnitPrefixSymbol(self, spec):
        if spec.display_value() is None:
            return ""
        display_value = spec.display_value().split(" ")
        unit = self.GetUnitSymbol(spec)
        if len(display_value)<2:
            return ""
        display_unit = display_value[1]
        prefix = display_unit[:-len(unit)]
        return prefix
    
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
        
        # import parameters
        for spec_name in octopart.item().specs():
            parameter = models.PartParameter()
            spec = octopart.item().specs()[spec_name]
            
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
                distributors = DistributorsQuery(name=distributor_name).get()
                if len(distributors)>0:
                    distributor = distributors[0]
                else:
                    # distributor does not exists, create it
                    distributor = models.Distributor()
                    distributor.name = offer.seller().name()
                    distributor.website = offer.seller().homepage_url()
                    distributor = DistributorsQuery().create(distributor)
            except:
                wx.MessageBox('%s: unknown error retrieving distributor' % (distributor_name), 'Warning', wx.OK | wx.ICON_EXCLAMATION)
            
            # remove distributor prior to add new offers
            self.edit_part_distributors.RemoveDistributor(distributor_name)
            
            for price_name in offer.prices():
                for quantity in offer.prices()[price_name]:
#                    print "--", quantity
                    part_distributor = models.PartDistributor()
                    part_distributor.name = distributor_name
                    part_distributor.distributor = distributor
                    part_distributor.currency = price_name
                    part_distributor.packaging_unit = quantity[0]
                    part_distributor.unit_price = float(quantity[1])
                    part_distributor.sku = offer.sku()
                    self.edit_part_distributors.AddDistributor(part_distributor)
        
        self.ShowPart(self.part)