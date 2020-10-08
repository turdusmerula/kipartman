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
## Class PanelPartAttachements
###########################################################################

class PanelPartAttachements ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 496,385 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer12 = wx.BoxSizer( wx.VERTICAL )

		self.tree_attachements = wx.dataview.DataViewCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12.Add( self.tree_attachements, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer1.Add( bSizer12, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()
		self.context_menu = wx.Menu()
		self.menu_attachement_add_attachement = wx.MenuItem( self.context_menu, wx.ID_ANY, u"Add new attachement", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_attachement_add_attachement.SetBitmap( wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ) )
		self.context_menu.Append( self.menu_attachement_add_attachement )

		self.menu_attachement_edit_attachement = wx.MenuItem( self.context_menu, wx.ID_ANY, u"Edit attachement", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_attachement_edit_attachement.SetBitmap( wx.Bitmap( u"resources/edit.png", wx.BITMAP_TYPE_ANY ) )
		self.context_menu.Append( self.menu_attachement_edit_attachement )

		self.menu_attachement_remove_attachement = wx.MenuItem( self.context_menu, wx.ID_ANY, u"Remove attachement", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_attachement_remove_attachement.SetBitmap( wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ) )
		self.context_menu.Append( self.menu_attachement_remove_attachement )

		self.context_menu.AppendSeparator()

		self.context_menu_open = wx.MenuItem( self.context_menu, wx.ID_ANY, u"Open", wx.EmptyString, wx.ITEM_NORMAL )
		self.context_menu.Append( self.context_menu_open )



		# Connect Events
		self.Bind( wx.EVT_MENU, self.onMenuAttachementAddAttachement, id = self.menu_attachement_add_attachement.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuAttachementEditAttachement, id = self.menu_attachement_edit_attachement.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuAttachementRemoveAttachement, id = self.menu_attachement_remove_attachement.GetId() )
		self.Bind( wx.EVT_MENU, self.onContextMenuOpenSelection, id = self.context_menu_open.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onMenuAttachementAddAttachement( self, event ):
		event.Skip()

	def onMenuAttachementEditAttachement( self, event ):
		event.Skip()

	def onMenuAttachementRemoveAttachement( self, event ):
		event.Skip()

	def onContextMenuOpenSelection( self, event ):
		event.Skip()


