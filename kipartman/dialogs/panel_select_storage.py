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
## Class PanelSelectStorage
###########################################################################

class PanelSelectStorage ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 499,306 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer16 = wx.BoxSizer( wx.VERTICAL )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer4 = wx.BoxSizer( wx.VERTICAL )

		bSizer61 = wx.BoxSizer( wx.HORIZONTAL )

		self.search_part = wx.SearchCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.search_part.ShowSearchButton( True )
		self.search_part.ShowCancelButton( False )
		self.search_part.SetMinSize( wx.Size( 200,-1 ) )

		bSizer61.Add( self.search_part, 0, wx.ALL|wx.EXPAND, 5 )

		self.button_refresh_storages = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0|wx.BORDER_NONE )

		self.button_refresh_storages.SetBitmap( wx.Bitmap( u"resources/refresh.png", wx.BITMAP_TYPE_ANY ) )
		bSizer61.Add( self.button_refresh_storages, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer4.Add( bSizer61, 0, wx.ALIGN_RIGHT, 5 )

		self.tree_storages = wx.dataview.DataViewCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.tree_storages, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer2.Add( bSizer4, 1, wx.EXPAND, 5 )


		bSizer16.Add( bSizer2, 1, wx.EXPAND, 5 )

		button_storage_select = wx.StdDialogButtonSizer()
		self.button_storage_selectOK = wx.Button( self, wx.ID_OK )
		button_storage_select.AddButton( self.button_storage_selectOK )
		self.button_storage_selectCancel = wx.Button( self, wx.ID_CANCEL )
		button_storage_select.AddButton( self.button_storage_selectCancel )
		button_storage_select.Realize();

		bSizer16.Add( button_storage_select, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5 )


		self.SetSizer( bSizer16 )
		self.Layout()

		# Connect Events
		self.search_part.Bind( wx.EVT_SEARCHCTRL_CANCEL_BTN, self.onSearchStorageCancelButton )
		self.search_part.Bind( wx.EVT_SEARCHCTRL_SEARCH_BTN, self.onSearchStorageSearchButton )
		self.search_part.Bind( wx.EVT_TEXT_ENTER, self.onSearchStorageTextEnter )
		self.button_refresh_storages.Bind( wx.EVT_BUTTON, self.onButtonRefreshStoragesClick )
		self.button_storage_selectCancel.Bind( wx.EVT_BUTTON, self.onButtonCancelClick )
		self.button_storage_selectOK.Bind( wx.EVT_BUTTON, self.onButtonOkClick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onSearchStorageCancelButton( self, event ):
		event.Skip()

	def onSearchStorageSearchButton( self, event ):
		event.Skip()

	def onSearchStorageTextEnter( self, event ):
		event.Skip()

	def onButtonRefreshStoragesClick( self, event ):
		event.Skip()

	def onButtonCancelClick( self, event ):
		event.Skip()

	def onButtonOkClick( self, event ):
		event.Skip()


