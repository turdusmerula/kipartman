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
## Class PanelPartParameters
###########################################################################

class PanelPartParameters ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 496,385 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer12 = wx.BoxSizer( wx.VERTICAL )
		
		self.tree_parameters = wx.dataview.DataViewCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12.Add( self.tree_parameters, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer1.Add( bSizer12, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		self.menu_parameter = wx.Menu()
		self.menu_parameter_add_parameter = wx.MenuItem( self.menu_parameter, wx.ID_ANY, u"Add new parameter", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_parameter_add_parameter.SetBitmap( wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_parameter.Append( self.menu_parameter_add_parameter )
		
		self.menu_parameter_edit_parameter = wx.MenuItem( self.menu_parameter, wx.ID_ANY, u"Edit parameter", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_parameter_edit_parameter.SetBitmap( wx.Bitmap( u"resources/edit.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_parameter.Append( self.menu_parameter_edit_parameter )
		
		self.menu_parameter_remove_parameter = wx.MenuItem( self.menu_parameter, wx.ID_ANY, u"Remove parameter", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_parameter_remove_parameter.SetBitmap( wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_parameter.Append( self.menu_parameter_remove_parameter )
		
		self.Bind( wx.EVT_RIGHT_DOWN, self.PanelPartParametersOnContextMenu ) 
		
		
		# Connect Events
		self.Bind( wx.EVT_MENU, self.onMenuParameterAddParameter, id = self.menu_parameter_add_parameter.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuParameterEditParameter, id = self.menu_parameter_edit_parameter.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuParameterRemoveParameter, id = self.menu_parameter_remove_parameter.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onMenuParameterAddParameter( self, event ):
		event.Skip()
	
	def onMenuParameterEditParameter( self, event ):
		event.Skip()
	
	def onMenuParameterRemoveParameter( self, event ):
		event.Skip()
	
	def PanelPartParametersOnContextMenu( self, event ):
		self.PopupMenu( self.menu_parameter, event.GetPosition() )
		

