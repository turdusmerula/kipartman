from dialogs.dialog_edit_part_offer import DialogEditPartOffer
import wx
from helper.exception import print_stack
import api.data.distributor
import api.data.part_offer
from helper import colors

# TODO: switch to a list for currency
class EditPartOfferFrame(DialogEditPartOffer):
    def __init__(self, parent): 
        super(EditPartOfferFrame, self).__init__(parent)
        self.loadDistributors()

        self.part = None
        self.distributor = None
        self.part_offer = None

    def loadDistributors(self):
        self.distributors = [None]
        for distributor in api.data.distributor.find():
            self.distributors.append(distributor)
        choices = ["<none>"]
        for distributor in self.distributors[1:]:
            choices.append(distributor.name)
        self.choice_distributor.SetItems(choices)

    def AddPartOffer(self, part, distributor=None, currency=None, sku=None, packaging=None):
        self.Title = "Add distributor"
        self.part = part
        self.part_offer = api.data.part_offer.create(self.part)
 
        self.choice_distributor.Enabled = True

        if distributor is None:
            self.choice_distributor.SetSelection(0)
        else:
            self.choice_distributor.SetSelection(distributor.id)
        if packaging is None:
            self.edit_part_offer_packaging.Value = ""
        else:
            self.edit_part_offer_packaging.Value = packaging
        self.edit_part_offer_packaging_unit.Value = '1'
        self.edit_part_offer_quantity.Value = '1'
        self.edit_part_offer_unit_price.Value = '0'
        if currency is None:
            self.edit_part_offer_currency.Value = 'USD'
        else:
            self.edit_part_offer_currency.Value = currency
        if sku is None:
            self.edit_part_offer_sku.Value = ''
        else:
            self.edit_part_offer_sku.Value = sku
            
        result = self.ShowModal()
        if result==wx.ID_OK:
            return self.part_offer
        return None

    def EditPartOffer(self, part, part_offer):
        self.Title = "Edit distributor"
        self.part = part
        self.part_offer = part_offer

        self.choice_distributor.Enabled = False

        if part_offer.distributor:
            self.choice_distributor.SetSelection(self.choice_distributor.FindString(self.part_offer.distributor.name))
        else:
            self.choice_distributor.SetSelection(0)
        self.edit_part_offer_packaging.Value = part_offer.packaging
        self.edit_part_offer_packaging_unit.Value = str(part_offer.packaging_unit)
        self.edit_part_offer_quantity.Value = str(part_offer.quantity)
        self.edit_part_offer_unit_price.Value = str(part_offer.unit_price)
        self.edit_part_offer_currency.Value = str(part_offer.currency)
        self.edit_part_offer_sku.Value = str(part_offer.sku)

        result = self.ShowModal()
        if result==wx.ID_OK:
            return self.part_offer
        return None

    def _check(self):
        error = False
        
        if self.choice_distributor.GetSelection()==0:
            error = True
            self.choice_distributor.SetBackgroundColour( colors.RED_ERROR )
        else:
            self.choice_distributor.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        
        try:
            self.edit_part_offer_packaging_unit.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
            value = int(self.edit_part_offer_packaging_unit.Value)
            if value<=0:
                error = True
                self.edit_part_offer_packaging_unit.SetBackgroundColour( colors.RED_ERROR )
        except Exception as e:
            error = True
            self.edit_part_offer_packaging_unit.SetBackgroundColour( colors.RED_ERROR )
            
        try:
            self.edit_part_offer_quantity.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
            value = int(self.edit_part_offer_quantity.Value)
            if value<=0:
                error = True
                self.edit_part_offer_quantity.SetBackgroundColour( colors.RED_ERROR )
        except Exception as e:
            error = True
            self.edit_part_offer_quantity.SetBackgroundColour( colors.RED_ERROR )
        
        try:
            self.edit_part_offer_unit_price.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
            value = float(self.edit_part_offer_unit_price.Value)
            if value<=0:
                error = True
                self.edit_part_offer_unit_price.SetBackgroundColour( colors.RED_ERROR )
        except Exception as e:
            error = True
            self.edit_part_offer_unit_price.SetBackgroundColour( colors.RED_ERROR )

        if error:
            self.button_part_offer_editApply.Enabled = False
        else:
            self.button_part_offer_editApply.Enabled = True

    def onButtonPartOfferEditApply( self, event ):
        try:
            if self.choice_distributor.GetSelection()==0:
                raise Exception("Missing distributor")
            else:
                self.part_offer.distributor = self.distributors[self.choice_distributor.GetSelection()] 
            
            self.part_offer.packaging = self.edit_part_offer_packaging.Value
            self.part_offer.packaging_unit = int(self.edit_part_offer_packaging_unit.Value)
            self.part_offer.quantity = int(self.edit_part_offer_quantity.Value)
            self.part_offer.unit_price = float(self.edit_part_offer_unit_price.Value)
            self.part_offer.currency = self.edit_part_offer_currency.Value
            self.part_offer.sku = self.edit_part_offer_sku.Value

            self.part.offers.add_pending(self.part_offer)
        except ValueError as e:
            print_stack()
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
            return
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
            return 
        
        self.EndModal(wx.ID_OK)

    def onButtonPartOfferEditCancel( self, event ):
        self.EndModal(wx.ID_CANCEL)
    
    def onValueChanged( self, event ):
        self._check()
        event.Skip()

