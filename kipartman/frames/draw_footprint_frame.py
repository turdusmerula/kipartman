from dialogs.dialog_draw_footprint import DialogDrawFootprint
from frames.frame_draw_footprint.edit_grid_frame import EditGridFrame
from frames.frame_draw_footprint.edit_dimension_frame import EditDimensionFrame
from frames.frame_draw_footprint.edit_line_frame import EditLineFrame
from kicad.Canvas import *
import wx.lib.wxcairo
import helper.tree
from operator import pos
from frames.frame_draw_footprint.edit_pad_frame import EditPadFrame
import numpy

epsilon=1e-9

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
                
    def FindObject(self, obj):
        for data in self.data:
            if isinstance(data, DataModelObject) and data.obj==obj:
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

    def DeleteObject(self, obj):
        objobj = self.FindObject(obj)
        if objobj is None:
            return None
        self.DeleteItem(objobj.parent, objobj)
        
class Anchor(object):
    def __init__(self, parent, pos):
        self.pos = pos # mm
        self.parent = parent
        
    def Distance(self, pospx, canvas):
        dx = pospx.x-canvas.xmm2px(self.pos.x)
        dy = pospx.y-canvas.ymm2px(self.pos.y)
        return math.sqrt(dx*dx+dy*dy)
    
    def Pos(self, point=None):
        return self.pos
    
class AnchorLine(object):
    def __init__(self, parent, line):
        self.line = line
        
    def Distance(self, pospx, canvas):
        p = Point(canvas.xpx2mm(pospx.x), canvas.ypx2mm(pospx.y))
        pp = self.line.get_projection(p)
        dx = p.x-pp.x
        dy = p.y-pp.y
        return canvas.mm2px(math.sqrt(dx*dx+dy*dy))

    # return projection of point on line
    def Pos(self, point=None):
        return self.line.get_projection(point)

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

    # find closest anchor to position in radius
    # priority: points then intersections, then lines
    # TODO: lines intersections 
    def FindAnchor(self, pos, canvas, exclude_objects=[]):
        [min_distance, min_anchor] = self.r_find_anchor(self, pos, canvas, exclude_objects, min_distance=None, min_anchor=None)
        if min_anchor is None:
            [min_distance, min_anchor] = self.r_find_anchor_line(self, pos, canvas, exclude_objects, min_distance=None, min_anchor=None)
        return [min_distance, min_anchor] 
    
    def r_find_anchor(self, obj, pos, canvas, exclude_objects=[], min_distance=None, min_anchor=None):
        if obj in exclude_objects:
            return [min_distance, min_anchor]
        
        for anchor in obj.anchors:
            if isinstance(anchor, Anchor):
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

    def r_find_anchor_line(self, obj, pos, canvas, exclude_objects=[], min_distance=None, min_anchor=None):
        if obj in exclude_objects:
            return [min_distance, min_anchor]
        
        for anchor in obj.anchors:
            if isinstance(anchor, AnchorLine):
                distance = anchor.Distance(pos, canvas)
                if distance<=self.radius:
                    if min_distance and distance<min_distance:
                        min_distance = distance
                        min_anchor = anchor
                    elif not min_distance:
                        min_distance = distance
                        min_anchor = anchor

        for node in obj.nodes:
            [min_distance, min_anchor] = self.r_find_anchor_line(node, pos, canvas, exclude_objects, min_distance, min_anchor)
                
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
        if "selection" not in self.layers:
            self.layers.append("selection")
        for node in self.nodes:
            node.Select()
            
    def UnSelect(self):
        if "selection" in self.layers:
            self.layers.remove("selection")
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
        if "anchor" not in self.layers:
            self.layers.append("anchor")
    
    def UnSelect(self):
        if "anchor" in self.layers:
            self.layers.remove("anchor")
        
# dimension object
class ObjectDimension(EditorObject):
    def __init__(self):
        super(ObjectDimension, self).__init__(["editor"], Point())
        
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
        if "selection" not in self.layers:
            self.layers.append("selection")
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

        dx = p1.x-p0.x
        dy = p1.y-p0.y
        
        if math.fabs(p1.x-p0.x)<epsilon:
            if dy>=0:
                self.points[1].pos.y = p0.y+size
            else:
                self.points[1].pos.y = p0.y-size                
        else:
            
            [p0p1a, p0p1b] = self.get_ab(p1, p0)
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

# line object
class ObjectLine(EditorObject):
    def __init__(self):
        super(ObjectLine, self).__init__(["editor"], Point())
        
        self.width = 1 # px

        self.points = [ObjectPoint(), ObjectPoint()]
        for point in self.points:
            self.AddNode(point)

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
        if "selection" not in self.layers:
            self.layers.append("selection")
    
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
        super(ObjectAngle, self).__init__(["editor"], Point())
        
        self.width = 1 # px
        self.font = Font(Point(15, 15), 1)
        
        self.points = [ObjectPoint(), ObjectPoint(), ObjectPoint()]
        for point in self.points:
            self.AddNode(point)
        
        self.placing_point = None
        
        self.text_point = Point()
        
        self.Update()

    def Update(self):
        self.Clear()
        self.AddAnchor(Point((self.points[0].pos.x+self.points[1].pos.x)/2., (self.points[0].pos.y+self.points[1].pos.y)/2.))
             
    def get_p0p1_center(self):
        p0 = self.points[0].pos
        p1 = self.points[1].pos
        
        pcx = math.fabs(p0.x+p1.x)
        pcy = math.fabs(p0.y+p1.y)
        
        return Point(pcx, pcy)
    
    def get_ab(self, p0, p1):
        a = (p1.y-p0.y)/(p1.x-p0.x)
        b = p0.y-a*p0.x
        return [a, b]
    
    def get_b(self, a, p0):
        b = p0.y-a*p0.x
        return b

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
        
        pc = self.get_p0p1_center()
        
        # p0 p1 line equation
        
        if math.fabs(p1.x-p0.x)<epsilon:
            p3 = Point(p2.x, p0.y)
            p4 = Point(p2.x, p1.y)
        else:
            [p0p1a, p0p1b] = self.get_ab(p0, p1)
            # parralel to p0p1 passing by p2
            p2b = self.get_b(p0p1a, p2)
            
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
        if "selection" not in self.layers:
            self.layers.append("selection")
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

        dx = p1.x-p0.x
        dy = p1.y-p0.y
        
        if math.fabs(p1.x-p0.x)<epsilon:
            if dy>=0:
                self.points[1].pos.y = p0.y+size
            else:
                self.points[1].pos.y = p0.y-size                
        else:
            
            [p0p1a, p0p1b] = self.get_ab(p1, p0)
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

class ObjectPad(EditorObject):
    def __init__(self):
        super(ObjectPad, self).__init__(["F.Cu"], Point())
        self.type = 'smd' # smd or thru_hole
        self.shape = 'rect' # rect or oval
        self.size = Point()
        self.drill = 0.
        
        self.points = []
        self.placing_point = None
        
        self.SetShape(self.shape)
        
    def SetType(self, type):
        self.type = type
            
        self.UpdatePoints()
        self.Update()

    def SetShape(self, shape):
        self.shape = shape
            
        
        self.points = []
        self.ClearNodes()
        if self.shape=='rect':
            self.points = [ ObjectPoint(),
                            ObjectPoint(), ObjectPoint(), ObjectPoint(), ObjectPoint(),
                            ObjectPoint(), ObjectPoint(), ObjectPoint(), ObjectPoint()
                        ]
        elif self.shape=='oval':
            self.points = [ObjectPoint(), 
                           ObjectPoint(), ObjectPoint(), ObjectPoint(), ObjectPoint()]
        
        self.UpdatePoints()
        for point in self.points:
            self.AddNode(point)        
        self.Update()
        
    def SetSize(self, size):
        self.size = size
            
        self.UpdatePoints()
        self.Update()
        
    def UpdatePoints(self):
        dx = self.size.x/2.
        dy = self.size.y/2.

        self.points[0].Move(self.pos)
        if self.shape=='rect':
            self.points[1].Move(Point(self.pos.x-dx, self.pos.y-dy))
            self.points[2].Move(Point(self.pos.x+dx, self.pos.y-dy))
            self.points[3].Move(Point(self.pos.x+dx, self.pos.y+dy))
            self.points[4].Move(Point(self.pos.x-dx, self.pos.y+dy))
            self.points[5].Move(Point(self.pos.x,    self.pos.y-dy))
            self.points[6].Move(Point(self.pos.x+dx, self.pos.y))
            self.points[7].Move(Point(self.pos.x,    self.pos.y+dy))
            self.points[8].Move(Point(self.pos.x-dx, self.pos.y))
        elif self.shape=='oval':
            self.points[1].Move(Point(self.pos.x,    self.pos.y-dy))
            self.points[2].Move(Point(self.pos.x+dx, self.pos.y))
            self.points[3].Move(Point(self.pos.x,    self.pos.y+dy))
            self.points[4].Move(Point(self.pos.x-dx, self.pos.y))
        
        if math.fabs(self.angle)>epsilon:
            for p in self.points:
                p.StartRotate()
                p.Rotate(self.pos, self.angle)
        
    def Render(self, canvas):
        super(ObjectPad, self).Render(canvas)
        
        pos = Position(canvas.xmm2px(self.pos.x), canvas.ymm2px(self.pos.y), self.angle)
        size = Point(canvas.mm2px(self.size.x), canvas.mm2px(self.size.y))
        drill = canvas.mm2px(self.drill)
        
        if self.placed or ( self.placing_point is not None and self.placing_point==1):
            if self.shape=='rect':
                points = []
                for p in range(1, 5):
                    points.append(Point(canvas.xmm2px(self.points[p].pos.x), canvas.ymm2px(self.points[p].pos.y)))
                points.append(points[0])
                canvas.Draw(PolyLine(points, width=1, fill=True), ["F.Cu", "B.Cu"])
        
    def Select(self):
        if "selection" not in self.layers:
            self.layers.append("selection")
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
            self.UpdatePoints()
            
        self.Update()

    def Rotate(self, origin, angle):
        self.pos = self.origin_pos.Rotate(origin, angle)
        self.angle = self.origin_angle+angle
        self.UpdatePoints()
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
            
class EditorState(object):
    StateNone = 0
    StateStartMoving = 1
    StateMoving = 2
    StatePlacing = 3
    StateStartRotating = 4
    StateRotatingInitRef = 5
    StateRotating = 6
    
    def __init__(self, canvas, anchors_obj):
        self.canvas = canvas
        self.state = self.StateNone
        self.objs = []
        self.anchor_objs = anchors_obj
        
        self.initial_pos = None
        self.initial_angle_ref = None
        
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
        
    def SetCursorPos(self, x, y):
        if self.state==self.StateMoving:
            for obj in self.objs:
                obj.Move(Point(obj.origin_pos.x+self.canvas.px2mm(x-self.initial_pos.x), obj.origin_pos.y+self.canvas.px2mm(y-self.initial_pos.y)))
        elif self.state==self.StatePlacing:                    
            self.objs[0].Move(Point(self.canvas.xpx2mm(x), self.canvas.ypx2mm(y)))
        elif self.state==self.StateRotating:
            angle = self.initial_pos.GetAngle(self.initial_angle_ref, Point(x, y))
            for obj in self.objs:
                obj.Rotate(Point(self.canvas.xpx2mm(self.initial_pos.x), self.canvas.ypx2mm(self.initial_pos.y)), angle)

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

    def GetMovingObjects(self):
        res = []
        if self.state==self.StateMoving or self.state==self.StatePlacing or self.state==self.StateRotating:
            res = self.objs
        return res
    
    def GetObjects(self):
        return self.objs
    
class DrawFootprintFrame(DialogDrawFootprint): 
    def __init__(self, parent):
        super(DrawFootprintFrame, self).__init__(parent)
        
        self.zoom = 1
        self.canvas = FootprintCanvas()
        self.selection = []
        self.magnet = 10
        
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
        self.last_pad = None
        
        self.Bind(wx.EVT_CHAR_HOOK, self.keyPressed)
        
        ######
        node = ObjectGrid(Position(0, 0), Position(20, 20), Position(10, 10))
        self.build_objects.AddNode(node)
        self.tree_objects_manager.AppendObject('Drawing', node)
        
        node = ObjectPoint(Position(0, 0))
        self.build_objects.AddNode(node)
        self.tree_objects_manager.AppendObject('Drawing', node)
    
        ###
        p0 = Point(10, 10)
        p1 = Point(5, 5)
        p2 = p1.Rotate(p0, math.pi/2.)
        p3 = p1.Rotate(p0, 3*math.pi/2)
        print "**", p2.x, p2.y
        print "**", p3.x, p3.y
        print "***", p0.GetAngle(p1, p2)*180./math.pi
        print "***", p0.GetAngle(p1, p3)*180./math.pi

    def Render(self):
        self.canvas.Viewport(self.image_draw.GetRect().width, self.image_draw.GetRect().height)
        self.canvas.Origin(self.image_draw.GetRect().width/2, self.image_draw.GetRect().height/2)
        
        self.canvas.Clear(["editor"])
        img = self.canvas.Render(self.all_objects)
        self.image_draw.SetBitmap(wx.lib.wxcairo.BitmapFromImageSurface(img))

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
            
    def keyPressed( self, event):
        print "keyPressed", type(event), event.GetKeyCode(), event.GetRawKeyFlags(), event.ControlDown()

        if event.GetKeyCode()==27:
            # cancel any operation
            self.SelectObjects([])
        
        event.Skip(True)
        
    def onImageDrawLeftDClick( self, event ):
        event.Skip()
    
    def onImageDrawLeftDown( self, event ):
        pos = event.GetPosition()

        [distance, anchor] = self.anchor_objects.FindAnchor(pos, self.canvas, self.state.GetMovingObjects())
        if anchor:
            self.cursor.pos = anchor.Pos(Point(self.canvas.xpx2mm(pos.x), self.canvas.ypx2mm(pos.y)))
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
            self.cursor.pos = anchor.Pos(Point(self.canvas.xpx2mm(pos.x), self.canvas.ypx2mm(pos.y)))
            pos = Point(self.canvas.xmm2px(self.cursor.pos.x), self.canvas.ymm2px(self.cursor.pos.y))
        else:
            self.cursor.pos = Position(self.canvas.xpx2mm(pos.x), self.canvas.ypx2mm(pos.y))
        self.cursor.Update()

        self.state.SetCursorPos(pos.x, pos.y)
        self.Render()
        
        status = self.GetStatusBar()
        status.SetStatusText("x: "+str(self.cursor.pos.x)+"mm, y: "+str(self.cursor.pos.y)+"mm", 0)
        status.SetStatusText("x: "+str(pos.x)+"px, y: "+str(pos.y)+"px", 1)
        status.SetStatusText("zoom: "+str(self.zoom), 2)

    def onImageDrawMouseWheel( self, event ):
        event.Skip()
    
    def onImageDrawRightDClick( self, event ):
        event.Skip()
    
    def onImageDrawRightDown( self, event ):
        event.Skip()
    
    def onImageDrawRightUp( self, event ):
        event.Skip()
    
    def onMenuDrawPadSelection( self, event ):
        node = ObjectPad()
            
        self.build_objects.AddNode(node)
        obj = self.tree_objects_manager.AppendObject('Drawing', node)
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
        event.Skip()
    
    def onMenuToolVerticalSelection( self, event ):
        node = ObjectVerticalLine()
            
        self.build_objects.AddNode(node)
        obj = self.tree_objects_manager.AppendObject('Drawing', node)
        self.tree_objects_manager.Select(obj)
        self.state.DoPlace(node)

        if self.current_panel:
            self.current_panel.Destroy()
        self.current_panel = EditLineFrame(self.panel_edit_object, self.Render, node)
    
    def onMenuToolHorizontalSelection( self, event ):
        node = ObjectHorizontalLine()
            
        self.build_objects.AddNode(node)
        obj = self.tree_objects_manager.AppendObject('Drawing', node)
        self.tree_objects_manager.Select(obj)
        self.state.DoPlace(node)

        if self.current_panel:
            self.current_panel.Destroy()
        self.current_panel = EditLineFrame(self.panel_edit_object, self.Render, node)
    
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
        