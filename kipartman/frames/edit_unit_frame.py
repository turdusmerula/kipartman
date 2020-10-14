from dialogs.panel_edit_unit import PanelEditUnit
from frames.dropdown_dialog import DropdownDialog
from frames.select_unit_frame import SelectUnitFrame
import wx
from helper.exception import print_stack
import api.data.unit
import helper.colors as colors

EditUnitApplyEvent, EVT_EDIT_UNIT_APPLY_EVENT = wx.lib.newevent.NewEvent()
EditUnitCancelEvent, EVT_EDIT_UNIT_CANCEL_EVENT = wx.lib.newevent.NewEvent()

class KicadUnitFrameException(Exception):
    def __init__(self, error):
        super(KicadUnitFrameException, self).__init__(error)


class EditUnitFrame(PanelEditUnit):
    def __init__(self, parent): 
        super(EditUnitFrame, self).__init__(parent)

        # set initial state
        self.SetUnit(None)
        self._enable(False)
        

    def SetUnit(self, unit):
        self.unit = unit
        
        self._show_unit(unit)
        self._enable(False)
        self._check()

    def EditUnit(self, unit):
        self.unit = unit
        
        self._show_unit(unit)
        self._enable(True)
        self._check()

    def AddUnit(self):
        self.unit = None
        self._unit = None
        
        self._show_unit(self.unit)
        self._enable(True)
        self._check()

    def _show_unit(self, unit):
        # enable everything else
        if unit is not None:
            self.edit_unit_name.Value = unit.name
            self.edit_unit_symbol.Value = unit.symbol
            self.check_unit_prefixable.Value = unit.prefixable
        else:
            self.edit_unit_name.Value = ""
            self.edit_unit_symbol.Value = ""
            self.check_unit_prefixable.Value = False
 
    def _enable(self, enabled=True):
        self.edit_unit_name.Enabled = enabled
        self.edit_unit_symbol.Enabled = enabled
        self.check_unit_prefixable.Enabled = enabled
        self.button_unit_editApply.Enabled = enabled
        self.button_unit_editCancel.Enabled = enabled
        
    def _check(self):
        error = False
        
        if self.edit_unit_name.Value=="":
            self.edit_unit_name.SetBackgroundColour( colors.RED_ERROR )
            error = True
        else:
            self.edit_unit_name.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        
        if error:
            self.button_unit_editApply.Enabled = False
        else:
            self.button_unit_editApply.Enabled = self.button_unit_editCancel.Enabled

    def onButtonUnitEditApply( self, event ):
        
        try:
            if self.unit is None and len(api.data.unit.find([api.data.unit.FilterSearchSymbol(self.edit_unit_symbol.Value)]).all())>0:
                raise KicadUnitFrameException(f"unit '{self.edit_unit_symbol.Value}' already exists")

            if self.unit is None:
                self.unit = api.data.unit.create()
            
            self.unit.name = self.edit_unit_name.Value
            self.unit.symbol = self.edit_unit_symbol.Value
            self.unit.prefixable = self.check_unit_prefixable.Value

            api.data.unit.save(self.unit)
            
            wx.PostEvent(self, EditUnitApplyEvent(data=self.unit))
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Error renaming library', wx.OK | wx.ICON_ERROR)

        event.Skip()

    def onButtonUnitEditCancel( self, event ):
        wx.PostEvent(self, EditUnitCancelEvent())
        event.Skip()

    def onTextEditUnitName( self, event ):
        self._check()
        event.Skip()

    def onTextEditUnitSymbol( self, event ):
        self._check()
        event.Skip()

    def onButtonSearchUnitClick( self, event ):
        frame = DropdownDialog(self, SelectUnitFrame, "")
        frame.DropHere(self.onSelectUnitFrameOk)
        event.Skip()

    def onButtonRemoveUnitClick( self, event ):
        self._unit = None
        self.button_search_unit.Label = "<none>"
        event.Skip()

    def onSelectUnitFrameOk(self, unit):
        self._unit = unit
        self.button_search_unit.Label = f"{self._unit.name} ({self._unit.symbol})"
        self._check()
        