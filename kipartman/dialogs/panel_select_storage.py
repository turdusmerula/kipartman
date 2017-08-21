# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jul 12 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.dataview

###########################################################################
## Class PanelSelectStorage
###########################################################################

class PanelSelectStorage ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 499,306 ), style = wx.TAB_TRAVERSAL )
		
		bSizer16 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.search_storage = wx.SearchCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_NOHIDESEL|wx.TE_PROCESS_ENTER )
		self.search_storage.ShowSearchButton( True )
		self.search_storage.ShowCancelButton( True )
		self.search_storage.SetMinSize( wx.Size( 200,-1 ) )
		
		bSizer4.Add( self.search_storage, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )
		
		self.tree_storages = wx.dataview.DataViewCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.tree_storages, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer2.Add( bSizer4, 1, wx.EXPAND, 5 )
		
		
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
		self.search_storage.Bind( wx.EVT_SEARCHCTRL_CANCEL_BTN, self.onSearchStorageCancelButton )
		self.search_storage.Bind( wx.EVT_SEARCHCTRL_SEARCH_BTN, self.onSearchStorageSearchButton )
		self.search_storage.Bind( wx.EVT_TEXT_ENTER, self.onSearchStorageTextEnter )
		self.m_sdbSizer2Cancel.Bind( wx.EVT_BUTTON, self.onButtonCancelClick )
		self.m_sdbSizer2OK.Bind( wx.EVT_BUTTON, self.onButtonOkClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onSearchStorageCancelButton( self, event ):
		event.Skip()
	
	def onSearchStorageSearchButton( self, event ):
		event.Skip()
	
	def onSearchStorageTextEnter( self, event ):
		event.Skip()
	
	def onButtonCancelClick( self, event ):
		event.Skip()
	
	def onButtonOkClick( self, event ):
		event.Skip()
	

