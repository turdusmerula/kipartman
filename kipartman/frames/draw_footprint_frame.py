from dialogs.dialog_draw_footprint import DialogDrawFootprint
from frames.frame_draw_footprint.edit_grid_frame import EditGridFrame
from kicad.Canvas import *
import wx.lib.wxcairo
import helper.tree


class DataModelCategory(helper.tree.TreeContainerItem):
    def __init__(self, name):
        super(DataModelCategory, self).__init__()
        self.name = name
        
    def GetValue(self, col):
        vMap = { 
            0 : self.name,
        }
        return vMap[col]

    def GetAttr(self, col, attr):
        attr.Bold = True
        return True

class DataModelObject(helper.tree.TreeItem):
    def __init__(self, name, obj):
        super(DataModelObject, self).__init__()
        self.name = name
        self.obj = obj
        
    def GetValue(self, col):
        vMap = { 
            0 : self.name,
        }
        return vMap[col]

class TreeManagerObjects(helper.tree.TreeManager):
    def __init__(self, tree_view, *args, **kwargs):
        super(TreeManagerObjects, self).__init__(tree_view)
        
    def FindCategory(self, name):
        for data in self.data:
            if isinstance(data, DataModelCategory) and data.name==name:
                return data
        return None
                
    def AppendCategory(self, name):
        categoryobj = self.FindCategory(name)
        if categoryobj:
            return categoryobj
        categoryobj = DataModelCategory(name)
        self.AppendItem(None, categoryobj)
        return categoryobj
    
    def AppendObject(self, catgory_name, obj):
        categoryobj = self.AppendCategory(catgory_name)
        objobj = DataModelObject(format(type(obj)), obj)
        self.AppendItem(categoryobj, objobj)
        self.Expand(categoryobj)
        return objobj


class Anchor(object):
    def __init__(self, pos):
        self.pos = pos # mm

    def Distance(self, pospx, canvas):
        dx = pospx.x-canvas.xmm2px(self.pos.x)
        dy = pospx.y-canvas.ymm2px(self.pos.y)
        return math.sqrt(dx*dx+dy*dy)
    
class AnchorGroup(object):
    def __init__(self):
        pass

# base object for all editor objects
class EditorObject(Object):
    def __init__(self, layers, pos=Point(0, 0)):
        super(EditorObject, self).__init__(layers)
        
        self.pos = pos  # mm
        self.origin_pos = None
        self.radius = 5
        
        self.Clear()
    
    def Clear(self):
        self.anchors = []

    def AddAnchor(self, pos):
        self.anchors.append(Anchor(pos))

    # find closest anchor to position in radius
    def FindAnchor(self, pos, canvas, exclude_objects=[]):
        return self.r_find_anchor(self, pos, canvas, exclude_objects, min_distance=None, min_anchor=None)
    
    def r_find_anchor(self, obj, pos, canvas, exclude_objects=[], min_distance=None, min_anchor=None):
        if obj in exclude_objects:
            return [min_distance, min_anchor]
        
        for anchor in obj.anchors:
            distance = anchor.Distance(pos, canvas)
            if distance<=self.radius:
                if min_distance and distance<min_distance:
                    min_distance = distance
                    min_anchor = anchor
                elif not min_distance:
                    min_distance = distance
                    min_anchor = anchor

        for node in obj.nodes:
            [min_distance, min_anchor] = self.r_find_anchor(node, pos, canvas, exclude_objects, min_distance, min_anchor)
                
        return [min_distance, min_anchor]

    
    # find closest anchor to position
    def FindAnchors(self, pos, canvas, exclude_objects=[]):
        anchors = self.r_find_anchors(self, pos, canvas, exclude_objects, anchors=[])
        return sorted(anchors, key=lambda distance: distance[0])
    
    def r_find_anchors(self, obj, pos, canvas, exclude_objects=[], anchors=[]):
        if obj in exclude_objects:
            return anchors
        
        for anchor in obj.anchors:
            distance = anchor.Distance(pos, canvas)
            if distance<=self.radius:
                anchors.append([distance, anchors])

        for node in obj.nodes:
            self.r_find_anchors(node, pos, canvas, exclude_objects, anchors)
                
        return anchors

    def Select(self):
        self.layers.append("selection")
        for node in self.nodes:
            node.Select()
            
    def UnSelect(self):
        self.layers.remove("selection")
        for node in self.nodes:
            node.UnSelect()

    def StartMove(self):
        self.origin_pos = self.pos

    def Move(self, pos):
        self.pos = pos
        self.Update()

    def StartPlace(self):
        pass
    
    # return True if placement is complete
    def Place(self, pos):
        self.pos = pos
        self.Update()
        return True

    def Cancel(self):
        if self.origin_pos:
            self.pos = self.origin_pos
            self.Update()
        self.origin_pos = None
        
    def Validate(self):
        self.origin_pos = self.pos

# landmark for origin
class ObjectOrigin(EditorObject):
    def __init__(self, pos=Point(0, 0)):
        super(ObjectOrigin, self).__init__(["editor"], pos)
        
        self.length = 20
        self.radius = 15
        self.width = 1
        
        self.Update()
    
    def Update(self):
        self.Clear()
        self.AddAnchor(self.pos)
         
    def Render(self, canvas):
        super(ObjectOrigin, self).Render(canvas)
        
        lines = []
        
        posx = canvas.xmm2px(self.pos.x)
        posy = canvas.ymm2px(self.pos.y)
        lines.append([Point(posx-self.length, posy), Point(posx+self.length, posy)])
        lines.append([Point(posx, posy-self.length), Point(posx, posy+self.length)])
        
        canvas.Draw(Circle(Point(-self.radius, 0), Point(self.radius, 0)), self.layers)    
        canvas.Draw(MultiLine(lines, self.width), self.layers)

# grid object
class ObjectGrid(EditorObject):
    def __init__(self, pos, count, spacing):
        super(ObjectGrid, self).__init__(["editor"], pos)
        
        self.count = count 
        self.spacing = spacing # mm
        
        self.length = 5 # px
        self.width = 1 # px

        self.Update()
    
    def Update(self):
        self.Clear()
        x = self.pos.x
        for px in range(0, self.count.x):
            y = self.pos.y
            for py in range(0, self.count.y):
                self.AddAnchor(Point(x, y))
                y = y+self.spacing.y
            x = x+self.spacing.x
         
    def Render(self, canvas):
        super(ObjectGrid, self).Render(canvas)
        
        lines = []
        
        for anchor in self.anchors:
            posx = canvas.xmm2px(anchor.pos.x)
            posy = canvas.ymm2px(anchor.pos.y)
            lines.append([Point(posx-self.length, posy), Point(posx+self.length, posy)])
            lines.append([Point(posx, posy-self.length), Point(posx, posy+self.length)])
            
        canvas.Draw(MultiLine(lines, self.width), self.layers)

class ObjectPoint(EditorObject):
    def __init__(self, pos):
        super(ObjectPoint, self).__init__([], pos)
                
        self.width = 4 # px

        self.Update()
    
    def Update(self):
        self.Clear()
        self.AddAnchor(self.pos)
        
    def Render(self, canvas):
        super(ObjectPoint, self).Render(canvas)
        
        posx = canvas.xmm2px(self.anchors[0].pos.x)
        posy = canvas.ymm2px(self.anchors[0].pos.y)
            
        canvas.Draw(Rect(Point(posx-self.width, posy-self.width), Point(posx+self.width, posy+self.width), self.width, True), self.layers)
        
    def Select(self):
        self.layers.append("anchor")
    
    def UnSelect(self):
        self.layers.remove("anchor")
    
# dimension object
class ObjectDimension(EditorObject):
    def __init__(self):
        super(ObjectDimension, self).__init__(["editor"], Point())
        
        self.width = 1 # px

        self.points = []

        self.Update()
             
    def Render(self, canvas):
        super(ObjectDimension, self).Render(canvas)
                    
    def StartPlace(self):
        pass
    
    # return True if placement is complete
    def Place(self, pos):
        res = False
        point = ObjectPoint(pos)
        point.Select()
        self.points.append(point)
        self.AddNode(point)
        if len(self.points)==3:
            res = True
        self.Update()
        return res

class EditorState(object):
    StateNone = 0
    StateStartMoving = 1
    StateMoving = 2
    StatePlacing = 3
    
    def __init__(self, canvas, anchors_obj):
        self.canvas = canvas
        self.state = self.StateNone
        self.objs = []
        self.anchor_objs = anchors_obj
        self.initial_pos = None
        
    def Cancel(self):
        self.state = self.StateNone
        
        for obj in self.objs:
            obj.Cancel()
            obj.UnSelect()
        self.objs = []

    def Validate(self):
        self.state = self.StateNone
        for obj in self.objs:
            obj.Validate()

    def SelectObjects(self, objs):        
        self.Cancel()

        for obj in objs:
            self.objs.append(obj)
            obj.Select()
        
    def DoMove(self):
        self.state = self.StateStartMoving
            
    def DoPlace(self, obj):
        self.SelectObjects([obj])
        obj.StartPlace()
        self.state = self.StatePlacing
        
    def SetCursorPos(self, x, y):
        if self.state==self.StateMoving:
            for obj in self.objs:
                obj.Move(Point(obj.origin_pos.x+self.canvas.px2mm(x-self.initial_pos.x), obj.origin_pos.y+self.canvas.px2mm(y-self.initial_pos.y)))
        elif self.state==self.StatePlacing:                    
            self.objs[0].Move(Point(self.canvas.xpx2mm(x), self.canvas.ypx2mm(y)))
            
    def DoClick(self, x, y):
        if self.state==self.StateStartMoving:
            self.initial_pos = Point(x, y)
            self.state = self.StateMoving
            for obj in self.objs:
                obj.StartMove()
        elif self.state==self.StateMoving:
            self.Validate()
        elif self.state==self.StatePlacing:
            if self.objs[0].Place(Point(self.canvas.xpx2mm(x), self.canvas.ypx2mm(y))):
                self.Validate()
                
    def GetMovingObjects(self):
        res = []
        if self.state==self.StateMoving:
            res = self.objs
        return res

class DrawFootprintFrame(DialogDrawFootprint): 
    def __init__(self, parent):
        super(DrawFootprintFrame, self).__init__(parent)
        
        self.zoom = 1
        self.canvas = FootprintCanvas()
        self.selection = []

        self.component_object = EditorObject([])
        self.build_objects = EditorObject([])
        
        self.anchor_objects = EditorObject([])
        self.anchor_objects.AddNode(self.component_object)
        self.anchor_objects.AddNode(self.build_objects)
        
        self.all_objects = EditorObject([])
        self.all_objects.AddNode(self.anchor_objects)
        
        self.state = EditorState(self.canvas, self.anchor_objects)
        
        self.current_panel = None

        # create manufacturers list
        self.tree_objects_manager = TreeManagerObjects(self.tree_objects, context_menu=self.menu_edit)
        self.tree_objects_manager.AddTextColumn("name")
        self.tree_objects_manager.OnSelectionChanged = self.onTreeMenuObjectsSelChanged
        
        self.tree_objects_manager.AppendCategory('Drawing')
        self.tree_objects_manager.AppendCategory('Part')
        
        node = ObjectOrigin(Position(0, 0))
        self.build_objects.AddNode(node)

        node = ObjectGrid(Position(0, 0), Position(1, 1), Position(10, 10))
        self.cursor = node
        self.all_objects.AddNode(self.cursor)
        
        # last used objects
        self.last_grid = None
        
        ######
        node = ObjectGrid(Position(0, 0), Position(20, 20), Position(10, 10))
        self.build_objects.AddNode(node)
        self.tree_objects_manager.AppendObject('Drawing', node)
        
        node = ObjectPoint(Position(0, 0))
        self.build_objects.AddNode(node)
        self.tree_objects_manager.AppendObject('Drawing', node)
    
    def Render(self):
        self.canvas.Viewport(self.image_draw.GetRect().width, self.image_draw.GetRect().height)
        self.canvas.Origin(self.image_draw.GetRect().width/2, self.image_draw.GetRect().height/2)
        
        self.canvas.Clear(["editor"])
        img = self.canvas.Render(self.all_objects)
        self.image_draw.SetBitmap(wx.lib.wxcairo.BitmapFromImageSurface(img))

    def SelectObjects(self, objs):
        self.state.Cancel()
        
        self.selection = objs
        self.state.SelectObjects(objs)
        
        if self.current_panel:
            self.current_panel.Destroy()
        
        if len(objs)==1 and isinstance(objs[0], ObjectGrid):
            self.current_panel = EditGridFrame(self.panel_edit_object, self.Render, objs[0])
            self.last_grid = objs[0]
            
    def onDialogDrawFootprintChar( self, event ):
        print type(event)

    def onImageDrawChar( self, event ):
        print type(event)

    def onImageDrawLeftDClick( self, event ):
        event.Skip()
    
    def onImageDrawLeftDown( self, event ):
        pos = event.GetPosition()

        [distance, anchor] = self.anchor_objects.FindAnchor(pos, self.canvas, self.state.GetMovingObjects())
        if anchor:
            self.cursor.pos = anchor.pos
            pos = Point(self.canvas.xmm2px(self.cursor.pos.x), self.canvas.ymm2px(self.cursor.pos.y))
        else:
            self.cursor.pos = Position(self.canvas.xpx2mm(pos.x), self.canvas.ypx2mm(pos.y))
        self.cursor.Update()
        
        self.state.DoClick(pos.x, pos.y)
        self.Render()
        
    def onImageDrawLeftUp( self, event ):
        event.Skip()
    
    def onImageDrawMiddleDClick( self, event ):
        event.Skip()
    
    def onImageDrawMiddleDown( self, event ):
        event.Skip()
    
    def onImageDrawMiddleUp( self, event ):
        event.Skip()

    def onImageDrawMotion( self, event ):
        pos = event.GetPosition()
        
        [distance, anchor] = self.anchor_objects.FindAnchor(pos, self.canvas, self.state.GetMovingObjects())
        if anchor:
            self.cursor.pos = anchor.pos
            pos = Point(self.canvas.xmm2px(self.cursor.pos.x), self.canvas.ymm2px(self.cursor.pos.y))
        else:
            self.cursor.pos = Position(self.canvas.xpx2mm(pos.x), self.canvas.ypx2mm(pos.y))
        self.cursor.Update()

        self.state.SetCursorPos(pos.x, pos.y)
        self.Render()
        
    def onImageDrawMouseWheel( self, event ):
        event.Skip()
    
    def onImageDrawRightDClick( self, event ):
        event.Skip()
    
    def onImageDrawRightDown( self, event ):
        event.Skip()
    
    def onImageDrawRightUp( self, event ):
        event.Skip()
    
    def onMenuDrawPadSelection( self, event ):
        event.Skip()
    
    def onMenuToolDimensionSelection( self, event ):
        node = ObjectDimension()
            
        self.build_objects.AddNode(node)
        obj = self.tree_objects_manager.AppendObject('Drawing', node)
        self.tree_objects_manager.Select(obj)
        self.state.DoPlace(node)
    
    def onMenuToolGridSelection( self, event ):
        if self.last_grid:
            node = ObjectGrid(self.last_grid.pos, self.last_grid.count, self.last_grid.spacing)
        else:
            node = ObjectGrid(Position(0, 0), Position(20, 20), Position(10, 10))
            
        self.build_objects.AddNode(node)
        obj = self.tree_objects_manager.AppendObject('Drawing', node)
        self.tree_objects_manager.Select(obj)
        self.state.DoPlace(node)
        
    def onMenuToolRulerSelection( self, event ):
        event.Skip()
    
    def onMenuZoomResetSelection( self, event ):
        event.Skip()

    def onMenuEditMoveSelection( self, event ):
        self.state.DoMove()
    
    def onMenuEditRemoveSelection( self, event ):
        event.Skip()

    def onTreeMenuObjectsSelChanged( self, event ):
        item = self.tree_objects.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_objects_manager.ItemToObject(item)
        if isinstance(obj, DataModelObject):
            self.SelectObjects([obj.obj])
        self.Render()
        