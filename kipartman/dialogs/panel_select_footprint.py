# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.9.0 Sep 24 2020)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.dataview

###########################################################################
## Class PanelSelectFootprint
###########################################################################

class PanelSelectFootprint ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 786,341 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer16 = wx.BoxSizer( wx.VERTICAL )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer4 = wx.BoxSizer( wx.VERTICAL )

		bSizer61 = wx.BoxSizer( wx.HORIZONTAL )

		self.search_footprint = wx.SearchCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.search_footprint.ShowSearchButton( True )
		self.search_footprint.ShowCancelButton( False )
		self.search_footprint.SetMinSize( wx.Size( 200,-1 ) )

		bSizer61.Add( self.search_footprint, 0, wx.ALL|wx.EXPAND, 5 )

		self.button_refresh_footprints = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0|wx.BORDER_NONE )

		self.button_refresh_footprints.SetBitmap( wx.Bitmap( u"resources/refresh.png", wx.BITMAP_TYPE_ANY ) )
		bSizer61.Add( self.button_refresh_footprints, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer4.Add( bSizer61, 0, wx.ALIGN_RIGHT, 5 )

		self.tree_footprints = wx.dataview.DataViewCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.tree_footprints, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer2.Add( bSizer4, 1, wx.EXPAND, 5 )

		self.panel_image_footprint = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer41 = wx.BoxSizer( wx.VERTICAL )

		self.image_footprint = wx.StaticBitmap( self.panel_image_footprint, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer41.Add( self.image_footprint, 1, wx.ALL|wx.EXPAND, 5 )


		self.panel_image_footprint.SetSizer( bSizer41 )
		self.panel_image_footprint.Layout()
		bSizer41.Fit( self.panel_image_footprint )
		bSizer2.Add( self.panel_image_footprint, 1, wx.EXPAND |wx.ALL, 5 )


		bSizer16.Add( bSizer2, 1, wx.EXPAND, 5 )

		button_footprint_edit = wx.StdDialogButtonSizer()
		self.button_footprint_editOK = wx.Button( self, wx.ID_OK )
		button_footprint_edit.AddButton( self.button_footprint_editOK )
		self.button_footprint_editCancel = wx.Button( self, wx.ID_CANCEL )
		button_footprint_edit.AddButton( self.button_footprint_editCancel )
		button_footprint_edit.Realize();

		bSizer16.Add( button_footprint_edit, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5 )


		self.SetSizer( bSizer16 )
		self.Layout()

		# Connect Events
		self.search_footprint.Bind( wx.EVT_SEARCHCTRL_CANCEL_BTN, self.onSearchFootprintCancel )
		self.search_footprint.Bind( wx.EVT_SEARCHCTRL_SEARCH_BTN, self.onSearchFootprintButton )
		self.search_footprint.Bind( wx.EVT_TEXT_ENTER, self.onSearchFootprintTextEnter )
		self.button_refresh_footprints.Bind( wx.EVT_BUTTON, self.onButtonRefreshFootprintsClick )
		self.button_footprint_editCancel.Bind( wx.EVT_BUTTON, self.onButtonCancelClick )
		self.button_footprint_editOK.Bind( wx.EVT_BUTTON, self.onButtonOkClick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onSearchFootprintCancel( self, event ):
		event.Skip()

	def onSearchFootprintButton( self, event ):
		event.Skip()

	def onSearchFootprintTextEnter( self, event ):
		event.Skip()

	def onButtonRefreshFootprintsClick( self, event ):
		event.Skip()

	def onButtonCancelClick( self, event ):
		event.Skip()

	def onButtonOkClick( self, event ):
		event.Skip()


