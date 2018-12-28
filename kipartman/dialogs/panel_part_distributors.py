# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Dec 18 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.dataview

###########################################################################
## Class PanelPartDistributors
###########################################################################

class PanelPartDistributors ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 496,385 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer12 = wx.BoxSizer( wx.VERTICAL )

		self.tree_distributors = wx.dataview.DataViewCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_MULTIPLE )
		bSizer12.Add( self.tree_distributors, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer1.Add( bSizer12, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()
		self.menu_distributors = wx.Menu()
		self.menu_distributor_add_distributor = wx.MenuItem( self.menu_distributors, wx.ID_ANY, u"Add new distributor", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_distributor_add_distributor.SetBitmap( wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_distributors.Append( self.menu_distributor_add_distributor )

		self.menu_distributor_edit_distributor = wx.MenuItem( self.menu_distributors, wx.ID_ANY, u"Edit distributor", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_distributor_edit_distributor.SetBitmap( wx.Bitmap( u"resources/edit.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_distributors.Append( self.menu_distributor_edit_distributor )

		self.menu_distributor_remove_distributor = wx.MenuItem( self.menu_distributors, wx.ID_ANY, u"Remove distributor", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_distributor_remove_distributor.SetBitmap( wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_distributors.Append( self.menu_distributor_remove_distributor )

		self.Bind( wx.EVT_RIGHT_DOWN, self.PanelPartDistributorsOnContextMenu )


		# Connect Events
		self.Bind( wx.EVT_MENU, self.onMenuDistributorAddDistributor, id = self.menu_distributor_add_distributor.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuDistributorEditDistributor, id = self.menu_distributor_edit_distributor.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuDistributorRemoveDistributor, id = self.menu_distributor_remove_distributor.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onMenuDistributorAddDistributor( self, event ):
		event.Skip()

	def onMenuDistributorEditDistributor( self, event ):
		event.Skip()

	def onMenuDistributorRemoveDistributor( self, event ):
		event.Skip()

	def PanelPartDistributorsOnContextMenu( self, event ):
		self.PopupMenu( self.menu_distributors, event.GetPosition() )


