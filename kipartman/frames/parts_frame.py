from dialogs.panel_parts import PanelParts
from frames.dropdown_dialog import DropdownDialog
from frames.progression_frame import ProgressionFrame
from frames.edit_category_frame import EditCategoryFrame
from frames.edit_part_frame import EditPartFrame, EVT_EDIT_PART_APPLY_EVENT, EVT_EDIT_PART_CANCEL_EVENT
from frames.select_part_parameter_frame import SelectPartParameterFrame
import helper.tree
from helper.filter import Filter
import rest
import wx

import os, datetime
from time import sleep
from octopart.queries import PartsQuery

from octopart.extractor import OctopartExtractor
import swagger_client
from helper.tree import TreeModel


from plugins import plugin_loader
from plugins import import_plugins as import_plugins



# help pages:
# https://wxpython.org/docs/api/wx.gizmos.TreeListCtrl-class.html

        
class DataModelCategory(helper.tree.TreeContainerItem):
    def __init__(self, category):
        super(DataModelCategory, self).__init__()
        self.category = category
        
    def GetValue(self, col):
        vMap = { 
            0 : self.category.name,
            1 : self.category.description,
        }
        return vMap[col]

    def GetAttr(self, col, attr):
        attr.Bold = True
        return True

    def GetDragData(self):
        return {'id': self.category.id}
    
class DataModelCategoryPath(helper.tree.TreeContainerItem):
    def __init__(self, category):
        super(DataModelCategoryPath, self).__init__()
        self.category = category
    
    def GetParam(self, col):
        return None
    
    def GetValue(self, col):
        if self.category:
            path = self.category.path
        else:
            path = "/"
        if col==1:
            return path
        return ''

    def HasContainerColumns(self):
        return True

    def GetAttr(self, col, attr):
        if col==1:
            attr.Bold = True
            return True
        return False

class DataColumnParameter(object):
    def __init__(self, parameter_name):
        self.parameter_name = parameter_name
    
class DataModelPart(helper.tree.TreeContainerLazyItem):
    def __init__(self, part, columns):
        super(DataModelPart, self).__init__()
        self.part = part
        self.columns = columns
        
        self.parameters = {}
        if part.parameters:
            for param in part.parameters:
                self.parameters[param.name] = param 

        if part.has_childs:
            # add a fake item
            self.childs.append(None)
        
    def value_string(self, value, prefix, unit):
        res = ""
        if value is None:
            return res
        res = res+"%g"%value+" "
        if not prefix is None:
            res = res+prefix.symbol
        if not unit is None:
            res = res+unit.symbol
        return res

    def FormatParameter(self, param):
        if param.numeric:
            value = ""
            if param.nom_value is None:
                return value
            value = value+"%g"%param.nom_value+" "
            if param.nom_prefix:
                value = value+param.nom_prefix.symbol
            if param.unit:
                value = value+param.unit.symbol
            return value
        else:
            return param.text_value
    
    def GetParam(self, col):
        if self.parameters.has_key(self.columns[col].parameter_name):
            return self.parameters[self.columns[col].parameter_name]
        return None
        

    def GetValue(self, col):
        if col<6:
            symbol = ''
            if self.part.symbol:
                symbol = os.path.basename(self.part.symbol.source_path).replace('.mod', '')
            footprint = ''
            if self.part.footprint:
                footprint = os.path.basename(self.part.footprint.source_path).replace('.kicad_mod', '')
            
            vMap = { 
                0 : str(self.part.id),
                1 : self.part.name,
                2 : self.part.description,
                3 : self.part.comment,
                4 : symbol,
                5 : footprint
            }
            return vMap[col]
        #if columns are not yet defined
        elif not(col in self.columns):
            return ''
        elif self.parameters.has_key(self.columns[col].parameter_name):
            return self.FormatParameter(self.parameters[self.columns[col].parameter_name])
        else:
            return ''

    def Load(self, manager):
        if self.part.has_childs==False:
            return
        part = rest.api.find_part(self.part.id, with_childs=True)
        
        for child in part.childs:
            manager.AppendItem(self, DataModelPart(child, self.columns))

    def GetDragData(self):
        if isinstance(self.parent, DataModelCategoryPath):
            return {'id': self.part.id}
        return None


class TreeModelParts(TreeModel):
    def __init__(self):
        super(TreeModelParts, self).__init__()
        self.columns = {}

    def Compare(self, item1, item2, column, ascending):
        if self.columns.has_key(column)==False:
            return super(TreeModelParts, self).Compare(item1, item2, column, ascending)
        else:
            obj1 = self.ItemToObject(item1)
            obj2 = self.ItemToObject(item2)

            if obj1:
                param1 = obj1.GetParam(column)
            if obj2:
                param2 = obj2.GetParam(column)
            
            # none element are always treated inferior
            if not param1 and param2:
                return 1
            elif param1 and not param2:
                return -1
            elif not param1 and not param2:
                return super(TreeModelParts, self).Compare(item1, item2, column, ascending)

            if not ascending: # swap sort order?
                param2, param1 = param1, param2

            
            if param1.numeric!=param2.numeric:
                return super(TreeModelParts, self).Compare(item1, item2, column, ascending)

            if param1.numeric==False and param2.numeric==False:
                return helper.tree.CompareString(param1.text_value, param2.text_value)

            if param1.unit and param2.unit and param1.unit!=param2.unit:
                return helper.tree.CompareString(param1.unit.name, param2.unit.name)

            value1 = 0
            if param1.nom_value:
                value1 = param1.nom_value
            if param1.nom_prefix:
                value1 = value1*float(param1.nom_prefix.power)
                
            value2 = 0
            if param2.nom_value:
                value2 = param2.nom_value
            if param2.nom_prefix:
                value2 = value2*float(param2.nom_prefix.power)
            
            if value2>value1:
                return -1
            elif value1>value2:
                return 1
            return 0


class TreeManagerParts(helper.tree.TreeManager):
    def __init__(self, tree_view):
        model = TreeModelParts()
        super(TreeManagerParts, self).__init__(tree_view, model)
        
    def FindPart(self, part_id):
        for data in self.data:
            if isinstance(data, DataModelPart) and isinstance(data.parent, DataModelCategoryPath) and data.part.id==part_id:
                return data
        return None
    
    def FindChildPart(self, parent_part_id, part_id):
        for data in self.data:
            if isinstance(data, DataModelPart) and isinstance(data.parent, DataModelPart) and data.part.id==part_id and data.parent.part.id==parent_part_id:
                return data
        return None

    def FindCategoryPath(self, category):
        if category:
            for data in self.data:
                if isinstance(data, DataModelCategoryPath) and data.category.id==category.id:
                    return data
        else:
            for data in self.data:
                if isinstance(data, DataModelCategoryPath) and data.category is None:
                    return data
        return None
    
    def DeletePart(self, part):
        partobj = self.FindPart(part.id)
        if partobj is None:
            return
        categoryobj = partobj.parent
        self.DeleteItem(partobj.parent, partobj)
        if categoryobj and len(categoryobj.childs)==0:
            self.DeleteItem(categoryobj.parent, categoryobj)

    def DeleteChildPart(self, parent_part, part):
        parentobj = self.FindPart(parent_part.id)
        if parentobj is None:
            return
        partobj = self.FindChildPart(parent_part.id, part.id)
        self.DeleteItem(partobj.parent, partobj)
        self.UpdateItem(parentobj)

    def ExistChildPart(self, parent_part, part):
        if parent_part.childs is None:
            return False
        for child in parent_part.childs:
            if child.id==part.id:
                return True
        return False
    
    def UpdatePart(self, part):
        partobj = self.FindPart(part.id)
        if partobj is None:
            return
        self.UpdateItem(partobj)

    def AppendCategoryPath(self, category):
        categoryobj = self.FindCategoryPath(category)
        if categoryobj:
            return categoryobj
        categoryobj = DataModelCategoryPath(category)
        self.AppendItem(None, categoryobj)
        return categoryobj
    
    def AppendPart(self, part):
        categoryobj = self.AppendCategoryPath(part.category)
        partobj = DataModelPart(part, self.symbol.columns)
        self.AppendItem(categoryobj, partobj)
        self.Expand(categoryobj)
        return partobj
    
    def AppendChildPart(self, parent_part, part):
        parentobj = self.FindPart(parent_part.id)
        partobj = DataModelPart(part, self.symbol.columns)
        self.AppendItem(parentobj, partobj)
        self.Expand(parentobj)
        return partobj

    def AddParameterColumn(self, parameter_name):
        column = self.AddCustomColumn(parameter_name, 'parameter', None)
        self.symbol.columns[column.GetSymbolColumn()] = DataColumnParameter(parameter_name)
        
    def RemoveParameterColumn(self, index):
        if self.symbol.columns.has_key(index)==False:
            return
        self.symbol.columns.pop(index)
        self.RemoveColumn(index)

class PartsFrame(PanelParts): 
    def __init__(self, parent): 
        super(PartsFrame, self).__init__(parent)
        
        # create categories list
        self.tree_categories_manager = helper.tree.TreeManager(self.tree_categories)
        self.tree_categories_manager.AddTextColumn("name")
        self.tree_categories_manager.AddTextColumn("description")
        self.tree_categories_manager.DropAccept(DataModelCategory, self.onTreeCategoriesDropCategory)
        self.tree_categories_manager.DropAccept(DataModelPart, self.onTreeCategoriesDropPart)
        self.tree_categories_manager.OnSelectionChanged = self.onTreeCategoriesSelChanged
        # parts filters
        self.parts_filter = Filter(self.filters_panel, self.onButtonRemoveFilterClick)
        
        # create parts list
        self.tree_parts_manager = TreeManagerParts(self.tree_parts)
        self.tree_parts_manager.AddIntegerColumn("id")
        self.tree_parts_manager.AddTextColumn("name")
        self.tree_parts_manager.AddTextColumn("description")
        self.tree_parts_manager.AddIntegerColumn("comment")
        self.tree_parts_manager.AddTextColumn("symbol")
        self.tree_parts_manager.AddTextColumn("footprint")
        self.tree_parts_manager.OnSelectionChanged = self.onTreePartsSelChanged
        self.tree_parts_manager.OnColumnHeaderRightClick = self.onTreePartsColumnHeaderRightClick
        self.tree_parts_manager.DropAccept(DataModelPart, self.onTreePartsDropPart)
        
        # 
        # create edit part panel
        self.panel_edit_part = EditPartFrame(self.part_splitter)
        self.part_splitter.SplitHorizontally(self.part_splitter.Window1, self.panel_edit_part, 400)
        self.panel_edit_part.Bind( EVT_EDIT_PART_APPLY_EVENT, self.onEditPartApply )
        self.panel_edit_part.Bind( EVT_EDIT_PART_CANCEL_EVENT, self.onEditPartCancel )

        # initial edit state
        self.show_part(None)
        self.edit_state = None
        self.show_categories = True
        
        self.load()
        
    def loadCategories(self):
        # clear all
        self.tree_categories_manager.ClearItems()
        
        # load categories
        categories = rest.api.find_parts_categories()

        # load tree
        to_add = []
        id_category_map = {}
        for category in categories:
            to_add.append(category)
        while len(to_add)>0:
            category = to_add[0]
            id_category_map[category.id] = DataModelCategory(category)
            to_add.pop(0)
            
            # add to symbol
            if category.parent:
                self.tree_categories_manager.AppendItem(id_category_map[category.parent.id], id_category_map[category.id])
            else:
                self.tree_categories_manager.AppendItem(None, id_category_map[category.id])
            
            # load childs
            if category.childs:
                for child in category.childs:
                    to_add.append(child)
        
    def loadParts(self):
        # clear all
        self.tree_parts_manager.ClearItems()
        
        # load parts
        parts = rest.api.find_parts( with_parameters=True, **self.parts_filter.query_filter())

        if self.show_categories:
            # load categories
            categories = {}
            for part in parts:
                if part.category:
                    category_name = part.category.path
                else:
                    category_name = "/"
    
                if categories.has_key(category_name)==False:
                    categories[category_name] = DataModelCategoryPath(part.category)
                    self.tree_parts_manager.AppendItem(None, categories[category_name])
                self.tree_parts_manager.AppendItem(categories[category_name], DataModelPart(part, self.tree_parts_manager.model.columns))
            
            for category in categories:
                self.tree_parts_manager.Expand(categories[category])
        else:
            for part in parts:
                self.tree_parts_manager.AppendItem(None, DataModelPart(part, self.tree_parts_manager.model.columns))
            
    def load(self):
        try:
            self.loadCategories()
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

        try:
            self.loadParts()
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def load_full_part(self, partobj):
        if partobj:
            # read whole part from server
            partobj.part = rest.api.find_part(partobj.part.id, with_offers=True, with_parameters=True, with_childs=True, with_distributors=True, with_manufacturers=True, with_storages=True, with_attachements=True)
        
    def show_part(self, part):
        # disable editing
        self.panel_edit_part.enable(False)
        # enable evrything else
        self.panel_category.Enabled = True
        self.panel_parts.Enabled = True
        # set part
        self.panel_edit_part.SetPart(part)
        
    def edit_part(self, part):
        self.show_part(part)
        # enable editing
        self.panel_edit_part.enable(True)
        # disable evrything else
        self.panel_category.Enabled = False
        self.panel_parts.Enabled = False
        
    def new_part(self):
        part = rest.model.PartNew()
        
        # set category
        item = self.tree_categories.GetSelection()
        if item.IsOk():
            category = self.tree_categories_manager.ItemToObject(item)
            if category.category:
                part.category = category.category

        self.edit_part(part)

    def export_parts(self):

        # exporters = plugin_loader.load_export_plugins()
        # wildcards = '|'.join([x.wildcard for x in exporters])
        # wildcards

        # exportpath=os.path.join(os.getcwd(),'test','TESTimportCSV.csv')
        # exportpath
        # base, ext = os.path.splitext(exportpath)

        # TODO: implement export
        exporters = plugin_loader.load_export_plugins()

        wildcards = '|'.join([x.wildcard for x in exporters])

        export_dialog = wx.FileDialog(self, "Export Parts", "", "",
                                      wildcards,
                                      wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if export_dialog.ShowModal() == wx.ID_CANCEL:
            return

        base, ext = os.path.splitext(export_dialog.GetPath())
        filt_idx = export_dialog.GetFilterIndex()
        # load parts
        parts = rest.api.find_parts(**self.parts_filter.query_filter())

        exporters[filt_idx]().export(base, parts)     
        self.edit_state = None

    def import_parts(self):

        importers = plugin_loader.load_import_plugins()
        wildcards = '|'.join([x.wildcard for x in importers])
        
        import_dialog = wx.FileDialog(self, "Import Parts", "", "",
                                      wildcards,
                                      wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if import_dialog.ShowModal() == wx.ID_CANCEL:
            return

        base, ext = os.path.splitext(import_dialog.GetPath())
        filt_idx = import_dialog.GetFilterIndex()


        # set category
        item = self.tree_categories.GetSelection()
        if item.IsOk():
            category = self.tree_categories_manager.ItemToObject(item)
            if category.category:
                import_items = importers[filt_idx]().fetch(base, category.category, rest.model)
        progression_frame = ProgressionFrame(self, "Importing  parts ") ;
        progression_frame.Show()

        for i, importItem in enumerate(import_items):
            wx.Yield()

            part = rest.model.PartNew()
            # SET imported Parts Fields
            
            part.name = importItem.name
            part.description = importItem.description

            # Update progress indicator
            progression_frame.SetProgression(part.name, i+1, len(import_items))
            if progression_frame.Canceled():
                break


            if isinstance(importItem.footprint, str) and len(importItem.footprint) == 0:  # Blank Footprint
                part.footprint = None
            else:  # Determine or Create correct Footprint References
                searchparam = {'search': importItem.footprint}
                matching_footprints = rest.api.find_footprints(**searchparam)
                if len(matching_footprints)==0: # ADD new footprint
                    # Check Footprint Category: "Uncatagorized" exists
                    try:
                        footprintcategoryid = {i.name: i.id
                                               for i in
                                               rest.api.find_footprints_categories()}['Uncategorized']
                    except KeyError, e:  # Category 'Uncategorized' does not exist
                        # Create the "Uncategorized" category
                        category = rest.model.FootprintCategoryNew()
                        category.name = "Uncategorized"
                        category.description = 'imported footprint names not already defined'
                        category = rest.api.add_footprints_category(category)
                        footprintcategoryid = category.id
                    except:
                            # TODO: handle other errors cleanly
                            raise
                            pass

                    part.footprint = rest.model.FootprintNew()
                    part.footprint.category = rest.model.FootprintCategoryRef(id=footprintcategoryid)
                    part.footprint.name = importItem.footprint
                    part.footprint.description = u''
                    part.footprint.comment = u''

                    # update part on server
                    part.footprint = rest.api.add_footprint(part.footprint)

                elif len(matching_footprints)==1: # only 1 option so referece it
                    part.footprint = matching_footprints[0]
                else:  # multiple Footprint items
                    pass  # TODO: handle if multiple Footprint options exist

            part.comment = 'NEW IMPORT Timestamp:{:%y-%m-%d %H:%M:%S.%f}\n'.format(datetime.datetime.now())
            
            # set category
            if category.category:
                part.category = category.category
            # Update edit_part panel
            try:
                #Lookup details in octopart
                m_octopart = self.import_octopart_lookup(part)
                assert len(m_octopart.data)==1,\
                    'Import Octopart Lookup found {} matchs {}'.format(
                        len(m_octopart.data)
                    )
                octopart_extractor = OctopartExtractor(m_octopart.data[0].json)
                assert part.name == m_octopart.data[0].item().mpn(),\
                    'Import Octopart Lookup found first part {}'.format(
                        m_octopart.data[0].item().mpn()
                    )
                part.octopart_uid = m_octopart.data[0].item().uid()
                part.parameters = []
                part.distributors =[]
                part.manufacturers =[]
                self.octopart_to_part(m_octopart.data[0], part)
                pass
            except Exception as e:
                part.comment = 'RESEARCH REQUIRED - FAILED OCTOPART LOOKUP - Timestamp:{:%y-%m-%d %H:%M:%S.%f}\n'.format(datetime.datetime.now()) \
                                + part.comment
                pass

            self.edit_part(part)
            self.show_part(part)

            try:
                if self.edit_state=='import':
                    part = rest.api.add_part(part)
                    self.tree_parts_manager.AppendPart(part)
            except Exception as e:
                wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
                return
        self.edit_state = None
        self.show_part(part)
        progression_frame.Destroy()

  
    def import_octopart_lookup(self, part):
        df = DummyFrame_import_ocotopart_lookup(None,'Dummy')
        from frames.select_octopart_frame import SelectOctopartFrame
        r = SelectOctopartFrame(df, part.name)
        # print('IMPORT: octopart_lookup:{} found Qty:{}, UID:{}, MPN:{}'.format(
        #     part.name
        #     ,len(r.Children[1].Symbol.data)
        #     , r.Children[1].Symbol.data[0].json['item']['uid']
        #     , r.Children[1].Symbol.data[0].json['item']['mpn']
        #     ))
        df.Destroy()
        return r.Children[1].Symbol


            

    def GetMenus(self):
        return [{'title': 'Parts', 'menu': self.menu_parts}]

    def onButtonRefreshCategoriesClick( self, event ):
        self.loadCategories()

    def onButtonAddCategoryClick( self, event ):
        category = EditCategoryFrame(self).addCategory(rest.model.PartCategoryNew)
        if category:
            try:
                # retrieve parent item from selection
                parentitem = self.tree_categories.GetSelection()
                parentobj = None
                category.parent = None
                if parentitem:
                    parentobj = self.tree_categories_manager.ItemToObject(parentitem)
                    category.parent = parentobj.category
                    
                # create category on server
                category = rest.api.add_parts_category(category)
                # create category on treeview
                newitem = self.tree_categories_manager.AppendItem(parentobj, DataModelCategory(category)) 
                # add category to item element
                self.tree_categories_manager.SelectItem(newitem)
                self.onTreeCategoriesSelChanged(None)
            except Exception as e:
                wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def onButtonEditCategoryClick( self, event ):
        sel = self.tree_categories.GetSelection()
        if sel.IsOk()==False:
            return
        categoryobj = self.tree_categories_manager.ItemToObject(sel)
        if categoryobj is None:
            return
        category = EditCategoryFrame(self).editCategory(categoryobj.category)
        if not category is None:
            try:
                categoryobj.category = rest.api.update_parts_category(categoryobj.category.id, category)
                self.tree_categories_manager.UpdateItem(categoryobj)
                self.onTreeCategoriesSelChanged(None)
            except Exception as e:
                wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def onButtonRemoveCategoryClick( self, event ):
        sel = self.tree_categories.GetSelection()
        categoryobj = self.tree_categories_manager.ItemToObject(sel)
        if categoryobj is None:
            return
        try:
            res = wx.MessageDialog(self, "Remove category '"+categoryobj.category.name+"'", "Remove?", wx.OK|wx.CANCEL).ShowModal()
            if res==wx.ID_OK:
                rest.api.delete_parts_category(categoryobj.category.id)
                self.tree_categories_manager.DeleteItem(categoryobj.parent, categoryobj)
            else:
                return
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)



    def onButtonRemoveFilterClick( self, event ):
        button = event.GetEventObject()
        self.parts_filter.remove(button.GetName())
        self.tree_categories.UnselectAll()
        self.loadParts()


    def onTreeCategoriesSelChanged( self, event ):
        item = self.tree_categories.GetSelection()
        category = None
        if item.IsOk():
            category = self.tree_categories_manager.ItemToObject(item)
        # set category filter
        self.parts_filter.remove('category')
        if category:
            self.parts_filter.add('category', category.category.id, category.category.name)
        # apply new filter and reload
        self.loadParts()

    def onTreeCategoriesDropCategory(self, x, y, data):
        dest_categoryitem, _ = self.tree_categories.HitTest((x, y))
        try:
            source_category_id = data['id']
            source_category = rest.api.find_parts_category(source_category_id)
            source_categoryitem = helper.tree.TreeManager.drag_item
            source_categoryobj = self.tree_categories_manager.ItemToObject(source_categoryitem)
    
            dest_category = None
            dest_categoryobj = None
            if dest_categoryitem.IsOk():
                dest_categoryobj = self.tree_categories_manager.ItemToObject(dest_categoryitem)
                dest_category = dest_categoryobj.category
                if source_category_id==dest_category.id:
                    return wx.DragError
                source_category.parent = rest.model.PartCategoryRef(id=dest_category.id)
            else:
                # set if as root category
                source_category.parent = None
            
            # update on server
            category = rest.api.update_parts_category(source_category.id, source_category)

            # update tree symbol
            if source_categoryobj:
                self.tree_categories_manager.MoveItem(source_categoryobj.parent, dest_categoryobj, source_categoryobj)
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

        return wx.DragMove

    def onTreeCategoriesDropPart(self, x, y, data):
        dest_categoryitem, _ = self.tree_categories.HitTest((x, y))

        try:
            source_part_id = data['id']
            source_part = rest.api.find_part(source_part_id)

            dest_category = None
            dest_categoryobj = None
            if dest_categoryitem.IsOk():
                dest_categoryobj = self.tree_categories_manager.ItemToObject(dest_categoryitem)
                dest_category = dest_categoryobj.category
                source_part.category = rest.model.PartCategoryRef(id=dest_category.id)
            else:
                # set if as root category
                source_part.category = None
            
            # update on server
            part = rest.api.update_part(source_part.id, source_part)
            
            # update tree symbol
            self.tree_parts_manager.DeletePart(source_part)
            self.tree_parts_manager.AppendPart(part)
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
        return wx.DragMove


    def onToggleCategoryPathButton( self, event ):
        self.show_categories = self.toggle_category_path.GetValue()
        self.loadParts()
    
    def onTreePartsSelChanged( self, event ):
        item = self.tree_parts.GetSelection()
        part = None
        if not item.IsOk():
            return
        
        obj = self.tree_parts_manager.ItemToObject(item)
        if isinstance(obj, DataModelPart):
            self.load_full_part(obj)
            part = obj.part
        self.show_part(part)

    def onTreePartsColumnHeaderRightClick( self, event ):
        pos = event.GetPosition()
        # TODO: Nasty hack, this would be better to have a way to pass the column in the event object 
        self.menu_parameters.Column = event.GetDataViewColumn() 
        self.panel_parts.PopupMenu(self.menu_parameters, pos)
        
    def onTreePartsDropPart(self, x, y, data):
        dest_item, _ = self.tree_parts.HitTest((x, y))
        if not dest_item.IsOk():
            return 
        dest_obj = self.tree_parts_manager.ItemToObject(dest_item)
        '''
        @TODO: Additional Use Cases for dragging parts on to lines on the parts list
               USE CASE: 1. Drag a part in the tree_parts onto an line. That is a Category Path
                Essentially changing a parts category
               USE CASE: 2. Drag a category in the tree_parts onto a line That is a Category path
                Essentially changing all items to a sub category of the selected Category path

            PSUEDOCODE: Usecase 1- part to cat
            if isinstance(dest_obj, DataModelCategoryPath) and isinstance(source_obj,DataModelPart)
                dest.obj.tree_categories. onTreeCategoriesDropPart(dest, x, y, data):

            CODE: as per (onTreeCategoriesDropPart)
                try:
                    source_part_id = data['id']
                    source_part = rest.api.find_part(source_part_id)

                    dest_category = None
                    dest_categoryobj = None
                    if dest_categoryitem.IsOk():
                        dest_categoryobj = self.tree_categories_manager.ItemToObject(dest_categoryitem)
                        dest_category = dest_categoryobj.category
                        source_part.category = rest.model.PartCategoryRef(id=dest_category.id)
                    else:
                        # set if as root category
                        source_part.category = None
                    
                    # update on server
                    part = rest.api.update_part(source_part.id, source_part)
                    
                    # update tree symbol
                    self.tree_parts_manager.DeletePart(source_part)
                    self.tree_parts_manager.AppendPart(part)
                except Exception as e:
                    wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
                return wx.DragMove

            PSUEDOCODE: Usecase 2- cat to cat
            if isinstance(dest_obj, DataModelCategoryPath) and isinstance(source_obj,DataModelCategoryPath)
                dest.obj.tree_categories. onTreeCategoriesDropCategory(, x, y, data):
        '''
        if isinstance(dest_obj, DataModelPart): #and isinstance(dest_obj.parent, DataModelCategoryPath):
            try:
                source_part_id = data['id']
                source_partobj = self.tree_parts_manager.FindPart(source_part_id)
    
                dest_part = rest.api.find_part(dest_obj.part.id, with_childs=True)

                if self.tree_parts_manager.ExistChildPart(dest_part, source_partobj.part):
                    wx.MessageBox("Part %s is already a subpart of %s"%(source_partobj.part.name, dest_part.name), 'Error', wx.OK | wx.ICON_ERROR)
                    return wx.DragCancel

                dest_part.childs.append(source_partobj.part)
                rest.api.update_part(dest_part.id, dest_part)

                # update tree symbol
                self.tree_parts_manager.AppendChildPart(dest_part, source_partobj.part)
            except Exception as e:
                wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
                return wx.DragCancel
            return wx.DragMove
        else:
            return wx.DragCancel

    def onMenuParametersAddSelection( self, event ):
        frame = DropdownDialog(self, SelectPartParameterFrame, "")
        frame.DropHere(self.onSelectPartParameterFrameOk)
    
    def onSelectPartParameterFrameOk(self, parameter):
        self.tree_parts_manager.AddParameterColumn(parameter.name)
        
    def onMenuParametersRemoveSelection( self, event ):
        self.tree_parts_manager.RemoveParameterColumn(self.menu_parameters.Column.GetSymbolColumn())
            
    def onEditPartApply( self, event ):
        part = event.data
        try:
            if self.edit_state=='edit':
                # update part on server
                part = rest.api.update_part(part.id, part)
                self.tree_parts_manager.UpdatePart(part)
            elif self.edit_state=='add':
                part = rest.api.add_part(part)
                self.tree_parts_manager.AppendPart(part)
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
            return
        self.edit_state = None
        self.show_part(part)
     
    def onEditPartCancel( self, event ):
        part = None
        item = self.tree_parts.GetSelection()
        if item.IsOk():
            partobj = self.tree_parts_manager.ItemToObject(item)
            self.load_full_part(partobj)
            part = partobj.part
        self.edit_state = None
        self.show_part(part)


    def onButtonAddPartClick( self, event ):
        self.edit_state = 'add'
        self.new_part()

    def onButtonEditPartClick( self, event ):
        item = self.tree_parts.GetSelection()
        if not item.IsOk():
            return
        obj = self.tree_parts_manager.ItemToObject(item)
        if isinstance(obj, DataModelCategoryPath):
            return
        self.load_full_part(obj)
        self.edit_state = 'edit'
        self.edit_part(obj.part)

    def onButtonRemovePartClick( self, event ):
        item = self.tree_parts.GetSelection()
        if not item.IsOk():
            return
        obj = self.tree_parts_manager.ItemToObject(item)
        if isinstance(obj, DataModelCategoryPath):
            return
        part = obj.part
        if isinstance(obj.parent, DataModelPart):
            parent = obj.parent.part
            res = wx.MessageDialog(self, "Remove part '"+part.name+"' from '"+parent.name+"'", "Remove?", wx.OK|wx.CANCEL).ShowModal()
            if res==wx.ID_OK:
                # remove selected part from subparts
                parent = rest.api.find_part(parent.id, with_childs=True)
                for child in parent.childs:
                    if child.id==part.id:
                        parent.childs.remove(child)

                #parent.childs.remove(part)
                rest.api.update_part(parent.id, parent)
                self.tree_parts_manager.DeleteChildPart(parent, part)
            else:
                return 
        else:
            res = wx.MessageDialog(self, "Remove part '"+part.name+"'", "Remove?", wx.OK|wx.CANCEL).ShowModal()
            if res==wx.ID_OK:
                # remove part
                rest.api.delete_part(part.id)
                self.tree_parts_manager.DeletePart(part)
            else:
                return
        self.show_part(None)

    def onMenuItemPartsImportParts( self, event ):
        # TODO: Implement onButtonImportPartsClick
        self.edit_state = 'import'
        self.import_parts()

        pass

    def onMenuItemPartsExportParts( self, event ):
        # TODO: Implement onButtonImportPartsClick
        self.edit_state = 'export'
        self.export_parts()

        pass


    def onSearchPartsTextEnter( self, event ):
        # set search filter
        self.parts_filter.remove('search')
        if self.search_parts.Value!='':
            self.parts_filter.add('search', self.search_parts.Value)
        # apply new filter and reload
        self.loadParts()
 
    def onSearchPartsButton(self, event):
        return self.onSearchPartsTextEnter(event)

    def onButtonRefreshPartsClick( self, event ):
        self.loadParts()

    def OnMenuItem( self, event ):
        # events are not distributed by the frame so we distribute them manually
        if event.GetId()==self.menu_parts_refresh_octopart.GetId():
            self.onMenuItemPartsRefreshOctopart(event)

    def onMenuItemPartsRefreshOctopart( self, event ):
        progression_frame = ProgressionFrame(self, "Refresh parts from Octopart") ;
        progression_frame.Show() ;
        self.Enabled = False 
        
        # get category
        sel = self.tree_categories.GetSelection()
        if sel.IsOk():
            categoryobj = self.tree_categories_manager.ItemToObject(sel)
        else:
            categoryobj = None
        if categoryobj is None:
            parts = rest.api.find_parts()
        else:
            parts = rest.api.find_parts(category=categoryobj.category.id)

        i = 1
        for part in parts:
            wx.Yield()
            
            if part.octopart and part.octopart!="":
                self.refresh_octopart(part)
            
            progression_frame.SetProgression(part.name, i, len(parts)) ;
            if progression_frame.Canceled():
                break
            
            i = i+1

        self.Enabled = True
        progression_frame.Destroy()
        
    
    def refresh_octopart(self, part):
#        print "Refresh octopart for", part.name
        
        # get full part
        part = rest.api.find_part(part.id, with_offers=True, with_parameters=True, with_distributors=True, with_manufacturers=True)
        
        # get octopart data
        q = PartsQuery()
        q.get(part.octopart)
        sleep(1)    # only one request per second allowed

        for octopart in q.results():
            print "octopart:", octopart.json
            if octopart.item().uid()==part.octopart_uid:
                print "Refresh", part.octopart
                self.octopart_to_part(octopart, part)
                # update part
                rest.api.update_part(part.id, part)

        return 
    
    def octopart_to_part(self, octopart, part):
        # convert octopart to part values
        octopart_extractor = OctopartExtractor(octopart)

        # import part fields
        part.name = octopart.item().mpn()
        part.description = octopart.snippet()
        if part.description is None:
            part.description = ""
            
        # set field octopart to indicate that part was imported from octopart
        part.octopart = octopart.item().mpn()
        part.updated = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # import parameters
        for spec_name in octopart.item().specs():
            parameter = octopart_extractor.ExtractParameter(spec_name)            
            
            # check if parameter already exist
            for p in part.parameters:
                if p.name==parameter.name:
                    part.parameters.remove(p)
                    break
            part.parameters.append(parameter)
        
        # remove all offers from distributor prior to add new offers
        for offer in octopart.item().offers():
            distributor_name = offer.seller().name()
            if part.distributors is None:
                return 
            to_remove = []
            for distributor in part.distributors:
                if distributor.name==distributor_name:
                    to_remove.append(distributor)            
            # don't remove in previous loop to avoid missing elements
            for distributor in to_remove:
                part.distributors.remove(distributor)

        # import distributors
        part_distributors = {}
        for offer in octopart.item().offers():
            
            distributor_name = offer.seller().name()
            if part_distributors.has_key(distributor_name)==False:
                distributor = None
                try:
                    distributors = rest.api.find_distributors(name=distributor_name)
                    if len(distributors)>0:
                        distributor = distributors[0]
                    else:
                        # distributor does not exists, create it
                        distributor = rest.model.DistributorNew()
                        distributor.name = offer.seller().name()
                        distributor.website = offer.seller().homepage_url()
                        distributor.allowed = True
                        distributor = rest.api.add_distributor(distributor)
                        
                except Exception as e:
                    wx.MessageBox(format(e), 'Error with distributor %s'%distributor_name, wx.OK | wx.ICON_ERROR)
                
                if distributor:
                    part_distributor = rest.model.PartDistributor()
                    part_distributor.id = distributor.id
                    part_distributor.name = distributor.name
                    part_distributor.offers = []
                    part_distributors[distributor_name] = part_distributor
            
            if part_distributors.has_key(distributor_name):           
                for price_name in offer.prices():
                    for quantity in offer.prices()[price_name]:
                        part_offer = rest.model.PartOffer()
                        part_offer.name = distributor_name
                        part_offer.distributor = distributor
                        part_offer.currency = price_name
                        if offer.moq():
                            part_offer.packaging_unit = offer.moq()
                        else:
                            part_offer.packaging_unit = 1
                        part_offer.quantity = quantity[0]
                        part_offer.unit_price = float(quantity[1])
                        part_offer.sku = offer.sku()
                        part_distributors[distributor_name].offers.append(part_offer)
        # add part_distributors to part
        for distributor_name in part_distributors:
            part.distributors.append(part_distributors[distributor_name])
        
        # import manufacturer
        manufacturer_name = octopart.item().manufacturer().name()
        manufacturer = None
        part.manufacturers = []
        try:
            manufacturers = rest.api.find_manufacturers(name=manufacturer_name)
            if len(manufacturers)>0:
                manufacturer = manufacturers[0]
            else:
                # manufacturer does not exists, create it
                manufacturer = rest.model.ManufacturerNew()
                manufacturer.name = manufacturer_name
                manufacturer.website = octopart.item().manufacturer().homepage_url()
                manufacturer = rest.api.add_manufacturer(manufacturer)

            # add new manufacturer
            part_manufacturer = rest.model.PartManufacturer()
            part_manufacturer.name = manufacturer.name
            part_manufacturer.part_name = part.name
            part.manufacturers.append(part_manufacturer)
        except:
            wx.MessageBox('%s: unknown error retrieving manufacturer' % (manufacturer_name), 'Warning', wx.OK | wx.ICON_EXCLAMATION)

class DummyFrame_import_ocotopart_lookup(wx.Frame):
    def __init__(self, parent, title=""):
        super(DummyFrame_import_ocotopart_lookup, self).__init__(parent, title=title)
        # # Set an application icon
        # self.SetIcon(wx.Icon("appIcon.png"))
        # Set the panel
        self.panel = wx.Panel(self)
