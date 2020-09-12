from dialogs.panel_parts import PanelParts
import frames
from frames.part_categories_frame import PartCategoriesFrame
from frames.part_list_frame import PartListFrame
import helper.filter
import api.data.part
import wx
from helper.exception import print_stack

# from frames.dropdown_dialog import DropdownDialog
# from frames.progression_frame import ProgressionFrame
# from frames.edit_category_frame import EditCategoryFrame
# from frames.select_part_parameter_frame import SelectPartParameterFrame
# import helper.tree
# import wx
# 
# import os, datetime
# from time import sleep
# from octopart.queries import PartsQuery
# 
# from octopart.extractor import OctopartExtractor
# import swagger_client
# from helper.tree import TreeModel
# 
# from helper.part_updater import PartReferenceUpdater
# 

# class DataColumnParameter(object):
#     def __init__(self, parameter_name):
#         self.parameter_name = parameter_name
#     
# class DataModelPart(helper.tree.TreeContainerLazyItem):
#     def __init__(self, part, columns):
#         super(DataModelPart, self).__init__()
#         self.part = part
#         self.columns = columns
#         
#         self.parameters = {}
#         if part.parameters:
#             for param in part.parameters:
#                 self.parameters[param.name] = param 
# 
#         if part.has_childs:
#             # add a fake item
#             self.childs.append(None)
#         
#     def value_string(self, value, prefix, unit):
#         res = ""
#         if value is None:
#             return res
#         res = res+"%g"%value+" "
#         if not prefix is None:
#             res = res+prefix.symbol
#         if not unit is None:
#             res = res+unit.symbol
#         return res
# 
#     def FormatParameter(self, param):
#         if param.numeric:
#             value = ""
#             if param.nom_value is None:
#                 return value
#             value = value+"%g"%param.nom_value+" "
#             if param.nom_prefix:
#                 value = value+param.nom_prefix.symbol
#             if param.unit:
#                 value = value+param.unit.symbol
#             return value
#         else:
#             return param.text_value
#     
#     def GetParam(self, col):
#         if self.columns[col].parameter_name in self.parameters:
#             return self.parameters[self.columns[col].parameter_name]
#         return None
#         
# 
#     def GetValue(self, col):
#         if col<6:
#             symbol = ''
#             if self.part.symbol:
#                 symbol = os.path.basename(self.part.symbol.source_path).replace('.mod', '')
#             footprint = ''
#             if self.part.footprint:
#                 footprint = os.path.basename(self.part.footprint.source_path).replace('.kicad_mod', '')
#             
#             vMap = { 
#                 0 : str(self.part.id),
#                 1 : self.part.name,
#                 2 : self.part.description,
#                 3 : self.part.comment,
#                 4 : symbol,
#                 5 : footprint
#             }
#             return vMap[col]
#         #if columns are not yet defined
#         elif not(col in self.columns):
#             return ''
#         elif self.columns[col].parameter_name in self.parameters:
#             return self.FormatParameter(self.parameters[self.columns[col].parameter_name])
#         else:
#             return ''
# 
#     def Load(self, manager):
#         if self.part.has_childs==False:
#             return
#         part = rest.api.find_part(self.part.id, with_childs=True)
#         
#         for child in part.childs:
#             manager.AppendItem(self, DataModelPart(child, self.columns))
# 
#     def GetDragData(self):
#         if isinstance(self.parent, DataModelCategoryPath):
#             return {'id': self.part.id}
#         return None
# 
# 
# class TreeModelParts(TreeModel):
#     def __init__(self):
#         super(TreeModelParts, self).__init__()
#         self.columns = {}
# 
#     def Compare(self, item1, item2, column, ascending):
#         if column not in self.columns:
#             return super(TreeModelParts, self).Compare(item1, item2, column, ascending)
#         else:
#             obj1 = self.ItemToObject(item1)
#             obj2 = self.ItemToObject(item2)
# 
#             if obj1:
#                 param1 = obj1.GetParam(column)
#             if obj2:
#                 param2 = obj2.GetParam(column)
#             
#             # none element are always treated inferior
#             if not param1 and param2:
#                 return 1
#             elif param1 and not param2:
#                 return -1
#             elif not param1 and not param2:
#                 return super(TreeModelParts, self).Compare(item1, item2, column, ascending)
# 
#             if not ascending: # swap sort order?
#                 param2, param1 = param1, param2
# 
#             
#             if param1.numeric!=param2.numeric:
#                 return super(TreeModelParts, self).Compare(item1, item2, column, ascending)
# 
#             if param1.numeric==False and param2.numeric==False:
#                 return helper.tree.CompareString(param1.text_value, param2.text_value)
# 
#             if param1.unit and param2.unit and param1.unit!=param2.unit:
#                 return helper.tree.CompareString(param1.unit.name, param2.unit.name)
# 
#             value1 = 0
#             if param1.nom_value:
#                 value1 = param1.nom_value
#             if param1.nom_prefix:
#                 value1 = value1*float(param1.nom_prefix.power)
#                 
#             value2 = 0
#             if param2.nom_value:
#                 value2 = param2.nom_value
#             if param2.nom_prefix:
#                 value2 = value2*float(param2.nom_prefix.power)
#             
#             if value2>value1:
#                 return -1
#             elif value1>value2:
#                 return 1
#             return 0
# 
# 
# class TreeManagerParts(helper.tree.TreeManager):
#     def __init__(self, tree_view, *args, **kwargs):
#         model = TreeModelParts()
#         super(TreeManagerParts, self).__init__(tree_view, model, *args, **kwargs)
#         
#     def FindPart(self, part_id):
#         for data in self.data:
#             if isinstance(data, DataModelPart) and isinstance(data.parent, DataModelCategoryPath) and data.part.id==part_id:
#                 return data
#         return None
#     
#     def FindChildPart(self, parent_part_id, part_id):
#         for data in self.data:
#             if isinstance(data, DataModelPart) and isinstance(data.parent, DataModelPart) and data.part.id==part_id and data.parent.part.id==parent_part_id:
#                 return data
#         return None
# 
#     def FindCategoryPath(self, category):
#         if category:
#             for data in self.data:
#                 if isinstance(data, DataModelCategoryPath) and data.category.id==category.id:
#                     return data
#         else:
#             for data in self.data:
#                 if isinstance(data, DataModelCategoryPath) and data.category is None:
#                     return data
#         return None
#     
#     def DeletePart(self, part):
#         partobj = self.FindPart(part.id)
#         if partobj is None:
#             return
#         categoryobj = partobj.parent
#         self.DeleteItem(partobj.parent, partobj)
#         if categoryobj and len(categoryobj.childs)==0:
#             self.DeleteItem(categoryobj.parent, categoryobj)
# 
#     def DeleteChildPart(self, parent_part, part):
#         parentobj = self.FindPart(parent_part.id)
#         if parentobj is None:
#             return
#         partobj = self.FindChildPart(parent_part.id, part.id)
#         self.DeleteItem(partobj.parent, partobj)
#         self.UpdateItem(parentobj)
# 
#     def ExistChildPart(self, parent_part, part):
#         if parent_part.childs is None:
#             return False
#         for child in parent_part.childs:
#             if child.id==part.id:
#                 return True
#         return False
#     
#     def UpdatePart(self, part):
#         partobj = self.FindPart(part.id)
#         if partobj is None:
#             return
#         self.UpdateItem(partobj)
# 
#     def AppendCategoryPath(self, category):
#         categoryobj = self.FindCategoryPath(category)
#         if categoryobj:
#             return categoryobj
#         categoryobj = DataModelCategoryPath(category)
#         self.AppendItem(None, categoryobj)
#         return categoryobj
#     
#     def AppendPart(self, part):
#         categoryobj = self.AppendCategoryPath(part.category)
#         partobj = DataModelPart(part, self.model.columns)
#         self.AppendItem(categoryobj, partobj)
#         self.Expand(categoryobj)
#         return partobj
#     
#     def AppendChildPart(self, parent_part, part):
#         parentobj = self.FindPart(parent_part.id)
#         partobj = DataModelPart(part, self.model.columns)
#         self.AppendItem(parentobj, partobj)
#         self.Expand(parentobj)
#         return partobj
# 
#     def AddParameterColumn(self, parameter_name):
#         column = self.AddCustomColumn(parameter_name, 'parameter', None)
#         self.model.columns[column.GetModelColumn()] = DataColumnParameter(parameter_name)
#         
#     def RemoveParameterColumn(self, index):
#         if index not in self.model.columns:
#             return
#         self.model.columns.pop(index)
#         self.RemoveColumn(index)
# 
class PartsFrame(PanelParts): 
    def __init__(self, parent): 
        super(PartsFrame, self).__init__(parent)
        

        # add categories panel
        self.panel_categories = PartCategoriesFrame(self.splitter_vert, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.panel_categories.Bind( frames.part_categories_frame.EVT_SELECT_CATEGORY, self.onPartCategoriesSelectionChanged )
        
        # add part list panel
        self.panel_part_list = PartListFrame(self.splitter_vert, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.panel_part_list.Bind( frames.part_list_frame.EVT_ENTER_EDIT_MODE, self.onPartsEnterEditMode )
        self.panel_part_list.Bind( frames.part_list_frame.EVT_EXIT_EDIT_MODE, self.onPartsExitEditMode )
        self.panel_part_list.Filters.Bind( helper.filter.EVT_FILTER_CHANGED, self.onPartsFilterChanged )

        # organize panels
        self.splitter_vert.Unsplit()
        self.splitter_vert.SplitVertically( self.panel_categories, self.panel_part_list)
        self.panel_left.Hide()
        self.panel_right.Hide()

    def activate(self):
        self.panel_categories.activate()
        self.panel_part_list.activate()

    
    def GetMenus(self):
        return None
    
    def onPartCategoriesSelectionChanged( self, event ):
        self.panel_part_list.Filters.replace(api.data.part.FilterCategory(event.category), 'category')
        event.Skip()

    def onPartsFilterChanged( self, event ):
        if len(self.panel_part_list.Filters.get_filters_group('category'))==0:
            self.panel_categories.UnselectAll()
        event.Skip()

    def onPartsEnterEditMode( self, event ):
        self.panel_categories.Enabled = False
        event.Skip()

    def onPartsExitEditMode( self, event ):
        self.panel_categories.Enabled = True
        event.Skip()

#     def import_octopart_lookup(self, part):
#         df = DummyFrame_import_ocotopart_lookup(None,'Dummy')
#         from frames.select_octopart_frame import SelectOctopartFrame
#         r = SelectOctopartFrame(df, part.name)
#         df.Destroy()
#         return r.Children[1].Symbol
# 
# 
#             
# 
#     def GetMenus(self):
#         return [{'title': 'Parts', 'menu': self.menu_parts}]
# 
#     def onButtonRefreshCategoriesClick( self, event ):
#         self.loadCategories()
# 
# 
#     def onMenuCategoryAddCategory( self, event ):
#         category = EditCategoryFrame(self).addCategory(rest.model.PartCategoryNew)
#         if category:
#             try:
#                 # retrieve parent item from selection
#                 parentitem = self.tree_categories.GetSelection()
#                 parentobj = None
#                 category.parent = None
#                 if parentitem:
#                     parentobj = self.tree_categories_manager.ItemToObject(parentitem)
#                     category.parent = parentobj.category
#                     
#                 # create category on server
#                 category = rest.api.add_parts_category(category)
#                 # create category on treeview
#                 newitem = self.tree_categories_manager.AppendItem(parentobj, DataModelCategory(category)) 
#                 # add category to item element
#                 self.tree_categories_manager.SelectItem(newitem)
#                 self.onTreeCategoriesSelChanged(None)
#             except Exception as e:
#                 print_stack()
#                 wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
# 
#     def onMenuCategoryEditCategory( self, event ):
#         sel = self.tree_categories.GetSelection()
#         if sel.IsOk()==False:
#             return
#         categoryobj = self.tree_categories_manager.ItemToObject(sel)
#         if categoryobj is None:
#             return
#         category = EditCategoryFrame(self).editCategory(categoryobj.category)
#         if not category is None:
#             try:
#                 categoryobj.category = rest.api.update_parts_category(categoryobj.category.id, category)
#                 self.tree_categories_manager.UpdateItem(categoryobj)
#                 self.onTreeCategoriesSelChanged(None)
#             except Exception as e:
#                 print_stack()
#                 wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
# 
#     def onMenuCategoryRemoveCategory( self, event ):
#         sel = self.tree_categories.GetSelection()
#         categoryobj = self.tree_categories_manager.ItemToObject(sel)
#         if categoryobj is None:
#             return
#         try:
#             res = wx.MessageDialog(self, "Remove category '"+categoryobj.category.name+"'", "Remove?", wx.OK|wx.CANCEL).ShowModal()
#             if res==wx.ID_OK:
#                 rest.api.delete_parts_category(categoryobj.category.id)
#                 self.tree_categories_manager.DeleteItem(categoryobj.parent, categoryobj)
#             else:
#                 return
#         except Exception as e:
#             print_stack()
#             wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
# 
# 
# 
#     def onButtonRemoveFilterClick( self, event ):
#         button = event.GetEventObject()
#         self.parts_filter.remove(button.GetName())
#         self.tree_categories.UnselectAll()
#         self.loadParts()
# 
# 
#     def onTreeCategoriesSelChanged( self, event ):
#         item = self.tree_categories.GetSelection()
#         category = None
#         if item.IsOk():
#             category = self.tree_categories_manager.ItemToObject(item)
#         # set category filter
#         self.parts_filter.remove('category')
#         if category:
#             self.parts_filter.add('category', category.category.id, category.category.name)
#         # apply new filter and reload
#         self.loadParts()
# 
#     def onTreeCategoriesBeforeContextMenu( self, event ):
#         item = self.tree_categories.GetSelection()
#         obj = None
#         if item.IsOk():
#             obj = self.tree_categories_manager.ItemToObject(item)
# 
#         self.menu_category_add_category.Enable(True)
#         self.menu_category_edit_category.Enable(True)
#         self.menu_category_remove_category.Enable(True)
#         if isinstance(obj, DataModelCategory)==False:
#             self.menu_category_edit_category.Enable(False)
#             self.menu_category_remove_category.Enable(False)
# 
#     def onTreeCategoriesDropCategory(self, x, y, data):
#         dest_categoryitem, _ = self.tree_categories.HitTest((x, y))
#         try:
#             source_category_id = data['id']
#             source_category = rest.api.find_parts_category(source_category_id)
#             source_categoryitem = helper.tree.TreeManager.drag_item
#             source_categoryobj = self.tree_categories_manager.ItemToObject(source_categoryitem)
#     
#             dest_category = None
#             dest_categoryobj = None
#             if dest_categoryitem.IsOk():
#                 dest_categoryobj = self.tree_categories_manager.ItemToObject(dest_categoryitem)
#                 dest_category = dest_categoryobj.category
#                 if source_category_id==dest_category.id:
#                     return wx.DragError
#                 source_category.parent = rest.model.PartCategoryRef(id=dest_category.id)
#             else:
#                 # set if as root category
#                 source_category.parent = None
#             
#             # update on server
#             category = rest.api.update_parts_category(source_category.id, source_category)
# 
#             # update tree symbol
#             if source_categoryobj:
#                 self.tree_categories_manager.MoveItem(source_categoryobj.parent, dest_categoryobj, source_categoryobj)
#         except Exception as e:
#             print_stack()
#             wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
# 
#         return wx.DragMove
# 
#     def onTreeCategoriesDropPart(self, x, y, data):
#         dest_categoryitem, _ = self.tree_categories.HitTest((x, y))
# 
#         try:
#             source_part_id = data['id']
#             source_part = rest.api.find_part(source_part_id)
# 
#             dest_category = None
#             dest_categoryobj = None
#             if dest_categoryitem.IsOk():
#                 dest_categoryobj = self.tree_categories_manager.ItemToObject(dest_categoryitem)
#                 dest_category = dest_categoryobj.category
#                 source_part.category = rest.model.PartCategoryRef(id=dest_category.id)
#             else:
#                 # set if as root category
#                 source_part.category = None
#             
#             # update on server
#             part = rest.api.update_part(source_part.id, source_part)
#             
#             # update tree symbol
#             self.tree_parts_manager.DeletePart(source_part)
#             self.tree_parts_manager.AppendPart(part)
#         except Exception as e:
#             print_stack()
#             wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
#         return wx.DragMove
# 
# 
#     def onToggleCategoryPathClicked( self, event ):
#         self.show_categories = self.toolbar_part.GetToolState(self.toggle_part_path.GetId())
#         self.loadParts()
#     
#     def onTreePartsSelChanged( self, event ):
#         item = self.tree_parts.GetSelection()
#         part = None
#         if not item.IsOk():
#             return
#         
#         obj = self.tree_parts_manager.ItemToObject(item)
#         if isinstance(obj, DataModelPart):
#             self.load_full_part(obj)
#             part = obj.part
#         self.show_part(part)
# 
#     def onTreePartsBeforeContextMenu( self, event ):
#         item = self.tree_parts.GetSelection()
#         obj = None
#         if item.IsOk():
#             obj = self.tree_parts_manager.ItemToObject(item)
# 
#         self.menu_part_add_part.Enable(True)
#         self.menu_part_edit_part.Enable(True)
#         self.menu_part_remove_part.Enable(True)
#         self.menu_part_duplicate_part.Enable(True)
#         if isinstance(obj, DataModelPart)==False:
#             self.menu_part_edit_part.Enable(False)
#             self.menu_part_remove_part.Enable(False)
#             self.menu_part_duplicate_part.Enable(False)
# 
#     def onTreePartsColumnHeaderRightClick( self, event ):
#         pos = event.GetPosition()
#         # TODO: Nasty hack, this would be better to have a way to pass the column in the event object 
#         self.menu_parameters.Column = event.GetDataViewColumn() 
#         self.panel_parts.PopupMenu(self.menu_parameters, pos)
#         
#     def onTreePartsDropPart(self, x, y, data):
#         dest_item, _ = self.tree_parts.HitTest((x, y))
#         if not dest_item.IsOk():
#             return 
#         dest_obj = self.tree_parts_manager.ItemToObject(dest_item)
#         '''
#         @TODO: Additional Use Cases for dragging parts on to lines on the parts list
#                USE CASE: 1. Drag a part in the tree_parts onto an line. That is a Category Path
#                 Essentially changing a parts category
#                USE CASE: 2. Drag a category in the tree_parts onto a line That is a Category path
#                 Essentially changing all items to a sub category of the selected Category path
# 
#             PSUEDOCODE: Usecase 1- part to cat
#             if isinstance(dest_obj, DataModelCategoryPath) and isinstance(source_obj,DataModelPart)
#                 dest.obj.tree_categories. onTreeCategoriesDropPart(dest, x, y, data):
# 
#             CODE: as per (onTreeCategoriesDropPart)
#                 try:
#                     source_part_id = data['id']
#                     source_part = rest.api.find_part(source_part_id)
# 
#                     dest_category = None
#                     dest_categoryobj = None
#                     if dest_categoryitem.IsOk():
#                         dest_categoryobj = self.tree_categories_manager.ItemToObject(dest_categoryitem)
#                         dest_category = dest_categoryobj.category
#                         source_part.category = rest.model.PartCategoryRef(id=dest_category.id)
#                     else:
#                         # set if as root category
#                         source_part.category = None
#                     
#                     # update on server
#                     part = rest.api.update_part(source_part.id, source_part)
#                     
#                     # update tree model
#                     self.tree_parts_manager.DeletePart(source_part)
#                     self.tree_parts_manager.AppendPart(part)
#                 except Exception as e:
#                     print_stack()
#                     wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
#                 return wx.DragMove
# 
#             PSUEDOCODE: Usecase 2- cat to cat
#             if isinstance(dest_obj, DataModelCategoryPath) and isinstance(source_obj,DataModelCategoryPath)
#                 dest.obj.tree_categories. onTreeCategoriesDropCategory(, x, y, data):
#         '''
#         if isinstance(dest_obj, DataModelPart): #and isinstance(dest_obj.parent, DataModelCategoryPath):
#             try:
#                 source_part_id = data['id']
#                 source_partobj = self.tree_parts_manager.FindPart(source_part_id)
#     
#                 dest_part = rest.api.find_part(dest_obj.part.id, with_childs=True)
# 
#                 if self.tree_parts_manager.ExistChildPart(dest_part, source_partobj.part):
#                     wx.MessageBox("Part %s is already a subpart of %s"%(source_partobj.part.name, dest_part.name), 'Error', wx.OK | wx.ICON_ERROR)
#                     return wx.DragCancel
# 
#                 dest_part.childs.append(source_partobj.part)
#                 rest.api.update_part(dest_part.id, dest_part)
# 
#                 # update tree symbol
#                 self.tree_parts_manager.AppendChildPart(dest_part, source_partobj.part)
#             except Exception as e:
#                 print_stack()
#                 wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
#                 return wx.DragCancel
#             return wx.DragMove
#         else:
#             return wx.DragCancel
# 
#     def onMenuParametersAddSelection( self, event ):
#         frame = DropdownDialog(self, SelectPartParameterFrame, "")
#         frame.DropHere(self.onSelectPartParameterFrameOk)
#     
#     def onSelectPartParameterFrameOk(self, parameter):
#         self.tree_parts_manager.AddParameterColumn(parameter.name)
#         
#     def onMenuParametersRemoveSelection( self, event ):
#         self.tree_parts_manager.RemoveParameterColumn(self.menu_parameters.Column.GetModelColumn())
#             
# 
# # 
#     def onMenuItemPartsImportParts( self, event ):
#         # TODO: Implement onButtonImportPartsClick
#         self.edit_state = 'import'
#         self.import_parts()
# 
#         pass
# 
#     def onMenuItemPartsExportParts( self, event ):
#         # TODO: Implement onButtonImportPartsClick
#         self.edit_state = 'export'
#         self.export_parts()
# 
#         pass
# 
# 
#     def onSearchPartsTextEnter( self, event ):
#         # set search filter
#         self.parts_filter.remove('search')
#         if self.search_parts.Value!='':
#             self.parts_filter.add('search', self.search_parts.Value)
#         # apply new filter and reload
#         self.loadParts()
#  
#     def onSearchPartsButton(self, event):
#         return self.onSearchPartsTextEnter(event)
# 
#     def onButtonRefreshPartsClick( self, event ):
#         self.loadParts()
# 
#     def OnMenuItem( self, event ):
#         # events are not distributed by the frame so we distribute them manually
#         if event.GetId()==self.menu_parts_refresh_octopart.GetId():
#             self.onMenuItemPartsRefreshOctopart(event)
# 
#     def onMenuItemPartsRefreshOctopart( self, event ):
#         progression_frame = ProgressionFrame(self, "Refresh parts from Octopart") ;
#         progression_frame.Show() ;
#         self.Enabled = False 
#         
#         # get category
#         sel = self.tree_categories.GetSelection()
#         if sel.IsOk():
#             categoryobj = self.tree_categories_manager.ItemToObject(sel)
#         else:
#             categoryobj = None
#         if categoryobj is None:
#             parts = rest.api.find_parts()
#         else:
#             parts = rest.api.find_parts(category=categoryobj.category.id)
# 
#         i = 1
#         for part in parts:
#             wx.Yield()
#             
#             if part.octopart and part.octopart!="":
#                 self.refresh_octopart(part)
#             
#             progression_frame.SetProgression(part.name, i, len(parts)) ;
#             if progression_frame.Canceled():
#                 break
#             
#             i = i+1
# 
#         self.Enabled = True
#         progression_frame.Destroy()
#         self.loadParts()
# 
#     def onMenuPartRefreshOctopartPart(self, event):
#         item = self.tree_parts.GetSelection()
#         if not item.IsOk():
#             return
#         obj = self.tree_parts_manager.ItemToObject(item)
#         if isinstance(obj, DataModelCategoryPath):
#             return
#         part = obj.part
#     
#         self.refresh_octopart(part)
#         self.show_part(part)
# 
#     def refresh_octopart(self, part):
#         print("Refresh octopart for", part.name)
#         
#         updater = PartReferenceUpdater()
#         updater.refresh_distributors(part)
#         
#         return 
#     
# class DummyFrame_import_ocotopart_lookup(wx.Frame):
#     def __init__(self, parent, title=""):
#         super(DummyFrame_import_ocotopart_lookup, self).__init__(parent, title=title)
#         # # Set an application icon
#         # self.SetIcon(wx.Icon("appIcon.png"))
#         # Set the panel
#         self.panel = wx.Panel(self)

