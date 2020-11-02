# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.9.0 Sep 24 2020)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class DialogEditPartParameter
###########################################################################

class DialogEditPartParameter ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 471,360 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Parameter", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		fgSizer1.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.button_search_parameter = wx.Button( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.BU_LEFT )
		fgSizer1.Add( self.button_search_parameter, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Description", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		fgSizer1.Add( self.m_staticText4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.button_parameter_description = wx.Button( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.BU_LEFT )
		self.button_parameter_description.Enable( False )

		fgSizer1.Add( self.button_parameter_description, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"Unit", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		fgSizer1.Add( self.m_staticText5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.button_parameter_unit = wx.Button( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.BU_LEFT )
		self.button_parameter_unit.Enable( False )

		fgSizer1.Add( self.button_parameter_unit, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"Value Type", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )

		fgSizer1.Add( self.m_staticText6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		bSizer61 = wx.BoxSizer( wx.HORIZONTAL )

		self.radio_choice_parameter_integer = wx.RadioButton( self, wx.ID_ANY, u"Integer", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.radio_choice_parameter_integer.Enable( False )

		bSizer61.Add( self.radio_choice_parameter_integer, 0, wx.ALL, 5 )

		self.radio_choice_parameter_float = wx.RadioButton( self, wx.ID_ANY, u"Float", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.radio_choice_parameter_float.Enable( False )

		bSizer61.Add( self.radio_choice_parameter_float, 0, wx.ALL, 5 )

		self.radio_choice_parameter_text = wx.RadioButton( self, wx.ID_ANY, u"Text", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.radio_choice_parameter_text.Enable( False )

		bSizer61.Add( self.radio_choice_parameter_text, 0, wx.ALL, 5 )


		fgSizer1.Add( bSizer61, 1, wx.EXPAND, 5 )

		self.static_text_value = wx.StaticText( self, wx.ID_ANY, u"Value", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.static_text_value.Wrap( -1 )

		fgSizer1.Add( self.static_text_value, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.edit_text_value = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.edit_text_value, 1, wx.ALL|wx.EXPAND, 5 )

		self.static_numeric_value = wx.StaticText( self, wx.ID_ANY, u"Value", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.static_numeric_value.Wrap( -1 )

		fgSizer1.Add( self.static_numeric_value, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		bSizer71 = wx.BoxSizer( wx.HORIZONTAL )

		choice_operator_valueChoices = [ u"=", u"<", u"<=", u">", u">=", u"!=", u"<" ]
		self.choice_operator_value = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_operator_valueChoices, 0 )
		self.choice_operator_value.SetSelection( 0 )
		self.choice_operator_value.Hide()

		bSizer71.Add( self.choice_operator_value, 0, wx.ALL, 5 )

		self.edit_numeric_value = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer71.Add( self.edit_numeric_value, 1, wx.ALL, 5 )

		choice_numeric_value_prefixChoices = []
		self.choice_numeric_value_prefix = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_numeric_value_prefixChoices, 0 )
		self.choice_numeric_value_prefix.SetSelection( 0 )
		bSizer71.Add( self.choice_numeric_value_prefix, 1, wx.ALL, 5 )

		self.show_numeric_value = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY|wx.BORDER_NONE )
		bSizer71.Add( self.show_numeric_value, 1, wx.EXPAND|wx.ALL, 5 )


		fgSizer1.Add( bSizer71, 1, wx.EXPAND, 5 )


		bSizer1.Add( fgSizer1, 1, wx.EXPAND, 5 )

		button_part_edit = wx.StdDialogButtonSizer()
		self.button_part_editApply = wx.Button( self, wx.ID_APPLY )
		button_part_edit.AddButton( self.button_part_editApply )
		self.button_part_editCancel = wx.Button( self, wx.ID_CANCEL )
		button_part_edit.AddButton( self.button_part_editCancel )
		button_part_edit.Realize();

		bSizer1.Add( button_part_edit, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 10 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.button_search_parameter.Bind( wx.EVT_BUTTON, self.onButtonSearchParameterClick )
		self.button_parameter_description.Bind( wx.EVT_BUTTON, self.onButtonSearchParameterClick )
		self.button_parameter_unit.Bind( wx.EVT_BUTTON, self.onButtonSearchParameterClick )
		self.radio_choice_parameter_integer.Bind( wx.EVT_RADIOBUTTON, self.onRadioValueType )
		self.radio_choice_parameter_float.Bind( wx.EVT_RADIOBUTTON, self.onRadioValueType )
		self.radio_choice_parameter_text.Bind( wx.EVT_RADIOBUTTON, self.onRadioValueType )
		self.edit_text_value.Bind( wx.EVT_TEXT, self.onTextValueChanged )
		self.choice_operator_value.Bind( wx.EVT_CHOICE, self.onOperatorValueChoice )
		self.edit_numeric_value.Bind( wx.EVT_TEXT, self.onNumericValueChanged )
		self.choice_numeric_value_prefix.Bind( wx.EVT_CHOICE, self.onNumericValueChanged )
		self.button_part_editApply.Bind( wx.EVT_BUTTON, self.onButtonPartParameterEditApply )
		self.button_part_editCancel.Bind( wx.EVT_BUTTON, self.onButtonPartParameterEditCancel )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onButtonSearchParameterClick( self, event ):
		event.Skip()



	def onRadioValueType( self, event ):
		event.Skip()



	def onTextValueChanged( self, event ):
		event.Skip()

	def onOperatorValueChoice( self, event ):
		event.Skip()

	def onNumericValueChanged( self, event ):
		event.Skip()


	def onButtonPartParameterEditApply( self, event ):
		event.Skip()

	def onButtonPartParameterEditCancel( self, event ):
		event.Skip()


