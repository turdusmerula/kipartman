# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.9.0 Sep  2 2020)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class PanelEditManufacturer
###########################################################################

class PanelEditManufacturer ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 512,320 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer3 = wx.BoxSizer( wx.VERTICAL )

		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Manufacturer", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		fgSizer1.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.edit_manufacturer_name = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.edit_manufacturer_name, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Address", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		fgSizer1.Add( self.m_staticText4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.edit_manufacturer_address = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		fgSizer1.Add( self.edit_manufacturer_address, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"Website", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )

		fgSizer1.Add( self.m_staticText6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.edit_manufacturer_website = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.edit_manufacturer_website, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"Email", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )

		fgSizer1.Add( self.m_staticText8, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.edit_manufacturer_email = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.edit_manufacturer_email, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText9 = wx.StaticText( self, wx.ID_ANY, u"Phone", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )

		fgSizer1.Add( self.m_staticText9, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.edit_manufacturer_phone = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.edit_manufacturer_phone, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"Comment", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )

		fgSizer1.Add( self.m_staticText11, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.edit_manufacturer_comment = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		fgSizer1.Add( self.edit_manufacturer_comment, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer3.Add( fgSizer1, 1, wx.EXPAND, 5 )

		button_manufacturer_edit = wx.StdDialogButtonSizer()
		self.button_manufacturer_editApply = wx.Button( self, wx.ID_APPLY )
		button_manufacturer_edit.AddButton( self.button_manufacturer_editApply )
		self.button_manufacturer_editCancel = wx.Button( self, wx.ID_CANCEL )
		button_manufacturer_edit.AddButton( self.button_manufacturer_editCancel )
		button_manufacturer_edit.Realize();

		bSizer3.Add( button_manufacturer_edit, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5 )


		self.SetSizer( bSizer3 )
		self.Layout()

		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.onInitDialog )
		self.edit_manufacturer_name.Bind( wx.EVT_TEXT, self.onManufacturerValueChanged )
		self.edit_manufacturer_address.Bind( wx.EVT_TEXT, self.onManufacturerValueChanged )
		self.edit_manufacturer_website.Bind( wx.EVT_TEXT, self.onManufacturerValueChanged )
		self.edit_manufacturer_email.Bind( wx.EVT_TEXT, self.onManufacturerValueChanged )
		self.edit_manufacturer_phone.Bind( wx.EVT_TEXT, self.onManufacturerValueChanged )
		self.edit_manufacturer_comment.Bind( wx.EVT_TEXT, self.onManufacturerValueChanged )
		self.button_manufacturer_editApply.Bind( wx.EVT_BUTTON, self.onApplyButtonClick )
		self.button_manufacturer_editCancel.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onInitDialog( self, event ):
		event.Skip()

	def onManufacturerValueChanged( self, event ):
		event.Skip()






	def onApplyButtonClick( self, event ):
		event.Skip()

	def onCancelButtonClick( self, event ):
		event.Skip()


