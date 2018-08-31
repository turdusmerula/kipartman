from dialogs.dialog_draw_footprint import DialogDrawFootprint
from frames.frame_draw_footprint.edit_grid_frame import EditGridFrame
from frames.frame_draw_footprint.edit_dimension_frame import EditDimensionFrame
from frames.frame_draw_footprint.edit_line_frame import EditLineFrame
from frames.frame_draw_footprint.edit_angle_frame import EditAngleFrame
from frames.frame_draw_footprint.edit_pad_frame import EditPadFrame
from frames.frame_draw_footprint.edit_polyline_frame import EditPolylineFrame
from frames.frame_draw_footprint.edit_arc_frame import EditArcFrame
from frames.frame_draw_footprint.edit_circle_frame import EditCircleFrame
from frames.frame_draw_footprint.edit_footprint_frame import EditFootprintFrame
from frames.frame_draw_footprint.edit_text_frame import EditTextFrame

from kicad.Canvas import *
import wx.lib.wxcairo
import helper.tree
from operator import pos
import numpy
from kicad import kicad_mod_file

epsilon=1e-9

class DataModelCategoryObject(helper.tree.TreeContainerItem):
    def __init__(self, name):
        super(DataModelCategoryObject, self).__init__()
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
            if isinstance(data, DataModelCategoryObject) and data.name==name:
                return data
        return None
                
    def FindObject(self, obj):
        for data in self.data:
            if isinstance(data, DataModelObject) and data.obj==obj:
                return data
        return None

    def AppendCategory(self, name):
        categoryobj = self.FindCategory(name)
        if categoryobj:
            return categoryobj
        categoryobj = DataModelCategoryObject(name)
        self.AppendItem(None, categoryobj)
        return categoryobj
    
    def AppendObject(self, catgory_name, obj):
        categoryobj = self.AppendCategory(catgory_name)
        objobj = DataModelObject(obj.Description(), obj)
        self.AppendItem(categoryobj, objobj)
        self.Expand(categoryobj)
        return objobj

    def DeleteObject(self, obj):
        objobj = self.FindObject(obj)
        if objobj is None:
            return None
        self.DeleteItem(objobj.parent, objobj)
        


class DataModelCategoryLayer(helper.tree.TreeContainerItem):
    def __init__(self, name):
        super(DataModelCategoryLayer, self).__init__()
        self.name = name
        
    def GetValue(self, col):
        vMap = { 
            0 : True,
            1 : False,
            2 : self.name,
        }
        return vMap[col]

    def GetAttr(self, col, attr):
        attr.Bold = True
        return True

class DataModelLayer(helper.tree.TreeItem):
    def __init__(self, checked, layer):
        super(DataModelLayer, self).__init__()
        self.layer = layer
        self.checked = checked
        
    def GetValue(self, col):
        vMap = { 
            0 : self.checked,
            1 : self.layer.active,
            2 : self.layer.name
        }
        return vMap[col]

class TreeManagerLayers(helper.tree.TreeManager):
    def __init__(self, tree_view, *args, **kwargs):
        super(TreeManagerLayers, self).__init__(tree_view)

    def FindCategory(self, name):
        for data in self.data:
            if isinstance(data, DataModelCategoryLayer) and data.name==name:
                return data
        return None
                
    def FindLayer(self, name):
        for data in self.data:
            if isinstance(data, DataModelLayer) and data.layer.name==name:
                return data
        return None

    def AppendLayer(self, layer):
        categoryobj = self.AppendCategory(layer.layer_type)
        objlayer = DataModelLayer(True, layer)
        self.AppendItem(categoryobj, objlayer)
        self.Expand(categoryobj)
        return objlayer

    def AppendCategory(self, name):
        categoryobj = self.FindCategory(name)
        if categoryobj:
            return categoryobj
        categoryobj = DataModelCategoryLayer(name)
        self.AppendItem(None, categoryobj)
        return categoryobj


class Anchor(object):
    def __init__(self, parent, pos):
        self.pos = pos # mm
        self.parent = parent
        
    def Distance(self, pos):
        return self.pos.Distance(pos)
    
    def Pos(self, point=None):
        return self.pos
    
class AnchorLine(object):
    def __init__(self, parent, line):
        self.parent = parent
        self.line = line
        
    def Distance(self, pos):
        p = self.line.get_projection(pos)
        return p.Distance(pos)

    # return projection of point on line
    def Pos(self, point=None):
        return self.line.get_projection(point)

class AnchorSegment(AnchorLine):
    def __init__(self, parent, line):
        super(AnchorSegment, self).__init__(parent, line)
    
    def IsIn(self, p):
        isin = False
        if math.fabs(self.line.start.x-self.line.end.x)>epsilon:
            if self.line.start.x<self.line.end.x and p.x>=self.line.start.x and p.x<=self.line.end.x:
                isin = True
            elif p.x>=self.line.end.x and p.x<=self.line.start.x:
                isin = True
                 
        if math.fabs(self.line.start.y-self.line.end.y)>epsilon:
            if self.line.start.y<self.line.end.y and p.y>=self.line.start.y and p.y<=self.line.end.y:
                isin = True
            elif p.y>=self.line.end.y and p.y<=self.line.start.y:
                isin = True
        
        return isin
    
    def Distance(self, pos):
        c = 0
        p = self.line.get_projection(pos)

        if self.IsIn(p)==True:            
            return p.Distance(pos)
        return None

    # return projection of point on line
    def Pos(self, point=None):
        return self.line.get_projection(point)

class AnchorArc(object):
    def __init__(self, parent, arc):
        self.arc = arc
        self.parent = parent
         
    def Distance(self, pos):
        p = self.arc.get_projection(pos)
        if p is None:
            return None
        return p.Distance(pos)
 
    # return projection of point on line
    def Pos(self, point=None):
        return self.arc.get_projection(point)

class AnchorCircle(object):
    def __init__(self, parent, circle):
        self.circle = circle
        self.parent = parent
         
    def Distance(self, pos):
        p = self.circle.get_projection(pos)
        if p is None:
            return None
        return p.Distance(pos)
 
    # return projection of point on line
    def Pos(self, point=None):
        return self.circle.get_projection(point)

# base object for all editor objects
class EditorObject(Object):
    def __init__(self, layers, pos=Point(0, 0)):
        super(EditorObject, self).__init__(layers)
        
        self.pos = pos  # mm
        self.origin_pos = None
        self.radius = 10
        
        self.angle = 0.
        self.origin_angle = None
        
        self.placed = False
        
        self.Clear()
    
    def Clear(self):
        self.anchors = []

    def AddAnchor(self, pos):
        self.anchors.append(Anchor(self, pos))

    def AddAnchorLine(self, line):
        self.anchors.append(AnchorLine(self, line))

    def AddAnchorSegment(self, line):
        self.anchors.append(AnchorSegment(self, line))

    def AddAnchorArc(self, centre, radius, angle_start, angle_end):
        arc = Arc(centre, radius, angle_start, angle_end)
        self.anchors.append(AnchorArc(self, arc))
    
    def AddAnchorCircle(self, centre, end):
        circle = Circle(centre, end)
        self.anchors.append(AnchorCircle(self, circle))

    # find closest anchor to position
    # if a type is given then limit search to this type
    def FindAnchor(self, anchor_type, pos, exclude_objects=[]):
        return self.r_find_anchor(anchor_type, self, pos, exclude_objects)
    
    def r_find_anchor(self, anchor_type, obj, pos, exclude_objects=[], min_distance=None, min_anchor=None):
        if obj in exclude_objects:
            return [min_distance, min_anchor]
        
        for anchor in obj.anchors:
            if ( anchor_type and issubclass(type(anchor), anchor_type) ) or anchor_type is None:
                distance = anchor.Distance(pos)
                if distance is not None:
                    if min_distance is None:
                        min_distance = distance
                        min_anchor = anchor
                    if distance<min_distance:
                        min_distance = distance
                        min_anchor = anchor

        for node in obj.nodes:
            [min_distance, min_anchor] = self.r_find_anchor(anchor_type, node, pos, exclude_objects, min_distance, min_anchor)
                
        return [min_distance, min_anchor]
    
    # find closest anchor to position
    def FindAnchors(self, pos, exclude_objects=[]):
        anchors = self.r_find_anchors(self, pos, exclude_objects, anchors=[])
        return sorted(anchors, key=lambda distance: distance[0])
    
    def r_find_anchors(self, obj, pos, exclude_objects=[], anchors=[]):
        if obj in exclude_objects:
            return anchors
        
        for anchor in obj.anchors:
            distance = anchor.Distance(pos)
            if distance<=self.radius:
                anchors.append([distance, anchors])

        for node in obj.nodes:
            self.r_find_anchors(node, pos, exclude_objects, anchors)
                
        return anchors

    def Select(self):
        if "Selection" not in self.layers:
            self.layers.append("Selection")
        for node in self.nodes:
            node.Select()
            
    def UnSelect(self):
        if "Selection" in self.layers:
            self.layers.remove("Selection")
        for node in self.nodes:
            node.UnSelect()

    def StartMove(self):
        self.origin_pos = self.pos

    def Move(self, pos):
        self.pos = pos
        self.Update()

    def StartRotate(self):
        self.origin_pos = self.pos
        self.origin_angle = self.angle
        
    def Rotate(self, origin, angle):
        self.pos = self.origin_pos.Rotate(origin, angle)
        self.angle = self.origin_angle+angle
        self.Update()
        
    def StartPlace(self):
        pass
    
    # return True if placement is complete
    def Place(self, pos):
        self.pos = pos
        self.Update()
        self.placed = True
        return True

    def Placed(self):
        return self.placed
    
    def Cancel(self):
        changed = False
        if self.origin_pos:
            self.pos = self.origin_pos
            changed = True
        self.origin_pos = None
        if self.origin_angle:
            self.angle = self.origin_angle
            changed = True
        self.origin_angle = None
        if changed:    
            self.Update()
        
    def Validate(self):
        self.origin_pos = self.pos
        self.origin_angle = self.angle

    def Description(self):
        return format(type(self))
    
# landmark for origin
class ObjectOrigin(EditorObject):
    def __init__(self, pos=Point(0, 0)):
        super(ObjectOrigin, self).__init__(["Editor"], pos)
        
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

    def Description(self):
        return "Origin x={} y={}".format(self.pos.x, self.pos.y)

# grid object
class ObjectGrid(EditorObject):
    def __init__(self, pos, count, spacing):
        super(ObjectGrid, self).__init__(["Editor"], pos)
        
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
                self.AddAnchor(Point(x, y).Rotate(self.pos, self.angle))
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

    def Description(self):
        return "Grid {}x{} x={} y={}".format(self.count.x, self.count.y, self.pos.x, self.pos.y)

class ObjectPoint(EditorObject):
    def __init__(self, pos=Point()):
        super(ObjectPoint, self).__init__([], pos)
                
        self.width = 4 # px

        self.Update()
    
    def Update(self):
        self.Clear()
        self.AddAnchor(self.pos)
        
    def Render(self, canvas):
        super(ObjectPoint, self).Render(canvas)

        pos = Point(canvas.xmm2px(self.anchors[0].pos.x), canvas.ymm2px(self.anchors[0].pos.y))        
            
        canvas.Draw(Rect(Point(pos.x-self.width, pos.y-self.width), Point(pos.x+self.width, pos.y+self.width), self.width, True), self.layers)
        
    def Select(self):
        if "Anchor" not in self.layers:
            self.layers.append("Anchor")
    
    def UnSelect(self):
        if "Anchor" in self.layers:
            self.layers.remove("Anchor")

    def Description(self):
        return "Point x={} y={}".format(self.pos.x, self.pos.y)
        
# dimension object
class ObjectDimension(EditorObject):
    def __init__(self):
        super(ObjectDimension, self).__init__(["Editor"], Point())
        
        self.width = 1 # px
        self.font = Font(Point(15, 15), 1)
        
        self.points = [ObjectPoint(), ObjectPoint()]
        for point in self.points:
            self.AddNode(point)
        
        self.placing_point = None
        
        self.text_point = Point()
        
        self.Update()

    def Update(self):
        self.Clear()
        self.AddAnchor(Point((self.points[0].pos.x+self.points[1].pos.x)/2., (self.points[0].pos.y+self.points[1].pos.y)/2.))
    
    def get_projection(self, p0, a, b):
        p1 = Point()
        a1 = -1/a
        b1 = p0.y-a1*p0.x
        
        p1.x = (b-b1)/(a1-a)
        p1.y = (b*a1-a*b1)/(a1-a)
                
        return p1
    
    def Render(self, canvas):
        super(ObjectDimension, self).Render(canvas)

        # p0-p1 center
        p0 = Point(canvas.xmm2px(self.points[0].pos.x), canvas.ymm2px(self.points[0].pos.y))
        p1 = Point(canvas.xmm2px(self.points[1].pos.x), canvas.ymm2px(self.points[1].pos.y))
        p2 = Point(canvas.xmm2px(self.pos.x), canvas.ymm2px(self.pos.y))
        
        p0p1 = Line(p0, p1)
        pc = p0p1.get_center()
        
        if math.fabs(p1.x-p0.x)<epsilon:
            p3 = Point(p2.x, p0.y)
            p4 = Point(p2.x, p1.y)
        else:
            [p0p1a, p0p1b] = p0p1.get_ab()
            # parralel to p0p1 passing by p2
            p2b = Line.get_b(p0p1a, p2)
            
            if math.fabs(p0p1a)<epsilon:
                # projection of p0 and p1 on parallel
                p3 = Point(p0.x, p2b)
                p4 = Point(p1.x, p2b)
            else:
                # projection of p0 and p1 on parallel
                p3 = self.get_projection(p0, p0p1a, p2b)
                p4 = self.get_projection(p1, p0p1a, p2b)
                
        # compute angle for p0p1
        angle = -math.atan2( p1.x-p0.x,  p1.y-p0.y)+math.pi/2.

        # distance
        distance = self.Size()

        canvas.SetFont(self.font)
        
        if self.placed==False and self.placing_point is None:
            return
        if self.placing_point and self.placing_point==1:
            p5 = Point((p0.x+p1.x)/2., (p0.y+p1.y)/2.)
            canvas.Draw(Arrow(p0, p1, 1), self.layers)
            canvas.Draw(Text(format(distance), Position(p5.x, p5.y, angle), 'center', 'bottom', 5), self.layers)
        if self.placed or self.placing_point==2:
            p5 = Point((p3.x+p4.x)/2., (p3.y+p4.y)/2.)
            canvas.Draw(Line(p0, p3, 1), self.layers)
            canvas.Draw(Line(p1, p4, 1), self.layers)
            canvas.Draw(Arrow(p3, p4, 1), self.layers)
            canvas.Draw(Text(format(distance), Position(p5.x, p5.y, angle), 'center', 'bottom', 5), self.layers)
            
            for anchor in self.anchors:
                pm = Point(canvas.xmm2px(anchor.pos.x), canvas.ymm2px(anchor.pos.y))
                pml = 5
                canvas.Draw(Line(Point(pm.x-pml, pm.y), Point(pm.x+pml, pm.y), 1), self.layers)
                canvas.Draw(Line(Point(pm.x, pm.y-pml), Point(pm.x, pm.y+pml), 1), self.layers)
        
    def Move(self, pos):
        if not self.placing_point is None:
            if self.placing_point<2:
                self.points[self.placing_point].Move(pos)
            else:
                self.pos = pos
        elif self.placed:
            for point in self.points:
                point.pos = Point(point.pos.x+pos.x-self.pos.x, point.pos.y+pos.y-self.pos.y) 
                point.Update()
            self.pos = pos
            
        self.Update()
        
    def StartPlace(self):
        self.placing_point = 0
        self.points[0].Select()
        
    # return True if placement is complete
    def Place(self, pos):
        self.placing_point = self.placing_point+1
        if self.placing_point>0 and self.placing_point<2:
            self.points[self.placing_point].pos = self.points[self.placing_point-1].pos
            self.points[self.placing_point].Update()
        if self.placing_point==2:
            self.pos = self.points[1].pos
        if self.placing_point<2:
            self.points[self.placing_point].Select()
        if self.placing_point>2:
            self.placing_point = None
            self.placed = True
            return True
        return False

    def Select(self):
        if "Selection" not in self.layers:
            self.layers.append("Selection")
        if self.placed:
            for node in self.nodes:
                node.Select()

    def Size(self):
        dx = self.points[1].pos.x-self.points[0].pos.x
        dy = self.points[1].pos.y-self.points[0].pos.y
        return math.sqrt(dx*dx+dy*dy)
    
    def SetSize(self, size):
        p0 = Point(self.points[0].pos.x, self.points[0].pos.y)
        p1 = Point(self.points[1].pos.x, self.points[1].pos.y)
        p0p1 = Line(p0, p1)

        dx = p1.x-p0.x
        dy = p1.y-p0.y
        
        if math.fabs(p1.x-p0.x)<epsilon:
            if dy>=0:
                self.points[1].pos.y = p0.y+size
            else:
                self.points[1].pos.y = p0.y-size                
        else:
            
            [p0p1a, p0p1b] = p0p1.get_ab()
            d = size
            # solve: d=sqrt(dx*dx+dy*dy)
            # with: dy=a*dx
            ndx = d/math.sqrt(p0p1a*p0p1a+1)
            if dx>=0:
                self.points[1].pos.x = p0.x+ndx
            else:
                self.points[1].pos.x = p0.x-ndx                
            # solve: d=sqrt(dx*dx+dy*dy)
            # with: dx=dy/a
            ndy = math.fabs(p0p1a)*d/math.sqrt(p0p1a*p0p1a+1)
            if dy>=0:
                self.points[1].pos.y = p0.y+ndy
            else:
                self.points[1].pos.y = p0.y-ndy

    def Description(self):
        return "Dimension length={}".format(self.Size())

# line object
class ObjectLine(EditorObject):
    def __init__(self):
        super(ObjectLine, self).__init__(["Editor"], Point())
        
        self.width = 1 # px

        self.points = [ObjectPoint(), ObjectPoint()]
#        for point in self.points:
#            self.AddNode(point)

        self.placing_point = None
        
        self.Update()

    def Update(self):
        self.Clear()
        self.AddAnchorLine(Line(self.points[0].pos, self.points[1].pos))
    
    def Render(self, canvas):
        super(ObjectLine, self).Render(canvas)

        points = []
        for point in self.points:
            points.append(Point(point.pos.x, point.pos.y).Rotate(self.points[0].pos, self.angle))

        if self.placed or ( not self.placing_point is None and self.placing_point>0):
            p0 = Point(canvas.xmm2px(points[0].x), canvas.ymm2px(points[0].y))
            p1 = Point(canvas.xmm2px(points[1].x), canvas.ymm2px(points[1].y))
            canvas.Draw(StraightLine(p0, p1, self.width), self.layers)
        
    def Move(self, pos):
        if not self.placing_point is None:
            if self.placing_point<2:
                self.points[self.placing_point].Move(pos)
                self.points[self.placing_point].Update()
            else:
                self.pos = pos
        elif self.placed:
            for point in self.points:
                point.pos = Point(point.pos.x+pos.x-self.pos.x, point.pos.y+pos.y-self.pos.y) 
                point.Update()
            self.pos = pos
            
        self.Update()
        
    def StartPlace(self):
        self.placing_point = 0
        self.points[0].Select()
        
    # return True if placement is complete
    def Place(self, pos):
        self.placing_point = self.placing_point+1
        if self.placing_point==1:
            self.points[1].pos = self.points[0].pos
            self.points[1].Update()
        if self.placing_point<2:
            self.points[self.placing_point].Select()
        if self.placing_point==2:
            self.placing_point = None
            self.placed = True
            for node in self.nodes:
                node.UnSelect()
            return True
        return False

    def Select(self):
        if "Selection" not in self.layers:
            self.layers.append("Selection")
    
class ObjectVerticalLine(ObjectLine):
    def __init__(self):
        super(ObjectVerticalLine, self).__init__()
                        
    def Move(self, pos):
        if not self.placing_point is None:
            if self.placing_point<2:
                self.points[0].Move(pos)
                self.points[1].Move(Point(pos.x, pos.y+1))
                self.points[0].Update()
            else:
                self.pos = pos
        elif self.placed:
            for point in self.points:
                point.pos = Point(point.pos.x+pos.x-self.pos.x, point.pos.y+pos.y-self.pos.y) 
                point.Update()
            self.pos = pos
            
        self.Update()
        
    def StartPlace(self):
        self.placing_point = 1
        self.points[0].Select()

class ObjectHorizontalLine(ObjectLine):
    def __init__(self):
        super(ObjectHorizontalLine, self).__init__()

        self.points[1].pos = Point(1, 0)
                        
    def Move(self, pos):
        if not self.placing_point is None:
            if self.placing_point<2:
                self.points[0].Move(pos)
                self.points[1].Move(Point(pos.x+1, pos.y))
                self.points[0].Update()
            else:
                self.pos = pos
        elif self.placed:
            for point in self.points:
                point.pos = Point(point.pos.x+pos.x-self.pos.x, point.pos.y+pos.y-self.pos.y) 
                point.Update()
            self.pos = pos
            
        self.Update()
        
    def StartPlace(self):
        self.placing_point = 1
        self.points[0].Select()

# angle object
class ObjectAngle(EditorObject):
    def __init__(self):
        super(ObjectAngle, self).__init__(["Editor"], Point())
        
        self.width = 1 # px
        self.font = Font(Point(15, 15), 1)
        
        self.points = [ObjectPoint(), ObjectPoint(), ObjectPoint(), ObjectPoint()]
        for point in self.points:
            self.AddNode(point)
        
        self.placing_point = None
        
        self.text_point = Point()
        
        self.Update()

    def Update(self):
        self.Clear()
        if self.placed:
            p0 = self.points[0].pos
            p1 = self.points[1].pos
            p2 = self.points[2].pos
            p3 = self.points[3].pos
            pref = Point(p0.x+1, p0.y)
            
            angle_start = p0.GetAngle(pref, p1)
            angle_end = p0.GetAngle(pref, p2)

            d1 = p0.Distance(p1)
            d2 = p0.Distance(p2)
            d3 = p0.Distance(p3)
            
            d = d1
            if d2<d:
                d = d2
            
            if d3>d:
                d = d3
                self.AddAnchorSegment(Line(p0, Point(p0.x+d*math.cos(angle_start), p0.y+d*math.sin(angle_start))))
                self.AddAnchorSegment(Line(p0, Point(p0.x+d*math.cos(angle_end), p0.y+d*math.sin(angle_end))))
            else:
                self.AddAnchorSegment(Line(p0, p1))
                self.AddAnchorSegment(Line(p0, p2))
                 
    def Render(self, canvas):
        super(ObjectAngle, self).Render(canvas)

        canvas.SetFont(self.font)
        
        p0 = self.points[0].pos
        p1 = self.points[1].pos
        p2 = self.points[2].pos
        p3 = self.points[3].pos

        p0px = Point(canvas.xmm2px(p0.x), canvas.ymm2px(p0.y))
        p1px = Point(canvas.xmm2px(p1.x), canvas.ymm2px(p1.y))
        p2px = Point(canvas.xmm2px(p2.x), canvas.ymm2px(p2.y))
        p3px = Point(canvas.xmm2px(p3.x), canvas.ymm2px(p3.y))

        if self.placed==False and self.placing_point is None:
            return
        if self.placing_point and self.placing_point>0 and self.placing_point<3:
            canvas.Draw(Line(p0px, p1px, 1), self.layers)
        if self.placing_point and self.placing_point>1 and self.placing_point<3:
            canvas.Draw(Line(p0px, p2px, 1), self.layers)
        if self.placing_point and self.placing_point==3:
            canvas.Draw(Line(p0px, p1px, 1), self.layers)
            canvas.Draw(Line(p0px, p2px, 1), self.layers)
        if self.placed or ( self.placing_point and self.placing_point>=2 ):
            pref = Point(p0.x+1, p0.y)
            d1 = p0px.Distance(p1px)
            d2 = p0px.Distance(p2px)
            d3 = p0px.Distance(p3px)
            
            angle_start = p0.GetAngle(pref, p1)
            angle_end = p0.GetAngle(pref, p2)
            angle = p0.GetAngle(p1, p2) 
            
            d = d1
            if d2<d:
                d = d2
            
            if d3>d:
                d = d3
                canvas.Draw(Line(p0px, Point(p0px.x+d*math.cos(angle_start), p0px.y+d*math.sin(angle_start)), 1), self.layers)
                canvas.Draw(Line(p0px, Point(p0px.x+d*math.cos(angle_end), p0px.y+d*math.sin(angle_end)), 1), self.layers)
            else:
                canvas.Draw(Line(p0px, p1px, 1), self.layers)
                canvas.Draw(Line(p0px, p2px, 1), self.layers)
                
            ptext = Position(p0px.x+d*math.cos(angle_start), p0px.y+d*math.sin(angle_start)).Rotate(p0px, angle/2)
            if angle<0:
                ptext.angle = angle_end-angle/2.+math.pi/2.
                canvas.Draw(Arc(p0px, d, angle_end, angle_end-angle, 1), self.layers)
                canvas.Draw(Text("{:8.3f}".format(math.fabs(angle)*180./math.pi), ptext, anchor_x='center', anchor_y='center'), self.layers)            
            else:
                ptext.angle = angle_start+angle/2+math.pi/2.
                canvas.Draw(Arc(p0px, d, angle_start, angle_start+angle, 1), self.layers)
                canvas.Draw(Text("{:8.3f}".format(math.fabs(angle)*180./math.pi), ptext, anchor_x='center', anchor_y='center'), self.layers)            


        
    def Move(self, pos):
        if not self.placing_point is None:
            if self.placing_point<4:
                self.points[self.placing_point].Move(pos)
            else:
                self.pos = pos
        elif self.placed:
            for point in self.points:
                point.pos = Point(point.pos.x+pos.x-self.pos.x, point.pos.y+pos.y-self.pos.y) 
                point.Update()
            self.pos = pos
            
        self.Update()
        
    def StartPlace(self):
        self.placing_point = 0
        self.points[0].Select()
        
    # return True if placement is complete
    def Place(self, pos):
        self.placing_point = self.placing_point+1
        if self.placing_point>0 and self.placing_point<4:
            self.points[self.placing_point].pos = self.points[self.placing_point-1].pos
            self.points[self.placing_point].Update()
        if self.placing_point==2:
            self.pos = self.points[1].pos
            self.points[3].pos = self.points[0].pos
        if self.placing_point<4:
            self.points[self.placing_point].Select()
        if self.placing_point==4:
            self.placing_point = None
            self.placed = True
            return True
        return False

    def Select(self):
        if "Selection" not in self.layers:
            self.layers.append("Selection")
        if self.placed:
            for node in self.nodes:
                node.Select()

    def Angle(self):
        p0 = self.points[0].pos
        p1 = self.points[1].pos
        p2 = self.points[2].pos
        return p0.GetAngle(p1, p2) 
    
    def SetAngle(self, angle):
        p0 = self.points[0].pos
        p1 = self.points[1].pos
        p2 = self.points[2].pos
        return p0.SetAngle(p1, p2, angle)
    
class ObjectPad(EditorObject):
    def __init__(self):
        super(ObjectPad, self).__init__([], Point())
        self.type = 'smd' # smd thru_hole, connect, np_thru_hole
        self.shape = 'rect' # rect, trapezoid, oval, circular
        self.size = Point()
        self.offset = Point()
        self.drill = Point()
        self.drill_type = 'circle'
        self.die_length = 0.
        self.name = ''
        
        self.solder_mask_margin = 0.
        self.solder_paste_margin = 0.
        self.clearance = 0.
        self.solder_paste_margin_ratio = 0.
        
        self.thermal_width = 0.
        self.thermal_gap = 0.
        self.zone_connect = None
        
        self.trapezoidal_delta = 0.
        self.trapezoidal_direction = 'vert' # vert or horz
        
        self.font = Font(Point(15, 15), 1)

        self.points = []
        self.placing_point = None
        
        self.SetShape(self.shape)
        
    def SetType(self, type):
        self.type = type
        
        if type=='thru_hole':
            self.layers = ["*.Cu", "*.Mask"]
        elif type=='smd':
            self.layers = ["F.Cu", "F.Paste", "F.Mask"]
        elif type=='connect':
            self.layers = ["F.Cu", "F.Mask"]
        elif type=='np_thru_hole':
            self.layers = ["*.Cu", "*.Mask"]
             
        self.Update()

    def SetShape(self, shape):
        self.shape = shape
            
        
        self.points = []
        self.ClearNodes()
        if self.shape=='rect' or self.shape=='trapezoid' or self.shape=='oval':
            self.points = [ ObjectPoint(),
                            ObjectPoint(), ObjectPoint(), ObjectPoint(), ObjectPoint(),
                            ObjectPoint(), ObjectPoint(), ObjectPoint(), ObjectPoint()
                        ]
        elif self.shape=='circle':
            self.points = [ObjectPoint(), 
                           ObjectPoint(), ObjectPoint(), ObjectPoint(), ObjectPoint()]
        
        self.Update()
        for point in self.points:
            self.AddNode(point)        
        
    def SetSize(self, size):
        self.size = size
            
        self.Update()
        
    def Update(self):
        dx = self.size.x/2.
        dy = self.size.y/2.
        
        self.points[0].Move(self.pos)
        if self.shape=='rect' or self.shape=='trapezoid' or self.shape=='oval':
            self.points[1].Move(Point(self.pos.x-dx, self.pos.y-dy))
            self.points[2].Move(Point(self.pos.x+dx, self.pos.y-dy))
            self.points[3].Move(Point(self.pos.x+dx, self.pos.y+dy))
            self.points[4].Move(Point(self.pos.x-dx, self.pos.y+dy))
            self.points[5].Move(Point(self.pos.x,    self.pos.y-dy))
            self.points[6].Move(Point(self.pos.x+dx, self.pos.y))
            self.points[7].Move(Point(self.pos.x,    self.pos.y+dy))
            self.points[8].Move(Point(self.pos.x-dx, self.pos.y))
        elif self.shape=='circle':
            self.points[1].Move(Point(self.pos.x,    self.pos.y-dx))
            self.points[2].Move(Point(self.pos.x+dx, self.pos.y))
            self.points[3].Move(Point(self.pos.x,    self.pos.y+dx))
            self.points[4].Move(Point(self.pos.x-dx, self.pos.y))
                
        if math.fabs(self.angle)>epsilon:
            for p in self.points:
                p.StartRotate()
                p.Rotate(self.pos, -self.angle)
        
    def Render(self, canvas):
        super(ObjectPad, self).Render(canvas)
        
        offset = Point(canvas.mm2px(self.offset.x), canvas.mm2px(self.offset.y)) #.Rotate(Point(0, 0), self.angle)
        pos = Position(canvas.xmm2px(self.pos.x), canvas.ymm2px(self.pos.y), self.angle)
        size = Point(canvas.mm2px(self.size.x), canvas.mm2px(self.size.y))
        drill = Point(canvas.mm2px(self.drill.x), canvas.mm2px(self.drill.y))
        
        angle = -self.angle
        
        
        if self.placed or ( self.placing_point is not None and self.placing_point==1):
            if self.shape=='rect' or self.shape=='trapezoid' or self.shape=='oval':
                dx = size.x/2.
                dy = size.y/2.
                    
                tx = 0.
                ty = 0.
                if self.shape=='trapezoid' and self.trapezoidal_direction=='vert':
                    ty = canvas.mm2px(self.trapezoidal_delta/2.)
                if ty>dy:
                    ty = dy
                elif self.shape=='trapezoid' and self.trapezoidal_direction=='horz':
                    tx = canvas.mm2px(self.trapezoidal_delta/2.)
                if tx>dx:
                    tx = dx

                points = []
                if self.shape=='oval':
                    points.append(Point(pos.x-dx, pos.y-dy+dx))
                    points.append(Point(pos.x+dx, pos.y-dy+dx))
                    points.append(Point(pos.x+dx, pos.y+dy-dx))
                    points.append(Point(pos.x-dx, pos.y+dy-dx))
                else:
                    points.append(Point(pos.x-dx+tx, pos.y-dy-ty))
                    points.append(Point(pos.x+dx-tx, pos.y-dy+ty))
                    points.append(Point(pos.x+dx+tx,    pos.y+dy-ty))
                    points.append(Point(pos.x-dx-tx,    pos.y+dy+ty))
                
                for p in points:
                    pr = Point(p.x+offset.x, p.y+offset.y).Rotate(pos, angle)
                    p.x = pr.x
                    p.y = pr.y
                canvas.Draw(PolyLine(points, width=1, fill=True), self.layers)
            
                if self.shape=='oval':
                    canvas.Draw(Arc(Point(pos.x+offset.x, pos.y-dy+dx+offset.y).Rotate(pos, angle), dx, math.pi+angle, 2.*math.pi+angle, width=1, fill=True), self.layers)
                    canvas.Draw(Arc(Point(pos.x+offset.x, pos.y+dy-dx+offset.y).Rotate(pos, angle), dx, 0+angle, math.pi+angle, width=1, fill=True), self.layers)
            elif self.shape=='circle':
                radius = canvas.mm2px(self.size.x/2.)
                canvas.Draw(Circle(Point(pos.x, pos.y), Point(pos.x+radius, pos.y), width=1, fill=True), self.layers)

            if self.type=='thru_hole' or self.type=='np_thru_hole':
                if self.drill_type=='circle':
                    radius = drill.x/2.
                    canvas.Draw(Circle(Point(pos.x, pos.y), Point(pos.x+radius, pos.y), width=1, fill=True), ["Hole"])
                else:
                    dx = drill.x/2.
                    dy = drill.y/2.
                    points = []
                    points.append(Point(pos.x-dx, pos.y-dy+dx))
                    points.append(Point(pos.x+dx, pos.y-dy+dx))
                    points.append(Point(pos.x+dx, pos.y+dy-dx))
                    points.append(Point(pos.x-dx, pos.y+dy-dx))
                    for p in points:
                        pr = p.Rotate(pos, self.angle)
                        p.x = pr.x
                        p.y = pr.y
                    canvas.Draw(PolyLine(points, width=1, fill=True), ["Hole"])
                    canvas.Draw(Arc(Point(pos.x, pos.y-dy+dx).Rotate(pos, angle), dx, math.pi+angle, 2.*math.pi+angle, width=0, fill=True), ["Hole"])
                    canvas.Draw(Arc(Point(pos.x, pos.y+dy-dx).Rotate(pos, angle), dx, 0+angle, math.pi+angle, width=0, fill=True), ["Hole"])

            if self.type!='np_thru_hole':
                canvas.SetFont(self.font)
                canvas.Draw(Text(self.name, pos, anchor_x='center', anchor_y='center'), ["Editor"])            

    def Select(self):
        if "Selection" not in self.layers:
            self.layers.append("Selection")
        if self.placed:
            for node in self.nodes:
                node.Select()
    
#    def StartMove(self):
#        self.origin_pos = self.pos

    def Move(self, pos):
        if not self.placing_point is None and self.placing_point==1:
            dx = pos.x-self.points[0].pos.x
            dy = pos.y-self.points[0].pos.y
            self.SetSize(Point(math.fabs(dx*2), math.fabs(dy*2)))
        else:
            self.pos = pos
            
        self.Update()

    def Rotate(self, origin, angle):
        self.pos = self.origin_pos.Rotate(origin, angle)
        self.angle = self.origin_angle+angle
        self.Update()
                
    def StartPlace(self):
        self.placing_point = 0
        self.points[0].Select()

    def Place(self, pos):
        self.placing_point = self.placing_point+1
        if self.placing_point==1:
            self.points[0].pos = pos
            self.points[0].Update()
        elif self.placing_point==2:
            dx = pos.x-self.points[0].pos.x
            dy = pos.y-self.points[0].pos.y
            self.SetSize(Point(math.fabs(dx*2), math.fabs(dy*2)))
            self.placing_point = None
            self.placed = True
            self.Select()
        
        return self.placed

    def Description(self):
        return "Pad {} {} {} x={} y={} width={} height={} angle={}".format(self.type, self.shape, self.name, self.pos.x, self.pos.y, self.size.x, self.size.y, self.angle)
            
class ObjectPolyline(EditorObject):
    def __init__(self, layers=[]):
        super(ObjectPolyline, self).__init__(layers, Point())
        
        self.width = 1 # mm

        self.points = []
        
        self.Update()

    def Update(self):
        self.Clear()
        
        p0 = None
        for p1 in self.points:
            if p0:
                self.AddAnchorSegment(Line(p0.pos, p1.pos))
            self.AddAnchor(p1.pos)
            p0 = p1
    
    def Render(self, canvas):
        super(ObjectPolyline, self).Render(canvas)

        if self.placed or len(self.points)>0:
            for p in range(1, len(self.points)):
                p0 = Point(canvas.xmm2px(self.points[p-1].pos.x), canvas.ymm2px(self.points[p-1].pos.y))
                p1 = Point(canvas.xmm2px(self.points[p].pos.x), canvas.ymm2px(self.points[p].pos.y))
                canvas.Draw(Line(p0, p1, canvas.mm2px(self.width)), self.layers)
    
    def Move(self, pos):
        if self.placed==False:
            self.points[len(self.points)-1].Move(pos)
            self.points[len(self.points)-1].Update()
        elif self.placed:
            for point in self.points:
                point.pos = Point(point.pos.x+pos.x-self.pos.x, point.pos.y+pos.y-self.pos.y) 
                point.Update()
            self.pos = pos
            
        self.Update()

    def StartPlace(self):
        p = ObjectPoint()
        p.Select()
        self.points.append(p)
        self.AddNode(p)
        
    # return True if placement is complete
    def Place(self, pos):
        p = ObjectPoint(pos)
        p.Select()
        self.points.append(p)
        self.AddNode(p)
        return False

    def Select(self):
        if "Selection" not in self.layers:
            self.layers.append("Selection")
        for p in self.points:
            p.Select()

    def UnSelect(self):
        if "Selection" in self.layers:
            self.layers.remove("Selection")
        for p in self.points:
            p.UnSelect()

    def Description(self):
        coords = ""
        for p in self.points:
            coords = coords+"({},{})".format(p.pos.x, p.pos.y)
        return "Polyline width={} ".format(self.width)+coords

class ObjectText(EditorObject):
    def __init__(self, value, layers, font, pos=Point()):
        super(ObjectText, self).__init__(layers, pos)
        
        self.value = value
        self.font = font
        
        self.visible = True
        self.orientation = 'horizontal'
        
        self.center = ObjectPoint(pos)
        self.AddNode(self.center)
        
        self.Update()

    def Update(self):
        self.Clear()
        self.AddAnchor(self.pos)
    
    def Render(self, canvas):
        super(ObjectText, self).Render(canvas)

        font = Font(Point(canvas.mm2px(self.font.size.x), canvas.mm2px(self.font.size.y)), canvas.mm2px(self.font.thickness))
        canvas.SetFont(font)
        if self.orientation=='vertical':
            angle = -math.pi/2.
        else:
            angle = 0
        pos = Position(canvas.xmm2px(self.pos.x), canvas.ymm2px(self.pos.y), angle)
          
        canvas.Draw(Text(self.value, pos, anchor_x='center', anchor_y='center'), self.layers)            

    def Move(self, pos):
        self.pos = pos
        self.center.pos = pos 
        self.center.Update()
        self.Update()

    def Description(self):
        return "Text {} x={} y={}".format(self.value, self.pos.x, self.pos.y)
    
class ObjectTextReference(ObjectText):
    def __init__(self, value, font, pos=Point()):
        super(ObjectTextReference, self).__init__(value, ["F.SilkS"], font, pos)
        
    def Description(self):
        return "Reference {} x={} y={}".format(self.value, self.pos.x, self.pos.y)

class ObjectTextValue(ObjectText):
    def __init__(self, value, font, pos=Point()):
        super(ObjectTextValue, self).__init__(value, ["F.Fab"], font, pos)

    def Description(self):
        return "Value {} x={} y={}".format(self.value, self.pos.x, self.pos.y)

class ObjectTextUser(ObjectText):
    def __init__(self, value='', font=Font(), pos=Point()):
        super(ObjectTextUser, self).__init__(value, ["F.Fab"], font, pos)

    def Description(self):
        return "User {} x={} y={}".format(self.value, self.pos.x, self.pos.y)

class ObjectArc(EditorObject):
    def __init__(self, layers=[]):
        super(ObjectArc, self).__init__(layers, Point())
        
        self.width = 1 # mm
        
        self.points = [ObjectPoint(), ObjectPoint(), ObjectPoint()]
        for point in self.points:
            self.AddNode(point)
        
        self.placing_point = None

        self.Update()

    def Update(self):
        self.Clear()
        if self.placed:
            for p in self.points:
                self.AddAnchor(p.pos)
            r = self.points[0].pos.Distance(self.points[1].pos)
            pref = Point(self.points[0].pos.x+1, self.points[0].pos.y)
            angle_start = pref.GetAngle(self.points[0].pos, self.points[1].pos)
            angle_end = pref.GetAngle(self.points[0].pos, self.points[2].pos)
            self.AddAnchorArc(self.points[0].pos, r, angle_start, angle_end)
            
    def Render(self, canvas):
        super(ObjectArc, self).Render(canvas)
        
        p0 = self.points[0].pos
        p1 = self.points[1].pos
        p2 = self.points[2].pos

        p0px = Point(canvas.xmm2px(p0.x), canvas.ymm2px(p0.y))
        p1px = Point(canvas.xmm2px(p1.x), canvas.ymm2px(p1.y))
        p2px = Point(canvas.xmm2px(p2.x), canvas.ymm2px(p2.y))

        if self.placed==False and self.placing_point is None:
            return
        if self.placed or ( self.placing_point and self.placing_point>1 ):
            pref = Point(p0.x+1, p0.y)
            
            angle_start = p0.GetAngle(pref, p1)
#            angle_end = p0.GetAngle(pref, p2)
            angle = p0.GetAngle(p1, p2) 
            
            d = p0px.Distance(p1px)
            canvas.Draw(Arc(p0px, d, angle_start, angle_start+angle, canvas.mm2px(self.width)), self.layers)
        
    def Move(self, pos):
        if not self.placing_point is None:
            if self.placing_point<2:
                self.points[self.placing_point].Move(pos)
            elif self.placing_point==2:
                p0 = self.points[0].pos
                p1 = self.points[1].pos
                pref = Point(p0.x+1, p0.y)
                d = p0.Distance(p1)
                angle = p0.GetAngle(pref, pos)
                pos = Point(p0.x+d*math.cos(angle), p0.y+d*math.sin(angle))
                self.points[self.placing_point].Move(pos)
            else:
                self.pos = pos
        elif self.placed:
            for point in self.points:
                point.pos = Point(point.pos.x+pos.x-self.pos.x, point.pos.y+pos.y-self.pos.y) 
                point.Update()
            self.pos = pos
            
        self.Update()
        
    def StartPlace(self):
        self.placing_point = 0
        self.points[0].Select()
        
    # return True if placement is complete
    def Place(self, pos):
        self.placing_point = self.placing_point+1
        if self.placing_point>0 and self.placing_point<3:
            self.points[self.placing_point].pos = self.points[self.placing_point-1].pos
            self.points[self.placing_point].Update()
        if self.placing_point==3:
            self.placing_point = None
            self.placed = True
            return True
        return False

    def Angle(self):
        p0 = self.points[0].pos
        p1 = self.points[1].pos
        p2 = self.points[2].pos
        angle = p0.GetAngle(p1, p2)
        if angle<0:
            angle = angle+2.*math.pi
        return angle 
    
    def SetAngle(self, angle):
        p0 = self.points[0].pos
        p1 = self.points[1].pos
        p2 = self.points[2].pos
        return p0.SetAngle(p1, p2, angle)

    def Select(self):
        if "Selection" not in self.layers:
            self.layers.append("Selection")
        for p in self.points:
            p.Select()

    def UnSelect(self):
        if "Selection" in self.layers:
            self.layers.remove("Selection")
        for p in self.points:
            p.UnSelect()

    def Description(self):
        return "Arc x={} y={}".format(self.pos.x, self.pos.y)

class ObjectCircle(EditorObject):
    def __init__(self, layers=[]):
        super(ObjectCircle, self).__init__(layers, Point())
        
        self.width = 1 # mm
        
        self.points = [ObjectPoint(), ObjectPoint()]
        for point in self.points:
            self.AddNode(point)
        
        self.placing_point = None

        self.Update()

    def Update(self):
        self.Clear()
        if self.placed:
            for p in self.points:
                self.AddAnchor(p.pos)
            r = self.points[0].pos.Distance(self.points[1].pos)
            self.AddAnchorCircle(self.points[0].pos, self.points[1].pos)
            
    def Render(self, canvas):
        super(ObjectCircle, self).Render(canvas)
        
        p0 = self.points[0].pos
        p1 = self.points[1].pos

        p0px = Point(canvas.xmm2px(p0.x), canvas.ymm2px(p0.y))
        p1px = Point(canvas.xmm2px(p1.x), canvas.ymm2px(p1.y))

        if self.placed==False and self.placing_point is None:
            return
        if self.placed or ( self.placing_point and self.placing_point>0 ):
            canvas.Draw(Circle(p0px, p1px, canvas.mm2px(self.width)), self.layers)
        
    def Move(self, pos):
        if not self.placing_point is None:
            if self.placing_point<2:
                self.points[self.placing_point].Move(pos)
            else:
                self.pos = pos
        elif self.placed:
            for point in self.points:
                point.pos = Point(point.pos.x+pos.x-self.pos.x, point.pos.y+pos.y-self.pos.y) 
                point.Update()
            self.pos = pos
            
        self.Update()
        
    def StartPlace(self):
        self.placing_point = 0
        self.points[0].Select()
        
    # return True if placement is complete
    def Place(self, pos):
        self.placing_point = self.placing_point+1
        if self.placing_point>0 and self.placing_point<2:
            self.points[self.placing_point].pos = self.points[self.placing_point-1].pos
            self.points[self.placing_point].Update()
        if self.placing_point==2:
            self.placing_point = None
            self.placed = True
            return True
        return False

    def Select(self):
        if "Selection" not in self.layers:
            self.layers.append("Selection")
        for p in self.points:
            p.Select()

    def UnSelect(self):
        if "Selection" in self.layers:
            self.layers.remove("Selection")
        for p in self.points:
            p.UnSelect()

    def Description(self):
        return "Circle x={} y={}".format(self.pos.x, self.pos.y)

class EditorState(object):
    StateNone = 0
    StateStartMoving = 1
    StateMoving = 2
    StatePlacing = 3
    StateStartRotating = 4
    StateRotatingInitRef = 5
    StateRotating = 6
    StateMovingCanvas = 7
    
    def __init__(self, canvas, anchors_obj):
        self.canvas = canvas
        self.state = self.StateNone
        self.objs = []
        self.anchor_objs = anchors_obj
        
        self.initial_pos = None
        self.initial_angle_ref = None
        
        self.initial_origin = None
        self.initial_origin_pos = None
        
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
    
    def DoRotate(self):
        self.state = self.StateStartRotating
        
    def SetCursorPos(self, x, y, screenx, screeny):
        if self.state==self.StateMoving:
            for obj in self.objs:
                obj.Move(Point(obj.origin_pos.x+(x-self.initial_pos.x), obj.origin_pos.y+(y-self.initial_pos.y)))
        elif self.state==self.StatePlacing:                    
            self.objs[0].Move(Point(x, y))
        elif self.state==self.StateRotating:
            angle = self.initial_pos.GetAngle(self.initial_angle_ref, Point(x, y))
            for obj in self.objs:
                obj.Rotate(self.initial_pos, angle)
        elif self.state==self.StateMovingCanvas and self.initial_origin is not None:
            self.canvas.Origin(self.initial_origin.x+(screenx-self.initial_origin_pos.x), self.initial_origin.y+(screeny-self.initial_origin_pos.y))
            
    def DoLeftDown(self, x, y, screenx, screeny):
        if self.state==self.StateNone:
            self.state = self.StateMovingCanvas
            self.initial_origin = self.canvas.origin
            self.initial_origin_pos = Point(screenx, screeny)
            
    def DoLeftUp(self, x, y, screenx, screeny):
        if self.state==self.StateMovingCanvas:
            self.state = self.StateNone
            self.initial_origin = None
            self.initial_origin_pos = None
            
    def DoClick(self, x, y, screenx, screeny):
        if self.state==self.StateStartMoving:
            self.initial_pos = Point(x, y)
            self.state = self.StateMoving
            for obj in self.objs:
                obj.StartMove()
        elif self.state==self.StateMoving:
            self.Validate()
        elif self.state==self.StatePlacing:
            if self.objs[0].Place(Point(x, y)):
                self.Validate()
        elif self.state==self.StateStartRotating:
            self.initial_pos = Point(x, y)
            self.state = self.StateRotatingInitRef
            for obj in self.objs:
                obj.StartRotate()
        elif self.state==self.StateRotatingInitRef:
            self.initial_angle_ref = Point(x, y)
            self.state = self.StateRotating
        elif self.state==self.StateRotating:
            self.Validate()

    def DoDClick(self, x, y, screenx, screeny):
        if self.state==self.StatePlacing:
            self.Validate()
            self.state = self.StateNone

    def GetMovingObjects(self):
        res = []
        if self.state==self.StateMoving or self.state==self.StatePlacing or self.state==self.StateRotating:
            res = self.objs
        return res
    
    def GetObjects(self):
        return self.objs
    
class DrawFootprintFrame(DialogDrawFootprint): 
    def __init__(self, parent, filename):
        super(DrawFootprintFrame, self).__init__(parent)
        
        self.zoom = 1
        self.canvas = FootprintCanvas()
        self.selection = []
        self.magnet = 10
        
        self.filename = filename
        
        self.component_objects = EditorObject([])
        self.build_objects = EditorObject([])
        
        self.anchor_objects = EditorObject([])
        self.anchor_objects.AddNode(self.component_objects)
        self.anchor_objects.AddNode(self.build_objects)
        
        self.all_objects = EditorObject([])
        self.all_objects.AddNode(self.anchor_objects)
        
        self.state = EditorState(self.canvas, self.anchor_objects)
        
        self.current_panel = None

        self.current_pad_name = None
        
        # module elements
        self.footprint_name = ''
        self.footprint_timestamp = ''
        self.footprint_descr = ''
        self.footprint_tags = []
        
        # create manufacturers list
        self.tree_objects_manager = TreeManagerObjects(self.tree_objects, context_menu=self.menu_edit)
        self.tree_objects_manager.AddTextColumn("name")
        self.tree_objects_manager.OnSelectionChanged = self.onTreeMenuObjectsSelChanged
        self.tree_objects_manager.AppendCategory('Drawing')
        self.tree_objects_manager.AppendCategory('Part')
        
        # create layers list
        self.tree_layers_manager = TreeManagerLayers(self.tree_layers)
        self.tree_layers_manager.AddToggleColumn("visible")
        self.tree_layers_manager.AddToggleColumn("active")
        self.tree_layers_manager.AddTextColumn("name")
        #self.tree_layers_manager.OnSelectionChanged = self.onTreeMenuObjectsSelChanged

        # add origin 
        node = ObjectOrigin(Position(0, 0))
        self.build_objects.AddNode(node)

        # add cursor
        node = ObjectGrid(Position(0, 0), Position(1, 1), Position(10, 10))
        self.cursor = node
        self.all_objects.AddNode(self.cursor)
        
        # add default text fields
        self.part_reference = ObjectTextReference("REF**", Font(Point(1, 1), 0.15))
        self.component_objects.AddNode(self.part_reference)
        self.tree_objects_manager.AppendObject('Part', self.part_reference)
        self.part_value = ObjectTextValue("<value>", Font(Point(1, 1), 0.15))
        self.component_objects.AddNode(self.part_value)
        self.tree_objects_manager.AppendObject('Part', self.part_value)
#         self.part_user = ObjectTextUser("%R", Font(Point(1, 1), 0.15))
#         self.component_objects.AddNode(self.part_user)
#         self.tree_objects_manager.AppendObject('Part', self.part_user)

        # last used objects
        self.last_grid = None
        self.last_pad = None
        
        self.Bind(wx.EVT_CHAR_HOOK, self.keyPressed)

        self.canvas.Viewport(self.image_draw.GetRect().width, self.image_draw.GetRect().height)
        self.canvas.Origin(self.image_draw.GetRect().width/2, self.image_draw.GetRect().height/2)

        self.Load()
        self.LoadLayers()
        
        self.SelectObjects([])
        
    def Render(self):        
        self.canvas.Clear() #(["Editor"])
        img = self.canvas.Render(self.all_objects)
        self.image_draw.SetBitmap(wx.lib.wxcairo.BitmapFromImageSurface(img))

    def LoadLayers(self):
        for layer in self.canvas.layers:
            self.tree_layers_manager.AppendLayer(layer)
    
    def Load(self):
        if self.filename:
            mod = kicad_mod_file.KicadModFile()
            mod.LoadFile(self.filename)
            
            self.load_object(mod.parent)
        self.UpdateAll(self.all_objects)
    
    def Save(self):
        mod = kicad_mod_file.KicadModFile()
        
        module = kicad_mod_file.KicadModule()
        module.SetName(self.footprint_name)
        
        node = kicad_mod_file.KicadLayer()
        node.SetLayer("F.Cu")
        module.AddNode(node)
        
        node = kicad_mod_file.KicadTEdit()
        node.SetTimestamp(self.footprint_timestamp)
        module.AddNode(node)

        node = kicad_mod_file.KicadDescr()
        node.SetDescr(self.footprint_descr)
        module.AddNode(node)

        node = kicad_mod_file.KicadTags()
        for tag in self.footprint_tags:
            node.AddTag(tag)
        module.AddNode(node)

        node = kicad_mod_file.KicadAttr()
        node.SetAttr('smd')
        module.AddNode(node)

        mod.parent = module
        
        self.save_object(self.component_objects, module)
        mod.SaveFile("test.kicad_mod")
        
    def UpdateAll(self, obj):
        obj.Update()
        for node in obj.nodes:
            self.UpdateAll(node)
            
    def load_object(self, obj, stack=[], level=0):
        pop = False
        
        current = None
        if len(stack)>0:
            current = stack[len(stack)-1]
        
#         tab = ""
#         for i in range(0, level):
#             tab = tab+"  "
#         print "++", tab, len(stack), type(obj), type(current)
        
        if isinstance(obj, kicad_mod_file.KicadPad):
            current = ObjectPad()
            pop = True
            stack.append(current)
            current.name = obj.GetName()
            current.SetType(obj.GetType())
            current.SetShape(obj.GetShape())
            current.placed = True
            self.component_objects.AddNode(current)
            self.tree_objects_manager.AppendObject('Part', current)
        elif isinstance(obj, kicad_mod_file.KicadFPText):
            if obj.GetKind()=='value':
                current = self.part_value
            elif obj.GetKind()=='reference':
                current = self.part_reference
            else:
                current = ObjectTextUser()
                self.component_objects.AddNode(current)
                self.tree_objects_manager.AppendObject('Part', current)
            current.value = obj.GetValue()
            stack.append(current)
            pop = True
        elif isinstance(obj, kicad_mod_file.KicadFPArc):
            current = ObjectArc()
            pop = True
            stack.append(current)
            current.placed = True
            self.component_objects.AddNode(current)
            self.tree_objects_manager.AppendObject('Part', current)
        elif isinstance(obj, kicad_mod_file.KicadFPCircle):
            current = ObjectCircle()
            pop = True
            stack.append(current)
            current.placed = True
            self.component_objects.AddNode(current)
            self.tree_objects_manager.AppendObject('Part', current)
        elif isinstance(obj, kicad_mod_file.KicadFPLine):
            current = ObjectPolyline()
            pop = True
            stack.append(current)
            current.placed = True
            self.component_objects.AddNode(current)
            self.tree_objects_manager.AppendObject('Part', current)
        elif isinstance(obj, kicad_mod_file.KicadAt) and current:
            at = obj.GetAt()
            current.Move(at)
            if issubclass(type(current), ObjectText):
                if math.fabs(at.angle)>epsilon:
                    current.orientation = 'vertical'
            else:
                current.StartRotate()
                current.Rotate(current.pos, at.angle*math.pi/180.)
                current.Validate()
            self.tree_objects_manager.UpdateItem(self.tree_objects_manager.FindObject(current))
        elif isinstance(obj, kicad_mod_file.KicadSize) and current:
            size = obj.GetSize()
            current.size.x = size.x
            current.size.y = size.y
            self.tree_objects_manager.UpdateItem(self.tree_objects_manager.FindObject(current))
        elif isinstance(obj, kicad_mod_file.KicadCenter) and current:
            centre = obj.GetCenter()
            current.points[0].pos.x = centre.x
            current.points[1].pos.y = centre.y
            self.tree_objects_manager.UpdateItem(self.tree_objects_manager.FindObject(current))
        elif isinstance(obj, kicad_mod_file.KicadStart) and current:
            if isinstance(current, ObjectPad):
                current.Move(obj.GetStart())
            elif isinstance(current, ObjectPolyline):
                current.points.append(ObjectPoint(obj.GetStart()))
            elif isinstance(current, ObjectArc) or isinstance(current, ObjectCircle):
                current.points[0].pos = obj.GetStart()
            self.tree_objects_manager.UpdateItem(self.tree_objects_manager.FindObject(current))
        elif isinstance(obj, kicad_mod_file.KicadEnd) and current:
            if isinstance(current, ObjectPad):
                end = obj.GetEnd()
                start = current.GetPos()
                current.Move(Point((end.x-start.x)/2., (end.y-start.y)/2.))
                current.SetSize(Point(end.x-start.x, end.y-start.y))
            elif isinstance(current, ObjectPolyline):
                current.points.append(ObjectPoint(obj.GetEnd()))
            elif isinstance(current, ObjectArc) or isinstance(current, ObjectCircle):
                current.points[1].pos = obj.GetEnd()
            self.tree_objects_manager.UpdateItem(self.tree_objects_manager.FindObject(current))
        elif isinstance(obj, kicad_mod_file.KicadAngle) and current:
            if isinstance(current, ObjectArc):
                dx = current.points[0].pos.x-current.points[1].pos.x
                dy = current.points[0].pos.y-current.points[1].pos.y
                radius = math.sqrt(dx*dx+dy*dy)
                pref = Point(current.points[0].pos.x+1, current.points[0].pos.y)
                angle_start = current.points[0].pos.GetAngle(pref, current.points[1].pos)
                angle = obj.GetAngle()
                current.points[2].pos = Point(current.points[0].pos.x+radius*math.cos(angle_start+angle), current.points[0].pos.y+radius*math.sin(angle_start+angle))
        elif isinstance(obj, kicad_mod_file.KicadOffset) and current:
            if isinstance(current, ObjectPad):
                current.offset = obj.GetOffset()
            self.tree_objects_manager.UpdateItem(self.tree_objects_manager.FindObject(current))
        elif isinstance(obj, kicad_mod_file.KicadWidth) and current:
            width = obj.GetWidth()
            current.width = width
        elif isinstance(obj, kicad_mod_file.KicadThickness) and current:
            thickness = obj.GetThickness()
            current.thickness = thickness
        elif isinstance(obj, kicad_mod_file.KicadFont) and current:
            stack.append(current.font)
            pop = True
        elif isinstance(obj, kicad_mod_file.KicadItalic) and current:
            current.style = 'italic'
        elif isinstance(obj, kicad_mod_file.KicadLayer) and current:
            current.layers.append(obj.GetLayer())
        elif isinstance(obj, kicad_mod_file.KicadLayers) and current:
            current.layers = []
            for layer in obj.GetLayers():
                current.layers.append(layer)
        elif isinstance(obj, kicad_mod_file.KicadModule):
            self.SetFootprintName(obj.GetName())
        elif isinstance(obj, kicad_mod_file.KicadTEdit):
            self.SetFootprintTimestamp(obj.GetTimestamp())
        elif isinstance(obj, kicad_mod_file.KicadDescr):
            self.SetFootprintDescr(obj.GetDescr())
        elif isinstance(obj, kicad_mod_file.KicadTags):
            self.SetFootprintTags(obj.GetTags())
        elif isinstance(obj, kicad_mod_file.KicadDrill) and current:
            if obj.GetDrill() is not None:
                current.drill = obj.GetDrill()
                if obj.IsOval():
                    current.drill_type = 'oval'
        elif isinstance(obj, kicad_mod_file.KicadDieLength) and current:
            current.die_length = obj.GetDieLength()
        elif isinstance(obj, kicad_mod_file.KicadRectDelta) and current:
            rect = obj.GetRectDelta()
            if math.fabs(rect.x)>epsilon:
                current.trapezoidal_delta = rect.x
                current.trapezoidal_direction = 'vert'
            elif math.fabs(rect.y)>epsilon:
                current.trapezoidal_delta = rect.y
                current.trapezoidal_direction = 'horz'
        elif isinstance(obj, kicad_mod_file.KicadSolderMaskMargin) and current:
            current.solder_mask_margin = obj.GetSolderMaskMargin()
        elif isinstance(obj, kicad_mod_file.KicadSolderPasteMargin) and current:
            current.solder_paste_margin = obj.GetSolderPasteMargin()
        elif isinstance(obj, kicad_mod_file.KicadClearance) and current:
            current.clearance = obj.GetClearance()
        elif isinstance(obj, kicad_mod_file.KicadThermalWidth) and current:
            current.thermal_width = obj.GetThermalWidth()
        elif isinstance(obj, kicad_mod_file.KicadThermalGap) and current:
            current.thermal_gap = obj.GetThermalGap()
        elif isinstance(obj, kicad_mod_file.KicadSolderPasteMarginRatio) and current:
            current.solder_paste_margin_ratio = obj.GetSolderPasteMarginRatio()
        elif isinstance(obj, kicad_mod_file.KicadZoneConnect) and current:
            current.zone_connect = obj.GetZoneConnect()
        elif isinstance(obj, kicad_mod_file.KicadHide) and current:
            current.visible = False
    
        for node in obj.nodes:
            self.load_object(node, stack, level+1)
        
        if pop:
            stack.pop()
    
    def save_object(self, obj, parent):
        if isinstance(obj, ObjectArc):
            arc = kicad_mod_file.KicadFPArc()
            parent.AddNode(arc)
            node = kicad_mod_file.KicadStart()
            node.AddAttribute(str(obj.points[0].pos.x))
            node.AddAttribute(str(obj.points[0].pos.y))
            arc.AddNode(node)
            node = kicad_mod_file.KicadEnd()
            node.AddAttribute(str(obj.points[1].pos.x))
            node.AddAttribute(str(obj.points[1].pos.y))
            arc.AddNode(node)
            node = kicad_mod_file.KicadAngle()
            node.AddAttribute(str(obj.Angle()*180./math.pi))
            arc.AddNode(node)
            node = kicad_mod_file.KicadLayer()
            node.AddAttribute(obj.layers[0])
            arc.AddNode(node)
            node = kicad_mod_file.KicadWidth()
            node.AddAttribute(str(obj.width))
            arc.AddNode(node)
        elif isinstance(obj, ObjectCircle):
            circle = kicad_mod_file.KicadFPCircle()
            parent.AddNode(circle)
            node = kicad_mod_file.KicadCenter()
            node.AddAttribute(str(obj.points[0].pos.x))
            node.AddAttribute(str(obj.points[0].pos.y))
            circle.AddNode(node)
            node = kicad_mod_file.KicadEnd()
            node.AddAttribute(str(obj.points[1].pos.x))
            node.AddAttribute(str(obj.points[1].pos.y))
            circle.AddNode(node)
            node = kicad_mod_file.KicadLayer()
            node.AddAttribute(obj.layers[0])
            circle.AddNode(node)
            node = kicad_mod_file.KicadWidth()
            node.AddAttribute(str(obj.width))
            circle.AddNode(node)
        elif isinstance(obj, ObjectPad):
            pad = kicad_mod_file.KicadPad()
            parent.AddNode(pad)
            pad.SetName(obj.name)
            pad.SetType(obj.type)
            pad.SetShape(obj.shape)
            node = kicad_mod_file.KicadAt()
            node.AddAttribute(str(obj.pos.x))
            node.AddAttribute(str(obj.pos.y))
            node.AddAttribute(str(obj.angle*180./math.pi))
            pad.AddNode(node)
            node = kicad_mod_file.KicadSize()
            node.AddAttribute(str(obj.size.x))
            node.AddAttribute(str(obj.size.y))
            pad.AddNode(node)
            if math.fabs(obj.trapezoidal_delta)>epsilon:
                node = kicad_mod_file.KicadRectDelta()
                if obj.trapezoidal_direction=='vert':
                    node.AddAttribute(str(obj.trapezoidal_delta))
                    node.AddAttribute(str(0))
                else:
                    node.AddAttribute(str(0))
                    node.AddAttribute(str(obj.trapezoidal_delta))
                pad.AddNode(node)
            drill = None
            if obj.type=='thru_hole' or obj.type=='np_thru_hole':
                drill = kicad_mod_file.KicadDrill()
                if obj.drill_type=='oval':
                    drill.AddAttribute('oval')
                    drill.AddAttribute(obj.drill.x)
                    drill.AddAttribute(obj.drill.y)
                else:
                    drill.AddAttribute(obj.drill.x)
                pad.AddNode(drill)
            
            if math.fabs(obj.offset.x)>epsilon or math.fabs(obj.offset.y)>epsilon:
                if drill is None:
                    drill = kicad_mod_file.KicadDrill()
                    pad.AddNode(drill)
                node = kicad_mod_file.KicadOffset()
                node.AddAttribute(str(obj.offset.x))
                node.AddAttribute(str(obj.offset.y))
                drill.AddNode(node)
            if math.fabs(obj.die_length)>epsilon:
                node = kicad_mod_file.KicadDieLength()
                node.AddAttribute(str(obj.die_length))
                pad.AddNode(node)
            if math.fabs(obj.solder_mask_margin)>epsilon:
                node = kicad_mod_file.KicadSolderMaskMargin()
                node.AddAttribute(str(obj.solder_mask_margin))
                pad.AddNode(node)
            if math.fabs(obj.solder_paste_margin)>epsilon:
                node = kicad_mod_file.KicadSolderPasteMargin()
                node.AddAttribute(str(obj.solder_paste_margin))
                pad.AddNode(node)
            if math.fabs(obj.clearance)>epsilon:
                node = kicad_mod_file.KicadClearance()
                node.AddAttribute(str(obj.clearance))
                pad.AddNode(node)
            if math.fabs(obj.thermal_width)>epsilon:
                node = kicad_mod_file.KicadThermalWidth()
                node.AddAttribute(str(obj.thermal_width))
                pad.AddNode(node)
            if math.fabs(obj.thermal_gap)>epsilon:
                node = kicad_mod_file.KicadThermalGap()
                node.AddAttribute(str(obj.thermal_gap))
                pad.AddNode(node)
            if math.fabs(obj.solder_paste_margin_ratio)>epsilon:
                node = kicad_mod_file.KicadSolderPasteMarginRatio()
                node.AddAttribute(str(obj.solder_paste_margin_ratio))
                pad.AddNode(node)
            if obj.zone_connect is not None:
                node = kicad_mod_file.KicadZoneConnect()
                node.AddAttribute(str(obj.zone_connect))
                pad.AddNode(node)
                                
            node = kicad_mod_file.KicadLayers()
            for layer in obj.layers:
                if layer!='Selection':
                    node.AddAttribute(layer)
            pad.AddNode(node)
            
        elif isinstance(obj, ObjectPolyline):
            pp = None
            for p in obj.points:
                if pp is not None:
                    line = kicad_mod_file.KicadFPLine()
                    parent.AddNode(line)
                    node = kicad_mod_file.KicadStart()
                    node.AddAttribute(p.pos.x)
                    node.AddAttribute(p.pos.y)
                    line.AddNode(node)
                    node = kicad_mod_file.KicadEnd()
                    node.AddAttribute(pp.pos.x)
                    node.AddAttribute(pp.pos.y)
                    line.AddNode(node)
                    node = kicad_mod_file.KicadLayer()
                    node.AddAttribute(obj.layers[0])
                    line.AddNode(node)
                    node = kicad_mod_file.KicadWidth()
                    node.AddAttribute(obj.width)
                    line.AddNode(node)
                pp = p
        elif isinstance(obj, ObjectTextReference) or isinstance(obj, ObjectTextUser) or isinstance(obj, ObjectTextValue):
            text = kicad_mod_file.KicadFPText()
            parent.AddNode(text)
            if isinstance(obj, ObjectTextReference):
                text.AddAttribute('reference')
            elif isinstance(obj, ObjectTextUser):
                text.AddAttribute('user')
            elif isinstance(obj, ObjectTextValue):
                text.AddAttribute('value')
            text.AddAttribute(obj.value)
            node = kicad_mod_file.KicadAt()
            node.AddAttribute(obj.pos.x)
            node.AddAttribute(obj.pos.y)
            if obj.orientation=='vertical':
                node.AddAttribute('90')
            text.AddNode(node)
            node = kicad_mod_file.KicadLayer()
            node.AddAttribute(obj.layers[0])
            text.AddNode(node)
            if obj.visible==False:
                node = kicad_mod_file.KicadHide()
                text.AddNode(node)
            effects = kicad_mod_file.KicadEffects()
            text.AddNode(effects)
            
            font = kicad_mod_file.KicadFont()
            effects.AddNode(font)
            node = kicad_mod_file.KicadSize()
            node.AddAttribute(obj.font.size.x)
            node.AddAttribute(obj.font.size.y)
            font.AddNode(node)
            node = kicad_mod_file.KicadThickness()
            node.AddAttribute(obj.font.thickness)
            font.AddNode(node)
            if obj.font.style=='italic':
                node = kicad_mod_file.KicadItalic()
                font.AddNode(node)

        for node in obj.nodes:
            self.save_object(node, parent)
    
    def SetFootprintName(self, name):
        self.footprint_name = name
#        self.part_value.value = name
#        self.part_value.Update()

    def SetFootprintTimestamp(self, timestamp):
        self.footprint_timestamp = timestamp

    def SetFootprintDescr(self, descr):
        self.footprint_descr = descr

    def SetFootprintTags(self, tags):
        self.footprint_tags = tags

    def SelectObjects(self, objs):
#         for obj in self.state.GetObjects():
#             if obj.Placed()==False:
#                 self.tree_objects_manager.DeleteObject(obj)
#                 if obj.Parent():
#                     obj.Parent().RemoveNode(obj)
        self.state.Cancel()
        
        self.selection = objs
        self.state.SelectObjects(objs)
        
        if self.current_panel:
            self.current_panel.Destroy()
        
        if len(objs)==1 and isinstance(objs[0], ObjectGrid):
            self.current_panel = EditGridFrame(self.panel_edit_object, self.Render, objs[0])
            self.last_grid = objs[0]
        elif len(objs)==1 and isinstance(objs[0], ObjectDimension):
            self.current_panel = EditDimensionFrame(self.panel_edit_object, self.Render, objs[0])
        elif len(objs)==1 and isinstance(objs[0], ObjectPad):
            self.current_panel = EditPadFrame(self.panel_edit_object, self.Render, objs[0])
            self.last_pad = objs[0]
        elif len(objs)==1 and isinstance(objs[0], ObjectLine):
            self.current_panel = EditLineFrame(self.panel_edit_object, self.Render, objs[0])
        elif len(objs)==1 and isinstance(objs[0], ObjectAngle):
            self.current_panel = EditAngleFrame(self.panel_edit_object, self.Render, objs[0])
        elif len(objs)==1 and isinstance(objs[0], ObjectArc):
            self.current_panel = EditArcFrame(self.panel_edit_object, self.Render, objs[0])
        elif len(objs)==1 and isinstance(objs[0], ObjectPolyline):
            self.current_panel = EditPolylineFrame(self.panel_edit_object, self.Render, objs[0])
        elif len(objs)==1 and isinstance(objs[0], ObjectCircle):
            self.current_panel = EditCircleFrame(self.panel_edit_object, self.Render, objs[0])
        elif len(objs)==1 and issubclass(type(objs[0]), ObjectText):
            self.current_panel = EditTextFrame(self.panel_edit_object, self.Render, objs[0])
        else:
            self.current_panel = EditFootprintFrame(self.panel_edit_object, self.Render, self)
            
        if len(objs)==1:
            print "**", objs[0].Description()
                 
    def keyPressed( self, event):
        print "keyPressed", type(event), event.GetKeyCode(), event.GetRawKeyFlags(), event.ControlDown()

        if event.GetKeyCode()==27:
            # cancel any operation
            self.SelectObjects([])
        
        event.Skip(True)

    def onImageDrawLeftDClick( self, event ):
        pospx = event.GetPosition()
        pos = Point(self.canvas.xpx2mm(pospx.x), self.canvas.ypx2mm(pospx.y))
        
        self.cursor.pos = pos
        types = [Anchor, AnchorLine, AnchorArc, AnchorCircle]
        for t in types:
            [distance, anchor] = self.anchor_objects.FindAnchor(t, pos, self.state.GetMovingObjects())
            if not distance is None and self.canvas.mm2px(distance)<self.magnet:
                pos = anchor.Pos(pos)
                #pospx = Point(self.canvas.xpx2mm(pos.x), self.canvas.ypx2mm(pos.y))
                self.cursor.pos = pos
                break
        self.cursor.Update()
        
        self.state.DoDClick(pos.x, pos.y, pospx.x, pospx.y)
        self.Render()
    
        if self.current_panel:
            self.current_panel.Update()
    
    def onImageDrawLeftDown( self, event ):
        pospx = event.GetPosition()
        pos = Point(self.canvas.xpx2mm(pospx.x), self.canvas.ypx2mm(pospx.y))
                
        self.state.DoLeftDown(pos.x, pos.y, pospx.x, pospx.y)
        self.Render()
    
    def onImageDrawLeftUp( self, event ):
        pospx = event.GetPosition()
        pos = Point(self.canvas.xpx2mm(pospx.x), self.canvas.ypx2mm(pospx.y))
        
        self.cursor.pos = pos
        types = [Anchor, AnchorLine, AnchorArc, AnchorCircle]
        for t in types:
            [distance, anchor] = self.anchor_objects.FindAnchor(t, pos, self.state.GetMovingObjects())
            if not distance is None and self.canvas.mm2px(distance)<self.magnet:
                pos = anchor.Pos(pos)
                #pospx = Point(self.canvas.xpx2mm(pos.x), self.canvas.ypx2mm(pos.y))
                self.cursor.pos = pos
                break
        self.cursor.Update()
        
        self.state.DoLeftUp(pos.x, pos.y, pospx.x, pospx.y)
        self.state.DoClick(pos.x, pos.y, pospx.x, pospx.y)
        self.Render()
    
        if self.current_panel:
            self.current_panel.Update()
        
    def onImageDrawMiddleDClick( self, event ):
        event.Skip()
    
    def onImageDrawMiddleDown( self, event ):
        event.Skip()
    
    def onImageDrawMiddleUp( self, event ):
        event.Skip()

    def onImageDrawMotion( self, event ):
        pospx = event.GetPosition()
        pos = Point(self.canvas.xpx2mm(pospx.x), self.canvas.ypx2mm(pospx.y))
        
        self.cursor.pos = pos
        types = [Anchor, AnchorLine, AnchorArc, AnchorCircle]
        for t in types:
            [distance, anchor] = self.anchor_objects.FindAnchor(t, pos, self.state.GetMovingObjects())
            if not distance is None and self.canvas.mm2px(distance)<self.magnet:
                pos = anchor.Pos(pos)
                #pospx = Point(self.canvas.xpx2mm(pos.x), self.canvas.ypx2mm(pos.y))
                self.cursor.pos = pos
                break
        self.cursor.Update()

        self.state.SetCursorPos(pos.x, pos.y, pospx.x, pospx.y)
        self.Render()
        
        status = self.GetStatusBar()
        status.SetStatusText("x: "+str(self.cursor.pos.x)+"mm, y: "+str(self.cursor.pos.y)+"mm", 0)
        status.SetStatusText("x: "+str(pos.x)+"px, y: "+str(pos.y)+"px", 1)
        status.SetStatusText("zoom: "+str(self.zoom), 2)

        if self.current_panel:
            self.current_panel.Update()
        
    def onImageDrawMouseWheel( self, event ):
        #print type(event)
        pass
    
    def onImageDrawRightDClick( self, event ):
        event.Skip()
    
    def onImageDrawRightDown( self, event ):
        event.Skip()
    
    def onImageDrawRightUp( self, event ):
        event.Skip()
    
    def onMenuDrawPadSelection( self, event ):
        node = ObjectPad()
        
        if self.current_pad_name is None:
            self.current_pad_name = 1
        else:
            self.current_pad_name = self.current_pad_name+1
        node.name = str(self.current_pad_name)
        
        self.component_objects.AddNode(node)
        obj = self.tree_objects_manager.AppendObject('Part', node)
        self.tree_objects_manager.Select(obj)
        self.state.DoPlace(node)

        if self.current_panel:
            self.current_panel.Destroy()
        self.current_panel = EditPadFrame(self.panel_edit_object, self.Render, node)

    def onMenuToolDimensionSelection( self, event ):
        node = ObjectDimension()
            
        self.build_objects.AddNode(node)
        obj = self.tree_objects_manager.AppendObject('Drawing', node)
        self.tree_objects_manager.Select(obj)
        self.state.DoPlace(node)

        if self.current_panel:
            self.current_panel.Destroy()
        self.current_panel = EditDimensionFrame(self.panel_edit_object, self.Render, node)
    
    def onMenuToolGridSelection( self, event ):
        if self.last_grid:
            node = ObjectGrid(self.last_grid.pos, self.last_grid.count, self.last_grid.spacing)
        else:
            node = ObjectGrid(Position(0, 0), Position(20, 20), Position(10, 10))
            
        self.build_objects.AddNode(node)
        obj = self.tree_objects_manager.AppendObject('Drawing', node)
        self.tree_objects_manager.Select(obj)
        self.state.DoPlace(node)

        if self.current_panel:
            self.current_panel.Destroy()
        self.current_panel = EditGridFrame(self.panel_edit_object, self.Render, node)
        self.last_grid = node
        
    def onMenuToolRulerSelection( self, event ):
        event.Skip()

    def onMenuToolAngleSelection( self, event ):
        node = ObjectAngle()
            
        self.build_objects.AddNode(node)
        obj = self.tree_objects_manager.AppendObject('Drawing', node)
        self.tree_objects_manager.Select(obj)
        self.state.DoPlace(node)

        if self.current_panel:
            self.current_panel.Destroy()
        self.current_panel = EditAngleFrame(self.panel_edit_object, self.Render, node)
    
    def onMenuToolVerticalSelection( self, event ):
        node = ObjectVerticalLine()
            
        self.build_objects.AddNode(node)
        obj = self.tree_objects_manager.AppendObject('Drawing', node)
        self.tree_objects_manager.Select(obj)
        self.state.DoPlace(node)

        if self.current_panel:
            self.current_panel.Destroy()
        #self.current_panel = EditLineFrame(self.panel_edit_object, self.Render, node)
    
    def onMenuToolHorizontalSelection( self, event ):
        node = ObjectHorizontalLine()
            
        self.build_objects.AddNode(node)
        obj = self.tree_objects_manager.AppendObject('Drawing', node)
        self.tree_objects_manager.Select(obj)
        self.state.DoPlace(node)

        if self.current_panel:
            self.current_panel.Destroy()
        #self.current_panel = EditLineFrame(self.panel_edit_object, self.Render, node)
    
    def onMenuToolLineSelection( self, event ):
        node = ObjectLine()
            
        self.build_objects.AddNode(node)
        obj = self.tree_objects_manager.AppendObject('Drawing', node)
        self.tree_objects_manager.Select(obj)
        self.state.DoPlace(node)

        if self.current_panel:
            self.current_panel.Destroy()
        self.current_panel = EditLineFrame(self.panel_edit_object, self.Render, node)
    
    def onMenuZoomResetSelection( self, event ):
        event.Skip()

    def onMenuEditMoveSelection( self, event ):
        self.state.DoMove()
    
    def onMenuEditRemoveSelection( self, event ):
        event.Skip()

    def onMenuEditRotateSelection( self, event ):
        self.state.DoRotate()

    def onTreeMenuObjectsSelChanged( self, event ):
        item = self.tree_objects.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_objects_manager.ItemToObject(item)
        if isinstance(obj, DataModelObject):
            self.SelectObjects([obj.obj])
        self.Render()
    
    def onMenuZoomInSelection( self, event ):
        self.canvas.Zoom(self.canvas.zoom*2.)
        self.Render()
    
    def onMenuZoomOutSelection( self, event ):
        self.canvas.Zoom(self.canvas.zoom/2.)
        self.Render()
    
    def onImageDrawMouseEvents( self, event ):
        event.Skip()
            
    def onMenuDrawPadRowSelection( self, event ):
        event.Skip()
    
    def onMenuDrawPadArraySelection( self, event ):
        event.Skip()
    
    def onMenuDrawPolylineSelection( self, event ):
        item = self.tree_layers.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_layers_manager.ItemToObject(item)
        if obj.layer.active==False:
            return
        
        node = ObjectPolyline([obj.layer.name])
            
        self.build_objects.AddNode(node)
        obj = self.tree_objects_manager.AppendObject('Part', node)
        self.tree_objects_manager.Select(obj)
        self.state.DoPlace(node)

        if self.current_panel:
            self.current_panel.Destroy()
        self.current_panel = EditPolylineFrame(self.panel_edit_object, self.Render, node)
    
    def onMenuDrawArcSelection( self, event ):
        item = self.tree_layers.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_layers_manager.ItemToObject(item)
        if obj.layer.active==False:
            return
        node = ObjectArc([obj.layer.name])
            
        self.build_objects.AddNode(node)
        obj = self.tree_objects_manager.AppendObject('Part', node)
        self.tree_objects_manager.Select(obj)
        self.state.DoPlace(node)

        if self.current_panel:
            self.current_panel.Destroy()
        self.current_panel = EditArcFrame(self.panel_edit_object, self.Render, node)
        
    def onMenuEditDuplicateSelection( self, event ):
        event.Skip()
    
    def onMenuDrawCircleSelection( self, event ):
        item = self.tree_layers.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_layers_manager.ItemToObject(item)
        if obj.layer.active==False:
            return
        node = ObjectCircle([obj.layer.name])
            
        self.build_objects.AddNode(node)
        obj = self.tree_objects_manager.AppendObject('Part', node)
        self.tree_objects_manager.Select(obj)
        self.state.DoPlace(node)

        if self.current_panel:
            self.current_panel.Destroy()
        self.current_panel = EditCircleFrame(self.panel_edit_object, self.Render, node)
    
    def onMenuFileSaveAsSelection( self, event ):
        event.Skip()

    def onMenuFileSaveSelection( self, event ):
        self.Save()

    def onMenuDrawTextSelection( self, event ):
        item = self.tree_layers.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_layers_manager.ItemToObject(item)
        if obj.layer.active==False:
            return
        node = ObjectTextUser([obj.layer.name])
            
        self.build_objects.AddNode(node)
        obj = self.tree_objects_manager.AppendObject('Part', node)
        self.tree_objects_manager.Select(obj)
        self.state.DoPlace(node)

        if self.current_panel:
            self.current_panel.Destroy()
        self.current_panel = EditTextFrame(self.panel_edit_object, self.Render, node)
        