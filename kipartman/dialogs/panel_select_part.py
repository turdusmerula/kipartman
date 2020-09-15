# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.9.0 Sep  2 2020)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.dataview

###########################################################################
## Class PanelSelectPart
###########################################################################

class PanelSelectPart ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 833,312 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer16 = wx.BoxSizer( wx.VERTICAL )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_splitter1 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter1.Bind( wx.EVT_IDLE, self.m_splitter1OnIdle )

		self.m_panel1 = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer4 = wx.BoxSizer( wx.VERTICAL )

		bSizer61 = wx.BoxSizer( wx.HORIZONTAL )

		self.search_part = wx.SearchCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.search_part.ShowSearchButton( True )
		self.search_part.ShowCancelButton( False )
		self.search_part.SetMinSize( wx.Size( 200,-1 ) )

		bSizer61.Add( self.search_part, 0, wx.ALL|wx.EXPAND, 5 )

		self.button_refresh_parts = wx.BitmapButton( self.m_panel1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0|wx.BORDER_NONE )

		self.button_refresh_parts.SetBitmap( wx.Bitmap( u"resources/refresh.png", wx.BITMAP_TYPE_ANY ) )
		bSizer61.Add( self.button_refresh_parts, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer4.Add( bSizer61, 0, wx.ALIGN_RIGHT, 5 )

		self.tree_parts = wx.dataview.DataViewCtrl( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.tree_parts, 1, wx.ALL|wx.EXPAND, 5 )


		self.m_panel1.SetSizer( bSizer4 )
		self.m_panel1.Layout()
		bSizer4.Fit( self.m_panel1 )
		self.m_panel2 = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer5 = wx.BoxSizer( wx.VERTICAL )

		self.tree_parameters = wx.dataview.DataViewCtrl( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.tree_parameters, 1, wx.ALL|wx.EXPAND, 5 )


		self.m_panel2.SetSizer( bSizer5 )
		self.m_panel2.Layout()
		bSizer5.Fit( self.m_panel2 )
		self.m_splitter1.SplitVertically( self.m_panel1, self.m_panel2, 0 )
		bSizer2.Add( self.m_splitter1, 1, wx.EXPAND, 5 )


		bSizer16.Add( bSizer2, 1, wx.EXPAND, 5 )

		button_part_select = wx.StdDialogButtonSizer()
		self.button_part_selectOK = wx.Button( self, wx.ID_OK )
		button_part_select.AddButton( self.button_part_selectOK )
		self.button_part_selectCancel = wx.Button( self, wx.ID_CANCEL )
		button_part_select.AddButton( self.button_part_selectCancel )
		button_part_select.Realize();

		bSizer16.Add( button_part_select, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5 )


		self.SetSizer( bSizer16 )
		self.Layout()

		# Connect Events
		self.search_part.Bind( wx.EVT_SEARCHCTRL_CANCEL_BTN, self.onSearchPartCancelButton )
		self.search_part.Bind( wx.EVT_SEARCHCTRL_SEARCH_BTN, self.onSearchPartSearchButton )
		self.search_part.Bind( wx.EVT_TEXT_ENTER, self.onSearchPartTextEnter )
		self.button_refresh_parts.Bind( wx.EVT_BUTTON, self.onButtonRefreshPartsClick )
		self.button_part_selectCancel.Bind( wx.EVT_BUTTON, self.onButtonCancelClick )
		self.button_part_selectOK.Bind( wx.EVT_BUTTON, self.onButtonOkClick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onSearchPartCancelButton( self, event ):
		event.Skip()

	def onSearchPartSearchButton( self, event ):
		event.Skip()

	def onSearchPartTextEnter( self, event ):
		event.Skip()

	def onButtonRefreshPartsClick( self, event ):
		event.Skip()

	def onButtonCancelClick( self, event ):
		event.Skip()

	def onButtonOkClick( self, event ):
		event.Skip()

	def m_splitter1OnIdle( self, event ):
		self.m_splitter1.SetSashPosition( 0 )
		self.m_splitter1.Unbind( wx.EVT_IDLE )


