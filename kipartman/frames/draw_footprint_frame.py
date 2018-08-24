from dialogs.dialog_draw_footprint import DialogDrawFootprint
from frames.frame_draw_footprint.edit_grid_frame import EditGridFrame
from frames.frame_draw_footprint.edit_dimension_frame import EditDimensionFrame
from frames.frame_draw_footprint.edit_line_frame import EditLineFrame
from frames.frame_draw_footprint.edit_angle_frame import EditAngleFrame
from frames.frame_draw_footprint.edit_pad_frame import EditPadFrame
from kicad.Canvas import *
import wx.lib.wxcairo
import helper.tree
from operator import pos
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
        objobj = DataModelObject(obj.Description(), obj)
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
        
    def Distance(self, pos):
        return self.pos.Distance(pos)
    
    def Pos(self, point=None):
        return self.pos
    
class AnchorLine(object):
    def __init__(self, parent, line):
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
        
    def Distance(self, pos):
        r = Rect()
        c = 1
        if self.line.start.x<self.line.end.x:
            r.start.x = self.line.start.x-c
            r.end.x = self.line.end.x+c
        else:
            r.start.x = self.line.end.x-c
            r.end.x = self.line.start.x+c
             
        if self.line.start.y<self.line.end.y:
            r.start.y = self.line.start.y-c
            r.end.y = self.line.end.y+c
        else:
            r.start.y = self.line.end.y-c
            r.end.y = self.line.start.y+c
#             
#         if pos.x>=r.start.x and pos.x<=r.end.x and pos.y>=r.start.y and pos.y<=r.end.y:
#             p = self.line.get_projection(pos)
#             return p.Distance(pos)
        p = self.line.get_projection(pos)
        if p.x>=r.start.x and p.x<=r.end.x and p.y>=r.start.y and p.y<=r.end.y:
            return p.Distance(pos)
        return None

# class AnchorArc(object):
#     def __init__(self, parent, line):
#         self.line = line
#         
#     def Distance(self, pos):
#         p = self.line.get_projection(pos)
#         return p.Distance(pos)
# 
#     # return projection of point on line
#     def Pos(self, point=None):
#         return self.line.get_projection(point)

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
                if min_distance and distance<min_distance:
                    min_distance = distance
                    min_anchor = anchor
                elif not min_distance:
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

    def Description(self):
        return format(type(self))
    
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

    def Description(self):
        return "Origin x={} y={}".format(self.pos.x, self.pos.y)

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
        if "anchor" not in self.layers:
            self.layers.append("anchor")
    
    def UnSelect(self):
        if "anchor" in self.layers:
            self.layers.remove("anchor")

    def Description(self):
        return "Point x={} y={}".format(self.pos.x, self.pos.y)
        
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
        super(ObjectLine, self).__init__(["editor"], Point())
        
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
        if "selection" not in self.layers:
            self.layers.append("selection")
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
        super(ObjectPad, self).__init__(["F.Cu"], Point())
        self.type = 'smd' # smd or thru_hole
        self.shape = 'rect' # rect or oval
        self.size = Point()
        self.drill = 0.
        self.name = ''
        
        self.font = Font(Point(15, 15), 1)

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
        
        canvas.SetFont(self.font)
        
        if self.placed or ( self.placing_point is not None and self.placing_point==1):
            if self.shape=='rect':
                points = []
                for p in range(1, 5):
                    points.append(Point(canvas.xmm2px(self.points[p].pos.x), canvas.ymm2px(self.points[p].pos.y)))
                points.append(points[0])
                canvas.Draw(PolyLine(points, width=1, fill=True), ["F.Cu", "B.Cu"])
            
            canvas.Draw(Text(self.name, pos, anchor_x='center', anchor_y='center'), ["editor"])            

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
                obj.Move(Point(obj.origin_pos.x+(x-self.initial_pos.x), obj.origin_pos.y+(y-self.initial_pos.y)))
        elif self.state==self.StatePlacing:                    
            self.objs[0].Move(Point(x, y))
        elif self.state==self.StateRotating:
            angle = self.initial_pos.GetAngle(self.initial_angle_ref, Point(x, y))
            for obj in self.objs:
                obj.Rotate(self.initial_pos, angle)

    def DoClick(self, x, y):
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

        self.current_pad_name = None
        
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
        elif len(objs)==1 and isinstance(objs[0], ObjectAngle):
            self.current_panel = EditAngleFrame(self.panel_edit_object, self.Render, objs[0])
            
    def keyPressed( self, event):
        print "keyPressed", type(event), event.GetKeyCode(), event.GetRawKeyFlags(), event.ControlDown()

        if event.GetKeyCode()==27:
            # cancel any operation
            self.SelectObjects([])
        
        event.Skip(True)

    def onImageDrawLeftDClick( self, event ):
        event.Skip()
    
    def onImageDrawLeftDown( self, event ):
        pass
    
    def onImageDrawLeftUp( self, event ):
        pospx = event.GetPosition()
        pos = Point(self.canvas.xpx2mm(pospx.x), self.canvas.ypx2mm(pospx.y))
        
        self.cursor.pos = pos
        types = [Anchor, AnchorLine]
        for t in types:
            [distance, anchor] = self.anchor_objects.FindAnchor(t, pos, self.state.GetMovingObjects())
            if not distance is None and self.canvas.mm2px(distance)<self.magnet:
                pos = anchor.Pos(pos)
                pospx = Point(self.canvas.xpx2mm(pos.x), self.canvas.ypx2mm(pos.y))
                self.cursor.pos = pos
                break
        self.cursor.Update()
        
        self.state.DoClick(pos.x, pos.y)
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
        types = [Anchor, AnchorLine]
        for t in types:
            [distance, anchor] = self.anchor_objects.FindAnchor(t, pos, self.state.GetMovingObjects())
            if not distance is None and self.canvas.mm2px(distance)<self.magnet:
                pos = anchor.Pos(pos)
                pospx = Point(self.canvas.xpx2mm(pos.x), self.canvas.ypx2mm(pos.y))
                self.cursor.pos = pos
                break
        self.cursor.Update()

        self.state.SetCursorPos(pos.x, pos.y)
        self.Render()
        
        status = self.GetStatusBar()
        status.SetStatusText("x: "+str(self.cursor.pos.x)+"mm, y: "+str(self.cursor.pos.y)+"mm", 0)
        status.SetStatusText("x: "+str(pos.x)+"px, y: "+str(pos.y)+"px", 1)
        status.SetStatusText("zoom: "+str(self.zoom), 2)

        if self.current_panel:
            self.current_panel.Update()
        
    def onImageDrawMouseWheel( self, event ):
        print type(event)
    
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
    