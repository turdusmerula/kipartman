# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jul 12 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class DialogEditWish
###########################################################################

class DialogEditWish ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 409,124 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer2 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer2.AddGrowableCol( 1 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Quantity", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		fgSizer2.Add( self.m_staticText1, 1, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.spin_quantity = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10, 0 )
		fgSizer2.Add( self.spin_quantity, 0, wx.ALL, 5 )
		
		
		bSizer4.Add( fgSizer2, 1, wx.EXPAND, 5 )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_validate = wx.Button( self, wx.ID_OK, u"Add", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.button_validate.SetDefault() 
		bSizer2.Add( self.button_validate, 0, wx.ALL, 5 )
		
		self.button_cancel = wx.Button( self, wx.ID_CANCEL, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.button_cancel, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer2, 0, wx.TOP|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		bSizer4.Add( bSizer1, 0, wx.EXPAND|wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer4 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.button_validate.Bind( wx.EVT_BUTTON, self.onValidateClick )
		self.button_cancel.Bind( wx.EVT_BUTTON, self.onCancelClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onValidateClick( self, event ):
		event.Skip()
	
	def onCancelClick( self, event ):
		event.Skip()
	

