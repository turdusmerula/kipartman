# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Dec 22 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class PanelEditSymbol
###########################################################################

class PanelEditSymbol ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 926,271 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_splitter3 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter3.Bind( wx.EVT_IDLE, self.m_splitter3OnIdle )
		
		self.m_panel7 = wx.Panel( self.m_splitter3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer15 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText1 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		fgSizer1.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		bSizer162 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.edit_symbol_name = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer162.Add( self.edit_symbol_name, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.button_snapeda = wx.Button( self.m_panel7, wx.ID_ANY, u"SnapEDA", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer162.Add( self.button_snapeda, 0, wx.ALL, 5 )
		
		
		fgSizer1.Add( bSizer162, 1, wx.EXPAND, 5 )
		
		self.m_staticText2 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Description", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		fgSizer1.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.edit_symbol_description = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.edit_symbol_description, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText3 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Comment", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		fgSizer1.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.edit_symbol_comment = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		self.edit_symbol_comment.SetMinSize( wx.Size( -1,90 ) )
		
		fgSizer1.Add( self.edit_symbol_comment, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText42 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Snapeda", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText42.Wrap( -1 )
		fgSizer1.Add( self.m_staticText42, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		bSizer172 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_open_url_snapeda = wx.Button( self.m_panel7, wx.ID_ANY, u"<None>", wx.DefaultPosition, wx.DefaultSize, wx.BU_LEFT|wx.NO_BORDER )
		bSizer172.Add( self.button_open_url_snapeda, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.button_remove_url_snapeda = wx.BitmapButton( self.m_panel7, wx.ID_ANY, wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer172.Add( self.button_remove_url_snapeda, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		fgSizer1.Add( bSizer172, 1, wx.EXPAND, 5 )
		
		
		bSizer15.Add( fgSizer1, 1, wx.EXPAND, 5 )
		
		button_symbol_edit = wx.StdDialogButtonSizer()
		self.button_symbol_editApply = wx.Button( self.m_panel7, wx.ID_APPLY )
		button_symbol_edit.AddButton( self.button_symbol_editApply )
		self.button_symbol_editCancel = wx.Button( self.m_panel7, wx.ID_CANCEL )
		button_symbol_edit.AddButton( self.button_symbol_editCancel )
		button_symbol_edit.Realize();
		
		bSizer15.Add( button_symbol_edit, 0, wx.EXPAND, 5 )
		
		
		self.m_panel7.SetSizer( bSizer15 )
		self.m_panel7.Layout()
		bSizer15.Fit( self.m_panel7 )
		self.panel_image_symbol = wx.Panel( self.m_splitter3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer16 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_edit_ = wx.Button( self.panel_image_symbol, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.button_edit_.Hide()
		
		bSizer6.Add( self.button_edit_, 0, wx.ALL, 5 )
		
		self.m_button4 = wx.Button( self.panel_image_symbol, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button4.Hide()
		
		bSizer6.Add( self.m_button4, 0, wx.ALL, 5 )
		
		
		bSizer16.Add( bSizer6, 0, wx.EXPAND, 5 )
		
		self.bitmap_edit_symbol = wx.StaticBitmap( self.panel_image_symbol, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer16.Add( self.bitmap_edit_symbol, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.panel_image_symbol.SetSizer( bSizer16 )
		self.panel_image_symbol.Layout()
		bSizer16.Fit( self.panel_image_symbol )
		self.m_splitter3.SplitVertically( self.m_panel7, self.panel_image_symbol, 0 )
		bSizer1.Add( self.m_splitter3, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		self.menu_kicad = wx.Menu()
		self.menu_rebuild_symbols = wx.MenuItem( self.menu_kicad, wx.ID_ANY, u"Rebuild symbols", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_kicad.Append( self.menu_rebuild_symbols )
		
		self.Bind( wx.EVT_RIGHT_DOWN, self.PanelEditSymbolOnContextMenu ) 
		
		
		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.onInitDialog )
		self.button_snapeda.Bind( wx.EVT_BUTTON, self.onButtonSnapedaClick )
		self.button_open_url_snapeda.Bind( wx.EVT_BUTTON, self.onButtonOpenUrlSnapedaClick )
		self.button_remove_url_snapeda.Bind( wx.EVT_BUTTON, self.onButtonRemoveUrlSnapedaClick )
		self.button_symbol_editApply.Bind( wx.EVT_BUTTON, self.onButtonSymbolEditApply )
		self.button_symbol_editCancel.Bind( wx.EVT_BUTTON, self.onButtonSymbolEditCancel )
		self.Bind( wx.EVT_MENU, self.onMenuKicadRebuildSymbolsSelection, id = self.menu_rebuild_symbols.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onInitDialog( self, event ):
		event.Skip()
	
	def onButtonSnapedaClick( self, event ):
		event.Skip()
	
	def onButtonOpenUrlSnapedaClick( self, event ):
		event.Skip()
	
	def onButtonRemoveUrlSnapedaClick( self, event ):
		event.Skip()
	
	def onButtonSymbolEditApply( self, event ):
		event.Skip()
	
	def onButtonSymbolEditCancel( self, event ):
		event.Skip()
	
	def onMenuKicadRebuildSymbolsSelection( self, event ):
		event.Skip()
	
	def m_splitter3OnIdle( self, event ):
		self.m_splitter3.SetSashPosition( 0 )
		self.m_splitter3.Unbind( wx.EVT_IDLE )
	
	def PanelEditSymbolOnContextMenu( self, event ):
		self.PopupMenu( self.menu_kicad, event.GetPosition() )
		

