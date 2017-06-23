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
## Class PanelSelectOctopart
###########################################################################

class PanelSelectOctopart ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1050,407 ), style = wx.TAB_TRAVERSAL )
		
		bSizer16 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.search_octopart = wx.SearchCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_NOHIDESEL|wx.TE_PROCESS_ENTER )
		self.search_octopart.ShowSearchButton( True )
		self.search_octopart.ShowCancelButton( True )
		self.search_octopart.SetMinSize( wx.Size( 150,-1 ) )
		
		bSizer2.Add( self.search_octopart, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		self.tree_octoparts = wx.dataview.DataViewCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.tree_octoparts, 1, wx.ALL|wx.EXPAND, 5 )
		
		
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
		self.search_octopart.Bind( wx.EVT_SEARCHCTRL_SEARCH_BTN, self.onSearchOctopartButton )
		self.search_octopart.Bind( wx.EVT_TEXT_ENTER, self.onSearchOctopartEnter )
		self.tree_octoparts.Bind( wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.onTreeOctopartsSelectionChanged, id = wx.ID_ANY )
		self.m_sdbSizer2Cancel.Bind( wx.EVT_BUTTON, self.onButtonCancelClick )
		self.m_sdbSizer2OK.Bind( wx.EVT_BUTTON, self.onButtonOkClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onSearchOctopartButton( self, event ):
		event.Skip()
	
	def onSearchOctopartEnter( self, event ):
		event.Skip()
	
	def onTreeOctopartsSelectionChanged( self, event ):
		event.Skip()
	
	def onButtonCancelClick( self, event ):
		event.Skip()
	
	def onButtonOkClick( self, event ):
		event.Skip()
	

