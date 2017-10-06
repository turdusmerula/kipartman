from dialogs.panel_parts import PanelParts
from frames.progression_frame import ProgressionFrame
from frames.edit_category_frame import EditCategoryFrame
from frames.edit_part_frame import EditPartFrame, EVT_EDIT_PART_APPLY_EVENT, EVT_EDIT_PART_CANCEL_EVENT
import helper.tree
from helper.filter import Filter
import rest
import wx
from time import sleep
from octopart.queries import PartsQuery
import datetime
from octopart.extractor import OctopartExtractor

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
    
class DataModelPart(helper.tree.TreeContainerLazyItem):
    def __init__(self, part):
        super(DataModelPart, self).__init__()
        self.part = part
        if part.has_childs:
            # add a fake item
            self.childs.append(None)
            
    def GetValue(self, col):
        vMap = { 
            0 : str(self.part.id),
            1 : self.part.name,
            2 : self.part.description,
            3 : self.part.comment
        }
        return vMap[col]

    def Load(self, manager):
        if self.part.has_childs==False:
            return
        part = rest.api.find_part(self.part.id, with_childs=True)
        
        for child in part.childs:
            manager.AppendItem(self, DataModelPart(child))

    def GetDragData(self):
        if isinstance(self.parent, DataModelCategoryPath):
            return {'id': self.part.id}
        return None


class TreeManagerParts(helper.tree.TreeManager):
    def __init__(self, tree_view):
        super(TreeManagerParts, self).__init__(tree_view)

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
        partobj = DataModelPart(part)
        self.AppendItem(categoryobj, partobj)
        self.Expand(categoryobj)
        return partobj
    
    def AppendChildPart(self, parent_part, part):
        parentobj = self.FindPart(parent_part.id)
        partobj = DataModelPart(part)
        self.AppendItem(parentobj, partobj)
        self.Expand(parentobj)
        return partobj

        
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
        self.tree_parts_manager.OnSelectionChanged = self.onTreePartsSelChanged
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
            
            # add to model
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
        parts = rest.api.find_parts(**self.parts_filter.query_filter())

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
            self.tree_parts_manager.AppendItem(categories[category_name], DataModelPart(part))
        
        for category in categories:
            self.tree_parts_manager.Expand(categories[category])
                
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

            # update tree model
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
            
            # update tree model
            self.tree_parts_manager.DeletePart(source_part)
            self.tree_parts_manager.AppendPart(part)
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
        return wx.DragMove


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

    def onTreePartsDropPart(self, x, y, data):
        dest_item, _ = self.tree_parts.HitTest((x, y))
        if not dest_item.IsOk():
            return 
        dest_obj = self.tree_parts_manager.ItemToObject(dest_item)
        if isinstance(dest_obj, DataModelPart) and isinstance(dest_obj.parent, DataModelCategoryPath):
            try:
                source_part_id = data['id']
                source_partobj = self.tree_parts_manager.FindPart(source_part_id)
    
                dest_part = rest.api.find_part(dest_obj.part.id, with_childs=True)
                dest_part.childs.append(source_partobj.part)
                
                rest.api.update_part(dest_part.id, dest_part)
                # update tree model
                self.tree_parts_manager.AppendChildPart(dest_part, source_partobj.part)
            except Exception as e:
                wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
            return wx.DragMove

            
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
            
        # set field octopart to indicatethat part was imported from octopart
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
                # distributor does not exists, create it
                manufacturer = rest.model.Manufacturer()
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
