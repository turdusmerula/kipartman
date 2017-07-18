from dialogs.dialog_edit_part_offer import DialogEditPartOffer
import wx
import rest

# TODO: switch to a list for currency
class EditPartOfferFrame(DialogEditPartOffer):
    def __init__(self, parent): 
        super(EditPartOfferFrame, self).__init__(parent)
        self.loadDistributors()

    def loadDistributors(self):
        distributors = rest.api.find_distributors()
        choices = ["<none>"]
        for distributor in distributors:
            choices.append(distributor.name)
        self.choice_distributor.SetItems(choices)

    def AddOffer(self, part):
        self.Title = "Add distributor"
        self.part = part
        self.offer = rest.model.PartOffer()
 
        self.choice_distributor.Enabled = True

        self.choice_distributor.SetSelection(0)
        self.edit_part_offer_packaging_unit.Value = '1'
        self.edit_part_offer_quantity.Value = '1'
        self.edit_part_offer_unit_price.Value = '0'
        self.edit_part_offer_currency.Value = 'USD'
        self.edit_part_offer_sku.Value = ''

        result = self.ShowModal()
        if result==wx.ID_OK:
            return self.offer
        return None

    def EditOffer(self, part, offer):
        self.Title = "Edit distributor"
        self.part = part
        self.offer = offer

        self.choice_distributor.Enabled = False

        if offer.distributor:
            self.choice_distributor.SetSelection(self.offer.distributor.id)
        else:
            self.choice_distributor.SetSelection(0)
        self.edit_part_offer_packaging_unit.Value = str(offer.packaging_unit)
        self.edit_part_offer_quantity.Value = str(offer.quantity)
        self.edit_part_offer_unit_price.Value = str(offer.unit_price)
        self.edit_part_offer_currency.Value = str(offer.currency)
        self.edit_part_offer_sku.Value = str(offer.sku)

        result = self.ShowModal()
        if result==wx.ID_OK:
            return self.offer
        return None

    def onButtonPartOfferEditApply( self, event ):
        try:
            if self.choice_distributor.GetSelection()==0:
                raise Exception("Missing distributor")
            else:
                self.offer.distributor = rest.api.find_distributor(self.choice_distributor.GetSelection())

            self.offer.packaging_unit = int(self.edit_part_offer_packaging_unit.Value)
            self.offer.quantity = int(self.edit_part_offer_quantity.Value)
            self.offer.unit_price = float(self.edit_part_offer_unit_price.Value)
            self.offer.currency = self.edit_part_offer_currency.Value
            self.offer.sku = self.edit_part_offer_sku.Value
        except ValueError as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
            return
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
            return 
        self.EndModal(wx.ID_OK)

    def onButtonPartOfferEditCancel( self, event ):
        self.EndModal(wx.ID_CANCEL)
    
