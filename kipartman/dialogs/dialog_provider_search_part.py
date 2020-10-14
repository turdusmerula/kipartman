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
## Class DialogProviderSearchPart
###########################################################################

class DialogProviderSearchPart ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 1140,376 ), style = wx.DEFAULT_FRAME_STYLE|wx.FRAME_TOOL_WINDOW|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer16 = wx.BoxSizer( wx.VERTICAL )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		self.search_text = wx.SearchCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_NOHIDESEL|wx.TE_PROCESS_ENTER )
		self.search_text.ShowSearchButton( True )
		self.search_text.ShowCancelButton( True )
		self.search_text.SetMinSize( wx.Size( 150,-1 ) )

		bSizer2.Add( self.search_text, 0, wx.ALL|wx.EXPAND, 5 )

		self.tree_parts = wx.dataview.DataViewCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_MULTIPLE )
		bSizer2.Add( self.tree_parts, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer16.Add( bSizer2, 1, wx.EXPAND, 5 )

		m_sdbSizer2 = wx.StdDialogButtonSizer()
		self.m_sdbSizer2OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer2.AddButton( self.m_sdbSizer2OK )
		self.m_sdbSizer2Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer2.AddButton( self.m_sdbSizer2Cancel )
		m_sdbSizer2.Realize();

		bSizer16.Add( m_sdbSizer2, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5 )


		self.SetSizer( bSizer16 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.search_text.Bind( wx.EVT_SEARCHCTRL_CANCEL_BTN, self.onSearchCancel )
		self.search_text.Bind( wx.EVT_SEARCHCTRL_SEARCH_BTN, self.onSearchEnter )
		self.search_text.Bind( wx.EVT_TEXT_ENTER, self.onSearchEnter )
		self.m_sdbSizer2Cancel.Bind( wx.EVT_BUTTON, self.onButtonCancelClick )
		self.m_sdbSizer2OK.Bind( wx.EVT_BUTTON, self.onButtonOkClick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onSearchCancel( self, event ):
		event.Skip()

	def onSearchEnter( self, event ):
		event.Skip()


	def onButtonCancelClick( self, event ):
		event.Skip()

	def onButtonOkClick( self, event ):
		event.Skip()


