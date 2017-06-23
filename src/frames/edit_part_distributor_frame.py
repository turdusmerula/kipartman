from dialogs.dialog_edit_part_distributor import DialogEditPartDistributor
from api.models import PartDistributor
from api.queries import DistributorsQuery
from rest_client.exceptions import QueryError
import wx
 

class EditPartDistributorFrame(DialogEditPartDistributor):
    def __init__(self, parent): 
        super(EditPartDistributorFrame, self).__init__(parent)
        self.loadDistributors()

    def loadDistributors(self):
        distributors = DistributorsQuery().get()
        choices = ["<none>"]
        for distributor in distributors:
            choices.append(distributor.name)
        self.choice_distributor.SetItems(choices)

    def AddDistributor(self, part):
        self.Title = "Add distributor"
        self.part = part
        self.distributor = PartDistributor()
 
        self.choice_distributor.SetSelection(0)
        self.edit_part_distributor_packaging_unit.Value = '1'
        self.edit_part_distributor_unit_price.Value = '0'
        self.edit_part_distributor_currency.Value = 'USD'
        self.edit_part_distributor_sku.Value = ''

        result = self.ShowModal()
        if result==wx.ID_OK:
            return self.distributor
        return None

    def EditDistributor(self, part, distributor):
        self.Title = "Edit distributor"
        self.part = part
        self.distributor = distributor

        if distributor.distributor:
            self.choice_distributor.SetSelection(self.distributor.distributor.id)
        else:
            self.choice_distributor.SetSelection(0)
        self.edit_part_distributor_packaging_unit.Value = str(distributor.packaging_unit)
        self.edit_part_distributor_unit_price.Value = str(distributor.unit_price)
        self.edit_part_distributor_currency.Value = str(distributor.currency)
        self.edit_part_distributor_sku.Value = str(distributor.sku)

        result = self.ShowModal()
        if result==wx.ID_OK:
            return self.distributor
        return None

    def onButtonPartDistributorEditApply( self, event ):
        try:
            if self.choice_distributor.GetSelection()==0:
                self.distributor.distributor = None
            else:
                self.distributor.distributor = DistributorsQuery().get()[self.choice_distributor.GetSelection()-1]
            self.distributor.packaging_unit = int(self.edit_part_distributor_packaging_unit.Value)
            self.distributor.unit_price = float(self.edit_part_distributor_unit_price.Value)
            self.distributor.currency = self.edit_part_distributor_currency.Value
            self.distributor.sku = self.edit_part_distributor_sku.Value

        except ValueError as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
            return
        except QueryError as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
            return 

        self.EndModal(wx.ID_OK)

    def onButtonPartDistributorEditCancel( self, event ):
        self.EndModal(wx.ID_CANCEL)
    
