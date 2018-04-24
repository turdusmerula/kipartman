# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Dec 22 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.dataview

###########################################################################
## Class PanelSelectSymbol
###########################################################################

class PanelSelectSymbol ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 718,261 ), style = wx.TAB_TRAVERSAL )
		
		bSizer16 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.search_symbol = wx.SearchCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.search_symbol.ShowSearchButton( True )
		self.search_symbol.ShowCancelButton( True )
		self.search_symbol.SetMinSize( wx.Size( 180,-1 ) )
		
		bSizer4.Add( self.search_symbol, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )
		
		self.tree_symbols = wx.dataview.DataViewCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.tree_symbols, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer2.Add( bSizer4, 1, wx.EXPAND, 5 )
		
		self.panel_image_symbol = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer41 = wx.BoxSizer( wx.VERTICAL )
		
		self.image_symbol = wx.StaticBitmap( self.panel_image_symbol, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer41.Add( self.image_symbol, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.panel_image_symbol.SetSizer( bSizer41 )
		self.panel_image_symbol.Layout()
		bSizer41.Fit( self.panel_image_symbol )
		bSizer2.Add( self.panel_image_symbol, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		bSizer16.Add( bSizer2, 1, wx.EXPAND, 5 )
		
		m_sdbSizer2 = wx.StdDialogButtonSizer()
		self.m_sdbSizer2OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer2.AddButton( self.m_sdbSizer2OK )
		self.m_sdbSizer2Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer2.AddButton( self.m_sdbSizer2Cancel )
		m_sdbSizer2.Realize();
		
		bSizer16.Add( m_sdbSizer2, 0, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer16 )
		self.Layout()
		
		# Connect Events
		self.search_symbol.Bind( wx.EVT_SEARCHCTRL_CANCEL_BTN, self.onSearchSymbolCancel )
		self.search_symbol.Bind( wx.EVT_SEARCHCTRL_SEARCH_BTN, self.onSearchSymbolButton )
		self.search_symbol.Bind( wx.EVT_TEXT_ENTER, self.onSearchSymbolEnter )
		self.tree_symbols.Bind( wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.onTreeSymbolsSelectionChanged, id = wx.ID_ANY )
		self.m_sdbSizer2Cancel.Bind( wx.EVT_BUTTON, self.onButtonCancelClick )
		self.m_sdbSizer2OK.Bind( wx.EVT_BUTTON, self.onButtonOkClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onSearchSymbolCancel( self, event ):
		event.Skip()
	
	def onSearchSymbolButton( self, event ):
		event.Skip()
	
	def onSearchSymbolEnter( self, event ):
		event.Skip()
	
	def onTreeSymbolsSelectionChanged( self, event ):
		event.Skip()
	
	def onButtonCancelClick( self, event ):
		event.Skip()
	
	def onButtonOkClick( self, event ):
		event.Skip()
	

