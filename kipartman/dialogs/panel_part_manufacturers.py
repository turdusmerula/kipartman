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
## Class PanelPartManufacturers
###########################################################################

class PanelPartManufacturers ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 496,385 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer12 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_add_manufacturer = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer10.Add( self.button_add_manufacturer, 0, wx.ALL, 5 )
		
		self.button_edit_manufacturer = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( u"resources/edit.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer10.Add( self.button_edit_manufacturer, 0, wx.ALL, 5 )
		
		self.button_remove_manufacturer = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer10.Add( self.button_remove_manufacturer, 0, wx.ALL, 5 )
		
		
		bSizer11.Add( bSizer10, 1, wx.EXPAND, 5 )
		
		
		bSizer12.Add( bSizer11, 0, wx.EXPAND, 5 )
		
		self.tree_manufacturers = wx.dataview.DataViewCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12.Add( self.tree_manufacturers, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer1.Add( bSizer12, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		# Connect Events
		self.button_add_manufacturer.Bind( wx.EVT_BUTTON, self.onButtonAddManufacturerClick )
		self.button_edit_manufacturer.Bind( wx.EVT_BUTTON, self.onButtonEditManufacturerClick )
		self.button_remove_manufacturer.Bind( wx.EVT_BUTTON, self.onButtonRemoveManufacturerClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onButtonAddManufacturerClick( self, event ):
		event.Skip()
	
	def onButtonEditManufacturerClick( self, event ):
		event.Skip()
	
	def onButtonRemoveManufacturerClick( self, event ):
		event.Skip()
	

