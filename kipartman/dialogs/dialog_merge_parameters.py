# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.9.0 Sep 24 2020)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class DialogMergeParameters
###########################################################################

class DialogMergeParameters ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 427,187 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer4 = wx.BoxSizer( wx.VERTICAL )

		fgSizer2 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer2.AddGrowableCol( 1 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Merge into", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		fgSizer2.Add( self.m_staticText2, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		combo_merge_intoChoices = []
		self.combo_merge_into = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, combo_merge_intoChoices, 0 )
		self.combo_merge_into.SetSelection( 0 )
		fgSizer2.Add( self.combo_merge_into, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer4.Add( fgSizer2, 1, wx.EXPAND, 5 )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		self.button_apply = wx.Button( self, wx.ID_OK, u"Apply", wx.DefaultPosition, wx.DefaultSize, 0 )

		self.button_apply.SetDefault()
		bSizer2.Add( self.button_apply, 0, wx.ALL, 5 )

		self.button_cancel = wx.Button( self, wx.ID_CANCEL, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.button_cancel, 0, wx.ALL, 5 )


		bSizer1.Add( bSizer2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP|wx.BOTTOM, 5 )


		bSizer4.Add( bSizer1, 0, wx.EXPAND, 5 )


		self.SetSizer( bSizer4 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.combo_merge_into.Bind( wx.EVT_CHOICE, self.onComboMergeIntoChoice )
		self.button_apply.Bind( wx.EVT_BUTTON, self.onButtonOkClick )
		self.button_cancel.Bind( wx.EVT_BUTTON, self.onButtonCancelClick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onComboMergeIntoChoice( self, event ):
		event.Skip()

	def onButtonOkClick( self, event ):
		event.Skip()

	def onButtonCancelClick( self, event ):
		event.Skip()


