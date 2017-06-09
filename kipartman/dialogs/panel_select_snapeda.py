# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Apr 29 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.dataview

###########################################################################
## Class PanelSelectSnapeda
###########################################################################

class PanelSelectSnapeda ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1050,407 ), style = wx.TAB_TRAVERSAL )
		
		bSizer16 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.search_snapeda = wx.SearchCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_NOHIDESEL|wx.TE_PROCESS_ENTER )
		self.search_snapeda.ShowSearchButton( True )
		self.search_snapeda.ShowCancelButton( True )
		self.search_snapeda.SetMinSize( wx.Size( 150,-1 ) )
		
		bSizer2.Add( self.search_snapeda, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		self.tree_snapedas = wx.dataview.DataViewCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.tree_snapedas, 1, wx.ALL|wx.EXPAND, 5 )
		
		
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
		self.search_snapeda.Bind( wx.EVT_SEARCHCTRL_SEARCH_BTN, self.onSearchSnapedaButton )
		self.search_snapeda.Bind( wx.EVT_TEXT_ENTER, self.onSearchSnapedaEnter )
		self.tree_snapedas.Bind( wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.onTreeSnapedasSelectionChanged, id = wx.ID_ANY )
		self.m_sdbSizer2Cancel.Bind( wx.EVT_BUTTON, self.onButtonCancelClick )
		self.m_sdbSizer2OK.Bind( wx.EVT_BUTTON, self.onButtonOkClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onSearchSnapedaButton( self, event ):
		event.Skip()
	
	def onSearchSnapedaEnter( self, event ):
		event.Skip()
	
	def onTreeSnapedasSelectionChanged( self, event ):
		event.Skip()
	
	def onButtonCancelClick( self, event ):
		event.Skip()
	
	def onButtonOkClick( self, event ):
		event.Skip()
	

