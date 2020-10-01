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
## Class PanelPartReferences
###########################################################################

class PanelPartReferences ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 496,385 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer12 = wx.BoxSizer( wx.VERTICAL )

		self.tree_references = wx.dataview.DataViewCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_MULTIPLE )
		bSizer12.Add( self.tree_references, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer1.Add( bSizer12, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()
		self.menu_reference = wx.Menu()
		self.menu_reference_remove_reference = wx.MenuItem( self.menu_reference, wx.ID_ANY, u"Remove reference", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_reference_remove_reference.SetBitmap( wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_reference.Append( self.menu_reference_remove_reference )

		self.Bind( wx.EVT_RIGHT_DOWN, self.PanelPartReferencesOnContextMenu )


		# Connect Events
		self.Bind( wx.EVT_MENU, self.onMenuReferenceRemoveReference, id = self.menu_reference_remove_reference.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onMenuReferenceRemoveReference( self, event ):
		event.Skip()

	def PanelPartReferencesOnContextMenu( self, event ):
		self.PopupMenu( self.menu_reference, event.GetPosition() )


