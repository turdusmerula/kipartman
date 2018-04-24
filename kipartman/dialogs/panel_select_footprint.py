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
## Class PanelSelectFootprint
###########################################################################

class PanelSelectFootprint ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 718,261 ), style = wx.TAB_TRAVERSAL )
		
		bSizer16 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.search_footprint = wx.SearchCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.search_footprint.ShowSearchButton( True )
		self.search_footprint.ShowCancelButton( True )
		self.search_footprint.SetMinSize( wx.Size( 180,-1 ) )
		
		bSizer4.Add( self.search_footprint, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )
		
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
		self.search_footprint.Bind( wx.EVT_SEARCHCTRL_CANCEL_BTN, self.onSearchFootprintCancel )
		self.search_footprint.Bind( wx.EVT_SEARCHCTRL_SEARCH_BTN, self.onSearchFootprintButton )
		self.search_footprint.Bind( wx.EVT_TEXT_ENTER, self.onSearchFootprintEnter )
		self.tree_footprints.Bind( wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.onTreeFootprintsSelectionChanged, id = wx.ID_ANY )
		self.m_sdbSizer2Cancel.Bind( wx.EVT_BUTTON, self.onButtonCancelClick )
		self.m_sdbSizer2OK.Bind( wx.EVT_BUTTON, self.onButtonOkClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onSearchFootprintCancel( self, event ):
		event.Skip()
	
	def onSearchFootprintButton( self, event ):
		event.Skip()
	
	def onSearchFootprintEnter( self, event ):
		event.Skip()
	
	def onTreeFootprintsSelectionChanged( self, event ):
		event.Skip()
	
	def onButtonCancelClick( self, event ):
		event.Skip()
	
	def onButtonOkClick( self, event ):
		event.Skip()
	

