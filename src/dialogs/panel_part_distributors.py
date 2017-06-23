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
## Class PanelPartDistributors
###########################################################################

class PanelPartDistributors ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 496,385 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer12 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_add_distributor = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer10.Add( self.button_add_distributor, 0, wx.ALL, 5 )
		
		self.button_edit_distributor = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( u"resources/edit.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer10.Add( self.button_edit_distributor, 0, wx.ALL, 5 )
		
		self.button_remove_distributor = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer10.Add( self.button_remove_distributor, 0, wx.ALL, 5 )
		
		
		bSizer11.Add( bSizer10, 1, wx.EXPAND, 5 )
		
		
		bSizer12.Add( bSizer11, 0, wx.EXPAND, 5 )
		
		self.tree_distributors = wx.dataview.DataViewCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12.Add( self.tree_distributors, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer1.Add( bSizer12, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		# Connect Events
		self.button_add_distributor.Bind( wx.EVT_BUTTON, self.onButtonAddDistributorClick )
		self.button_edit_distributor.Bind( wx.EVT_BUTTON, self.onButtonEditDistributorClick )
		self.button_remove_distributor.Bind( wx.EVT_BUTTON, self.onButtonRemoveDistributorClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onButtonAddDistributorClick( self, event ):
		event.Skip()
	
	def onButtonEditDistributorClick( self, event ):
		event.Skip()
	
	def onButtonRemoveDistributorClick( self, event ):
		event.Skip()
	

