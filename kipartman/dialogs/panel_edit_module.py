# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Dec 18 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class PanelEditModule
###########################################################################

class PanelEditModule ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 926,271 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer15 = wx.BoxSizer( wx.VERTICAL )

		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		fgSizer1.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		bSizer162 = wx.BoxSizer( wx.HORIZONTAL )

		self.edit_module_name = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer162.Add( self.edit_module_name, 1, wx.ALL|wx.EXPAND, 5 )


		fgSizer1.Add( bSizer162, 1, wx.EXPAND, 5 )

		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Description", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		fgSizer1.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.edit_module_description = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.edit_module_description, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Comment", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		fgSizer1.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.edit_module_comment = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		self.edit_module_comment.SetMinSize( wx.Size( -1,90 ) )

		fgSizer1.Add( self.edit_module_comment, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer15.Add( fgSizer1, 1, wx.EXPAND, 5 )

		button_module_edit = wx.StdDialogButtonSizer()
		self.button_module_editApply = wx.Button( self, wx.ID_APPLY )
		button_module_edit.AddButton( self.button_module_editApply )
		self.button_module_editCancel = wx.Button( self, wx.ID_CANCEL )
		button_module_edit.AddButton( self.button_module_editCancel )
		button_module_edit.Realize();

		bSizer15.Add( button_module_edit, 0, wx.EXPAND, 5 )


		self.SetSizer( bSizer15 )
		self.Layout()
		self.menu_kicad = wx.Menu()
		self.menu_rebuild_modules = wx.MenuItem( self.menu_kicad, wx.ID_ANY, u"Rebuild modules", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_kicad.Append( self.menu_rebuild_modules )

		self.Bind( wx.EVT_RIGHT_DOWN, self.PanelEditModuleOnContextMenu )


		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.onInitDialog )
		self.button_module_editApply.Bind( wx.EVT_BUTTON, self.onButtonModuleEditApply )
		self.button_module_editCancel.Bind( wx.EVT_BUTTON, self.onButtonModuleEditCancel )
		self.Bind( wx.EVT_MENU, self.onMenuKicadRebuildModulesSelection, id = self.menu_rebuild_modules.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onInitDialog( self, event ):
		event.Skip()

	def onButtonModuleEditApply( self, event ):
		event.Skip()

	def onButtonModuleEditCancel( self, event ):
		event.Skip()

	def onMenuKicadRebuildModulesSelection( self, event ):
		event.Skip()

	def PanelEditModuleOnContextMenu( self, event ):
		self.PopupMenu( self.menu_kicad, event.GetPosition() )


