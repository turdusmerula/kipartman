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
## Class DialogEditPartOffer
###########################################################################

class DialogEditPartOffer ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 426,284 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Distributor", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		fgSizer1.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		choice_distributorChoices = []
		self.choice_distributor = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_distributorChoices, 0 )
		self.choice_distributor.SetSelection( 0 )
		bSizer2.Add( self.choice_distributor, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.button_add_distributor = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer2.Add( self.button_add_distributor, 0, wx.ALL, 5 )
		
		
		fgSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )
		
		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Packaging Unit", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		fgSizer1.Add( self.m_staticText4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.edit_part_offer_packaging_unit = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.edit_part_offer_packaging_unit.SetHelpText( u"Number of items per package" )
		
		fgSizer1.Add( self.edit_part_offer_packaging_unit, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"Quantity:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		fgSizer1.Add( self.m_staticText6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.edit_part_offer_quantity = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.edit_part_offer_quantity.SetHelpText( u"The minimum quantity at wich the price applies" )
		
		fgSizer1.Add( self.edit_part_offer_quantity, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.static_value = wx.StaticText( self, wx.ID_ANY, u"Unit Price", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.static_value.Wrap( -1 )
		fgSizer1.Add( self.static_value, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.edit_part_offer_unit_price = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.edit_part_offer_unit_price.SetHelpText( u"Price for one item" )
		
		fgSizer1.Add( self.edit_part_offer_unit_price, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.static_min_value = wx.StaticText( self, wx.ID_ANY, u"Currency", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.static_min_value.Wrap( -1 )
		fgSizer1.Add( self.static_min_value, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.edit_part_offer_currency = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.edit_part_offer_currency.SetHelpText( u"Currency for the price" )
		
		fgSizer1.Add( self.edit_part_offer_currency, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.static_nom_value = wx.StaticText( self, wx.ID_ANY, u"SKU", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.static_nom_value.Wrap( -1 )
		fgSizer1.Add( self.static_nom_value, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.edit_part_offer_sku = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.edit_part_offer_sku.SetHelpText( u"Distributor reference" )
		
		fgSizer1.Add( self.edit_part_offer_sku, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer1.Add( fgSizer1, 1, wx.EXPAND, 5 )
		
		button_part_offer_edit = wx.StdDialogButtonSizer()
		self.button_part_offer_editApply = wx.Button( self, wx.ID_APPLY )
		button_part_offer_edit.AddButton( self.button_part_offer_editApply )
		self.button_part_offer_editCancel = wx.Button( self, wx.ID_CANCEL )
		button_part_offer_edit.AddButton( self.button_part_offer_editCancel )
		button_part_offer_edit.Realize();
		
		bSizer1.Add( button_part_offer_edit, 0, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.button_add_distributor.Bind( wx.EVT_BUTTON, self.onButtonAddDistributorClick )
		self.button_part_offer_editApply.Bind( wx.EVT_BUTTON, self.onButtonPartOfferEditApply )
		self.button_part_offer_editCancel.Bind( wx.EVT_BUTTON, self.onButtonPartOfferEditCancel )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onButtonAddDistributorClick( self, event ):
		event.Skip()
	
	def onButtonPartOfferEditApply( self, event ):
		event.Skip()
	
	def onButtonPartOfferEditCancel( self, event ):
		event.Skip()
	

