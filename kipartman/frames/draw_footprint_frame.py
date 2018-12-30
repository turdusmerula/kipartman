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
import copy
from operator import itemgetter

from kicad.Canvas import *
import wx.lib.wxcairo
import helper.tree
from operator import pos
import numpy
from kicad import kicad_mod_file
from numpy.polynomial.polynomial import polyline

epsilon=1e-9

# class DataModelCategoryObject(helper.tree.TreeContainerItem):
#     def __init__(self, name):
#         super(DataModelCategoryObject, self).__init__()
#         self.name = name
#         
#     def GetValue(self, col):
#         vMap = { 
#             0 : self.name,
#         }
#         return vMap[col]
# 
#     def GetAttr(self, col, attr):
#         attr.Bold = True
#         return True
# 
# class DataModelObject(helper.tree.TreeItem):
#     def __init__(self, name, obj):
#         super(DataModelObject, self).__init__()
#         self.name = name
#         self.obj = obj
#         
#     def GetValue(self, col):
#         vMap = { 
#             0 : self.name,
#         }
#         return vMap[col]
# 
# class TreeManagerObjects(helper.tree.TreeManager):
#     def __init__(self, tree_view, *args, **kwargs):
#         super(TreeManagerObjects, self).__init__(tree_view)
#         
#     def FindCategory(self, name):
#         for data in self.data:
#             if isinstance(data, DataModelCategoryObject) and data.name==name:
#                 return data
#         return None
#                 
#     def FindObject(self, obj):
#         for data in self.data:
#             if isinstance(data, DataModelObject) and data.obj==obj:
#                 return data
#         return None
# 
#     def AppendCategory(self, name):
#         categoryobj = self.FindCategory(name)
#         if categoryobj:
#             return categoryobj
#         categoryobj = DataModelCategoryObject(name)
#         self.AppendItem(None, categoryobj)
#         return categoryobj
#     
#     def AppendObject(self, catgory_name, obj):
#         categoryobj = self.AppendCategory(catgory_name)
#         objobj = DataModelObject(obj.Description(), obj)
#         self.AppendItem(categoryobj, objobj)
#         self.Expand(categoryobj)
#         return objobj
# 
#     def DeleteObject(self, obj):
#         objobj = self.FindObject(obj)
#         if objobj is None:
#             return None
#         self.DeleteItem(objobj.parent, objobj)
        


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
    
    def Intersections(self, anchor):
        return []
    
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

    def Intersections(self, anchor):
        if issubclass(type(anchor), AnchorLine):
            intersection = self.line.get_intersection(anchor.line)
            if intersection:
                return [intersection]
        elif issubclass(type(anchor), AnchorSegment):
            intersection = self.line.get_intersection(anchor.line)
            if intersection and anchor.IsIn(intersection):
                return [intersection]
        return []

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
    
    def Copy(self, obj):
        super(EditorObject, self).Copy(obj)
        
        obj.pos = copy.copy(self.pos)
        obj.origin_pos = copy.copy(self.origin_pos)
        obj.radius = self.radius
        
        obj.angle = self.angle
        obj.origin_angle = self.origin_angle
        
        obj.placed = self.placed

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
    def FindAnchor(self, pos, radius, exclude_anchors=[]):
        anchors = []
        self.r_find_anchors(self, pos, radius, anchors)
    
        for anchor in exclude_anchors:
            if anchor in anchors:
                anchors.remove(anchor)
                 
        anchors.sort(key=itemgetter(0))
        if len(anchors)==0:
            return [None, None]
        
        # check points
        for anchor in anchors:
            if isinstance(anchor[1], Anchor):
                return anchor
        
        # check intersections
        anchor_lines = []
        for anchor in anchors:
            if issubclass(type(anchor[1]), AnchorLine):
                anchor_lines.append(anchor[1])
        min_distance = radius
        min_anchor = None
        while(len(anchor_lines)>0):
            for anchor in anchor_lines:
                if anchor!=anchor_lines[0]:
                    intersections = anchor.Intersections(anchor_lines[0])
                    if len(intersections)>0:
                        distance = intersections[0].Distance(pos)
                        if distance<min_distance:
                            min_distance = distance
                            min_anchor = Anchor(None, intersections[0])  
            anchor_lines.remove(anchor_lines[0])
        if min_anchor:
            return [min_distance, min_anchor]

        return anchors[0]
    
    def r_find_anchors(self, obj, pos, radius, anchors=[]):
        for anchor in obj.anchors:
            distance = anchor.Distance(pos)
            if distance is not None and distance<=radius:
                anchors.append([distance, anchor])

        for node in obj.nodes:
            self.r_find_anchors(node, pos, radius, anchors)
                
        return
    
#     # find closest anchor to position
#     def FindAnchors(self, pos, exclude_objects=[]):
#         anchors = self.r_find_anchors(self, pos, exclude_objects, anchors=[])
#         return sorted(anchors, key=lambda distance: distance[0])
#     
#     def r_find_anchors(self, obj, pos, exclude_objects=[], anchors=[]):
#         if obj in exclude_objects:
#             return anchors
#         
#         for anchor in obj.anchors:
#             distance = anchor.Distance(pos)
#             if distance<=self.radius:
#                 anchors.append([distance, anchors])
# 
#         for node in obj.nodes:
#             self.r_find_anchors(node, pos, exclude_objects, anchors)
#                 
#         return anchors

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
        self.placed = True
        self.Update()
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

#    def Render(self, canvas):
#        pass
    
    def Description(self):
        return format(type(self))
    
    def ContainsPos(self, pos, margin):
        for anchor in self.anchors:
            distance = anchor.Distance(pos)
            if distance is not None and distance<margin:
                return True
        return False
    
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
        if self.placed:
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
        
        self.points = []
        self.length = 5 # px
        self.width = 1 # px

        self.Update()
    
    def Update(self):
        self.Clear()
        self.points = []
        x = self.pos.x
        for px in range(0, self.count.x):
            y = self.pos.y
            for py in range(0, self.count.y):
                point = Point(x, y).Rotate(self.pos, self.angle)
                self.points.append(point)
                if self.placed:
                    self.AddAnchor(point)
                y = y+self.spacing.y
            x = x+self.spacing.x
         
    def Render(self, canvas):
        super(ObjectGrid, self).Render(canvas)
        
        lines = []
        
        for point in self.points:
            posx = canvas.xmm2px(point.x)
            posy = canvas.ymm2px(point.y)
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
        if self.placed:
            self.AddAnchor(self.pos)
        
    def Render(self, canvas):
        super(ObjectPoint, self).Render(canvas)

        pos = Point(canvas.xmm2px(self.pos.x), canvas.ymm2px(self.pos.y))        
            
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
        self.offset_points = [Point(), Point()]
        
        self.Update()

    def Update(self):
        self.Clear()

        p0 = self.points[0].pos
        p1 = self.points[1].pos
        p2 = self.pos
        
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
        self.offset_points[0] = p3
        self.offset_points[1] = p4
        
        if self.placed:
            self.AddAnchor(Point((p0.x+p1.x)/2., (p0.y+p1.y)/2.))
            self.AddAnchor(Point((p3.x+p4.x)/2., (p3.y+p4.y)/2.))
            self.AddAnchor(p3)
            self.AddAnchor(p4)
            self.AddAnchorSegment(Line(p0, p3))
            self.AddAnchorSegment(Line(p1, p4))
            self.AddAnchorSegment(Line(p3, p4))
    
    def get_projection(self, p0, a, b):
        p1 = Point()
        a1 = -1/a
        b1 = p0.y-a1*p0.x
        
        p1.x = (b-b1)/(a1-a)
        p1.y = (b*a1-a*b1)/(a1-a)
                
        return p1
    
    def Render(self, canvas):
        super(ObjectDimension, self).Render(canvas)

        p0 = Point(canvas.xmm2px(self.points[0].pos.x), canvas.ymm2px(self.points[0].pos.y))
        p1 = Point(canvas.xmm2px(self.points[1].pos.x), canvas.ymm2px(self.points[1].pos.y))
        p2 = Point(canvas.xmm2px(self.pos.x), canvas.ymm2px(self.pos.y))
        p3 = Point(canvas.xmm2px(self.offset_points[0].x), canvas.ymm2px(self.offset_points[0].y))
        p4 = Point(canvas.xmm2px(self.offset_points[1].x), canvas.ymm2px(self.offset_points[1].y))
#         
#         p0p1 = Line(p0, p1)
#         pc = p0p1.get_center()
#         
#         if math.fabs(p1.x-p0.x)<epsilon:
#             p3 = Point(p2.x, p0.y)
#             p4 = Point(p2.x, p1.y)
#         else:
#             [p0p1a, p0p1b] = p0p1.get_ab()
#             # parralel to p0p1 passing by p2
#             p2b = Line.get_b(p0p1a, p2)
#             
#             if math.fabs(p0p1a)<epsilon:
#                 # projection of p0 and p1 on parallel
#                 p3 = Point(p0.x, p2b)
#                 p4 = Point(p1.x, p2b)
#             else:
#                 # projection of p0 and p1 on parallel
#                 p3 = self.get_projection(p0, p0p1a, p2b)
#                 p4 = self.get_projection(p1, p0p1a, p2b)
                
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
            
            pm = Point((p0.x+p1.x)/2., (p0.y+p1.y)/2.)
            pml = 5
            canvas.Draw(Line(Point(pm.x-pml, pm.y), Point(pm.x+pml, pm.y), 1), self.layers)
            canvas.Draw(Line(Point(pm.x, pm.y-pml), Point(pm.x, pm.y+pml), 1), self.layers)

            pm = Point((p3.x+p4.x)/2., (p3.y+p4.y)/2.)
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
            for point in self.points:
                point.placed = True
                point.Update()
            self.Update()
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
        if self.placed:
            self.AddAnchorLine(StraightLine(self.points[0].pos, self.points[1].pos))
    
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
            self.Update()
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
                ps = Point(p0.x+d*math.cos(angle_start), p0.y+d*math.sin(angle_start))
                self.AddAnchorSegment(Line(p0, ps))
                self.AddAnchor(ps)
                pe = Point(p0.x+d*math.cos(angle_end), p0.y+d*math.sin(angle_end))
                self.AddAnchor(pe)
                self.AddAnchorSegment(Line(p0, pe))
            else:
                self.AddAnchorSegment(Line(p0, p1))
                self.AddAnchor(p1)
                self.AddAnchorSegment(Line(p0, p2))
                self.AddAnchor(p2)
                 
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
                point.placed = True
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
            self.Update()
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
        self.SetType(self.type)
        
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
            
        self.ClearNodes()
        for point in self.points:
            self.AddNode(point)  
            if self.placed:
                point.placed = True      
        self.Update()
    
    def Copy(self, pad):
        super(ObjectPad, self).Copy(pad)
        
        pad.type = self.type
        pad.shape = self.shape
        pad.size = copy.copy(self.size)
        pad.offset = copy.copy(self.offset)
        pad.drill = copy.copy(self.drill)
        pad.drill_type = self.drill_type
        pad.die_length = self.die_length
        pad.name = self.name
         
        pad.solder_mask_margin = self.solder_mask_margin
        pad.solder_paste_margin = self.solder_paste_margin
        pad.clearance = self.clearance
        pad.solder_paste_margin_ratio = self.solder_paste_margin_ratio
         
        pad.thermal_width = self.thermal_width
        pad.thermal_gap = self.thermal_gap
        pad.zone_connect = self.zone_connect
         
        pad.trapezoidal_delta = self.trapezoidal_delta
        pad.trapezoidal_direction = self.trapezoidal_direction
         
        pad.font = copy.copy(self.font)
 
        pad.SetShape(self.shape)
        pad.SetType(self.type)

    def SetSize(self, size):
        self.size = size
            
        self.Update()
        
    def Update(self):
        self.Clear()
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
                p.Rotate(self.pos, self.angle)
        
        if self.placed:
            if self.type=='thru_hole' or self.type=='np_thru_hole':
                if self.drill_type=='circle':
                    self.AddAnchorCircle(self.pos, Point(self.pos.x+self.drill.x, self.pos.y))
                else:
                    pass
            if self.shape=='rect' or self.shape=='trapezoid' or self.shape=='oval':        
                self.AddAnchorSegment(Line(self.points[1].pos, self.points[2].pos))
                self.AddAnchorSegment(Line(self.points[2].pos, self.points[3].pos))
                self.AddAnchorSegment(Line(self.points[3].pos, self.points[4].pos))
                self.AddAnchorSegment(Line(self.points[4].pos, self.points[1].pos))
                if self.shape=='oval':
                    pass
            elif self.shape=='circle':
                self.AddAnchorCircle(self.pos, Point(self.pos.x+dx, self.pos.y))

    def Render(self, canvas):
        super(ObjectPad, self).Render(canvas)
        
        offset = Point(canvas.mm2px(self.offset.x), canvas.mm2px(self.offset.y)) #.Rotate(Point(0, 0), self.angle)
        pos = Position(canvas.xmm2px(self.pos.x), canvas.ymm2px(self.pos.y), self.angle)
        size = Point(canvas.mm2px(self.size.x), canvas.mm2px(self.size.y))
        drill = Point(canvas.mm2px(self.drill.x), canvas.mm2px(self.drill.y))
        
        #angle = -self.angle
        angle = self.angle
        
        if self.placed or ( self.placing_point is not None and self.placing_point==1):
            if self.shape=='rect' or self.shape=='trapezoid' or self.shape=='oval':
                dx = size.x/2.
                dy = size.y/2.
                    
                tx = 0.
                ty = 0.
                if self.shape=='trapezoid' and self.trapezoidal_direction=='horz':
                    ty = canvas.mm2px(self.trapezoidal_delta/2.)
                if ty>dy:
                    ty = dy
                elif self.shape=='trapezoid' and self.trapezoidal_direction=='vert':
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
            self.Update()
            for point in self.points:
                point.placed = True
                point.Update()
            self.Select()
        
        return self.placed

    def Description(self):
        return "Pad {} {} {} x={} y={} width={} height={} angle={}".format(self.type, self.shape, self.name, self.pos.x, self.pos.y, self.size.x, self.size.y, self.angle)

    def dotcross(self, p0, p1, p2, p3):
        v0 = Point(p1.x-p0.x, p1.y-p0.y)
        v1 = Point(p3.x-p2.x, p3.y-p2.y)
        return v0.x*v1.y-v0.y*v1.x
    
    def ContainsPos(self, pos, margin):
        print("****")
        for anchor in self.anchors:
            distance = anchor.Distance(pos)
            if distance is not None and distance<margin:
                return True

        dx = self.size.x/2.
        dy = self.size.y/2.
        points = []
        points.append(Point(self.pos.x-dx, self.pos.y-dy))
        points.append(Point(self.pos.x+dx, self.pos.y-dy))
        points.append(Point(self.pos.x+dx, self.pos.y+dy))
        points.append(Point(self.pos.x-dx, self.pos.y+dy))
        
        for p in points:
            pr = p.Rotate(pos, self.angle)
            p.x = pr.x
            p.y = pr.y

#        print "****", self.dotcross(points[0], points[1], points[0], pos), self.dotcross(points[1], points[2], points[1], pos), self.dotcross(points[2], points[3], points[2], pos), self.dotcross(points[3], points[0], points[3], pos)

        if self.dotcross(points[0], points[1], points[0], pos)>0 and \
            self.dotcross(points[1], points[2], points[1], pos)>0 and \
            self.dotcross(points[2], points[3], points[2], pos)>0 and \
            self.dotcross(points[3], points[0], points[3], pos)>0:
            return True
#         print "****", pos.x, pos.y, points[0].GetAngle(points[1], pos)*180./math.pi, points[1].GetAngle(points[2], pos)*180./math.pi, points[2].GetAngle(points[3], pos)*180./math.pi, points[3].GetAngle(points[0], pos)*180./math.pi
#         if points[0].GetAngle(points[1], pos)>math.pi:
#             return False
#         if points[1].GetAngle(points[2], pos)>math.pi:
#             return False
#         if points[2].GetAngle(points[3], pos)>math.pi:
#             return False
#         if points[3].GetAngle(points[0], pos)>math.pi:
#             return False
    
        return False

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
            if self.placed==True or p1!=self.points[len(self.points)-1]:
                if p0:
                    self.AddAnchorSegment(Line(p0.pos, p1.pos))
                self.AddAnchor(p1.pos)
            p0 = p1
    
    def Render(self, canvas):
        super(ObjectPolyline, self).Render(canvas)

        if self.placed or len(self.points)>0:
            points = []
            for p in self.points:
                points.append(Point(canvas.xmm2px(p.pos.x), canvas.ymm2px(p.pos.y)))
            canvas.Draw(PolyLine(points, canvas.mm2px(self.width), fill=False), self.layers)

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
        for point in self.points:
            point.placed = True
            point.Update()
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

class ObjectMultiline(EditorObject):
    def __init__(self, layers=[]):
        super(ObjectMultiline, self).__init__(layers, Point())
        
        self.width = 1 # mm

        self.points = []
        
        self.Update()

    def Update(self):
        self.Clear()
        
        p0 = None
        for p1 in self.points:
            if p1!=self.points[len(self.points)-1]:
                if p0:
                    self.AddAnchorSegment(Line(p0.pos, p1.pos))
                self.AddAnchor(p1.pos)
            p0 = p1
    
    def Render(self, canvas):
        super(ObjectMultiline, self).Render(canvas)

        if self.placed or len(self.points)>0:
            lines = []
            pp = None
            for pmm in self.points:
                p = Point(canvas.xmm2px(pmm.pos.x), canvas.ymm2px(pmm.pos.y))
                if pp is not None:
                    lines.append(Line(pp, p))
                    pp = None
                else:
                    pp = p
                 
            canvas.Draw(MultiLine(lines, canvas.mm2px(self.width)), self.layers)
                
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
        for point in self.points:
            point.placed = True
            point.Update()
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
        return "Multiline width={} ".format(self.width)+coords

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
        if self.placed:
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
            self.Update()
            for point in self.points:
                point.placed = True
                point.Update()
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
            self.Update()
            for point in self.points:
                point.placed = True
                point.Update()
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

class ObjectPadRow(EditorObject):
    def __init__(self, editor, model_pad):
        super(ObjectPadRow, self).__init__([], Point())
        
        self.editor = editor
        
        self.placing_point = None
        
        self.model_pad = model_pad
        self.pads = []

        self.increment = 0.
        
        self.Update()

    def Update(self):
        self.Clear()
                            
    def Render(self, canvas):
        super(ObjectPadRow, self).Render(canvas)
        self.model_pad.Render(canvas)
        for pad in self.pads:
            pad.Render(canvas)
            
    def StartPlace(self):
        if self.model_pad.placed==False:
            self.model_pad.StartPlace()
            self.model_pad.Select()
        self.placing_point = 0
        
    # return True if placement is complete
    def Place(self, pos):
        if self.model_pad.placed==False:
            self.model_pad.Place(pos)
            self.model_pad.Update()
        else:
            self.placing_point = self.placing_point+1
            if self.placing_point==1:
                self.increment = self.model_pad.pos.Distance(pos)
            elif self.placing_point==2:
                self.PlacePads()
                self.placing_point = None
                self.placed = True
                return True
        return False

    def Move(self, pos):
        if self.model_pad.placed==False:
            self.model_pad.Move(pos)
            self.model_pad.Update()
        else:
            if self.placing_point==0:
                pref = Point(self.model_pad.pos.x+1, self.model_pad.pos.y)
                self.angle = self.model_pad.pos.GetAngle(pref, pos)
                self.model_pad.angle = self.angle
                self.model_pad.Update()

                self.pads = []
                pad = ObjectPad() 
                self.model_pad.Copy(pad)
                pad.angle = self.angle
                increment = self.model_pad.pos.Distance(pos)
                pad.pos = Point(self.model_pad.pos.x+increment*math.cos(self.angle), self.model_pad.pos.y+increment*math.sin(self.angle))
                pad.Update()
                pad.Select()
                self.pads.append(pad)
                self.NamePads()
            elif self.placing_point==1:
                distance = self.model_pad.pos.Distance(pos)
                pad_num = int(distance/self.increment)
                while len(self.pads)>pad_num:
                    self.pads.remove(self.pads[len(self.pads)-1])
                while pad_num>len(self.pads):
                    pad = ObjectPad() 
                    self.model_pad.Copy(pad)
                    pad.angle = self.angle
                    col = len(self.pads)-1
                    pad.pos = Point(self.model_pad.pos.x+(self.increment*(col+2))*math.cos(self.angle), 
                                    self.model_pad.pos.y+(self.increment*(col+2))*math.sin(self.angle))
                    pad.Select()
                    self.pads.append(pad)
                    self.NamePads()
                    
        self.Update()

    def NamePads(self):
        names = []
        for obj in self.editor.component_objects.nodes:
            if isinstance(obj, ObjectPad) and obj.name!='':
                try:
                    iname = int(obj.name)
                    names.append(iname)
                except:
                    pass

        for pad in self.pads:    
            names.sort()
            pname = 0
            for name in names:
                if name-pname>1:
                    break
                pname = name
            pad.name = str(pname+1)
            names.append(pname+1)

    def PlacePads(self):
        for pad in self.pads:
            self.editor.component_objects.AddNode(pad)
#             obj = self.editor.tree_objects_manager.AppendObject('Part', pad)
#             self.editor.tree_objects_manager.Select(obj)
            pad.Update()
            pad.UnSelect()
        self.model_pad.UnSelect()
        self.pads = []
        
class ObjectPadArray(ObjectPadRow):
    def __init__(self, editor, model_pad):
        super(ObjectPadArray, self).__init__(editor, model_pad)
        
        self.col_increment = 0.
        self.row_increment = 0.
        self.row_size = 0.
        
        self.Update()

    def Render(self, canvas):
        super(ObjectPadArray, self).Render(canvas)
        self.model_pad.Render(canvas)
        for pad in self.pads:
            pad.Render(canvas)
            
    # return True if placement is complete
    def Place(self, pos):
        if self.model_pad.placed==False:
            self.model_pad.Place(pos)
            self.model_pad.Update()
        else:
            self.placing_point = self.placing_point+1
            if self.placing_point==1:
                self.col_increment = self.model_pad.pos.Distance(pos)
            elif self.placing_point==2:
                self.row_size = len(self.pads)+1
            elif self.placing_point==3:
                axis = Line(self.model_pad.pos, Point(self.model_pad.pos.x, self.model_pad.pos.y+1).Rotate(self.model_pad.pos, self.angle))
                pp = axis.get_projection(pos)
                self.row_increment = self.model_pad.pos.Distance(pp)
            elif self.placing_point==4:
                self.PlacePads()
                self.placing_point = None
                self.placed = True
                return True
        return False

    def Move(self, pos):
        if self.model_pad.placed==False:
            self.model_pad.Move(pos)
            self.model_pad.Update()
        else:
            if self.placing_point==0:
                pref = Point(self.model_pad.pos.x+1, self.model_pad.pos.y)
                self.angle = self.model_pad.pos.GetAngle(pref, pos)
                self.model_pad.angle = self.angle
                self.model_pad.Update()

                self.pads = []
                pad = ObjectPad() 
                self.model_pad.Copy(pad)
                pad.angle = self.angle
                increment = self.model_pad.pos.Distance(pos)
                pad.pos = Point(self.model_pad.pos.x+increment*math.cos(self.angle), self.model_pad.pos.y+increment*math.sin(self.angle))
                pad.Select()
                self.pads.append(pad)
                self.NamePads()
            elif self.placing_point==1:
                distance = self.model_pad.pos.Distance(pos)
                pad_num = int(distance/self.col_increment)
                while pad_num<len(self.pads):
                    self.pads.remove(self.pads[len(self.pads)-1])
                while pad_num>len(self.pads):
                    pad = ObjectPad() 
                    self.model_pad.Copy(pad)
                    pad.angle = self.angle
                    i = len(self.pads)-1
                    pad.pos = Point(self.model_pad.pos.x+(self.col_increment*(i+2))*math.cos(self.angle), self.model_pad.pos.y+(self.col_increment*(i+2))*math.sin(self.angle))
                    pad.Select()
                    self.pads.append(pad)
                    self.NamePads()
            elif self.placing_point==2:
                axis = Line(self.model_pad.pos, Point(self.model_pad.pos.x, self.model_pad.pos.y+1).Rotate(self.model_pad.pos, self.angle))
                pp = axis.get_projection(pos)
                row_increment = self.model_pad.pos.Distance(pp)
                while len(self.pads)>self.row_size-1:
                    self.pads.remove(self.pads[len(self.pads)-1])                
                for col in range(0, self.row_size):
                    pad = ObjectPad() 
                    self.model_pad.Copy(pad)
                    pad.angle = self.angle
                    pad.pos = Point(self.model_pad.pos.x+row_increment*math.cos(self.angle+math.pi/2.)+(self.col_increment*col)*math.cos(self.angle), 
                                    self.model_pad.pos.y+row_increment*math.sin(self.angle+math.pi/2.)+(self.col_increment*col)*math.sin(self.angle))
                    pad.Select()
                    self.pads.append(pad)
                    self.NamePads()
            elif self.placing_point==3:
                axis = Line(self.model_pad.pos, Point(self.model_pad.pos.x, self.model_pad.pos.y+1).Rotate(self.model_pad.pos, self.angle))
                pp = axis.get_projection(pos)
                distance = self.model_pad.pos.Distance(pp)
                row_num = int(distance/self.row_increment)
                if row_num>0:
                    while len(self.pads)>row_num*self.row_size-1:
                        self.pads.remove(self.pads[len(self.pads)-1])
                    while len(self.pads)<row_num*self.row_size:
                        row = len(self.pads)/self.row_size+1
                        for col in range(0, self.row_size):
                            pad = ObjectPad() 
                            self.model_pad.Copy(pad)
                            pad.angle = self.angle
                            pad.pos = Point(self.model_pad.pos.x+(self.row_increment*row)*math.cos(self.angle+math.pi/2.)+(self.col_increment*col)*math.cos(self.angle), 
                                            self.model_pad.pos.y+(self.row_increment*row)*math.sin(self.angle+math.pi/2.)+(self.col_increment*col)*math.sin(self.angle))
                            pad.Select()
                            self.pads.append(pad)
                        self.NamePads()
                
        self.Update()

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
        else:
            return None
        return self.state
    
    def DoDClick(self, x, y, screenx, screeny):
        if self.state==self.StatePlacing:
            self.Validate()
            self.state = self.StateNone

    def GetMovingObjects(self):
        res = []
        if self.state==self.StateMoving or self.state==self.StateRotating:
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
        
        self.selectable_objects = EditorObject([])
        self.selectable_objects.AddNode(self.component_objects)
        self.selectable_objects.AddNode(self.build_objects)
        
        self.all_objects = EditorObject([])
        self.all_objects.AddNode(self.selectable_objects)
        
        self.state = EditorState(self.canvas, self.selectable_objects)
        
        self.current_panel = None
        
        # module elements
        self.footprint_name = ''
        self.footprint_timestamp = ''
        self.footprint_descr = ''
        self.footprint_tags = []
        
#         # create manufacturers list
#         self.tree_objects_manager = TreeManagerObjects(self.tree_objects, context_menu=self.menu_edit)
#         self.tree_objects_manager.AddTextColumn("name")
#         self.tree_objects_manager.OnSelectionChanged = self.onTreeMenuObjectsSelChanged
#         self.tree_objects_manager.AppendCategory('Drawing')
#         self.tree_objects_manager.AppendCategory('Part')
        
        # create layers list
        self.tree_layers_manager = TreeManagerLayers(self.tree_layers)
        self.tree_layers_manager.AddToggleColumn("visible")
        self.tree_layers_manager.AddToggleColumn("active")
        self.tree_layers_manager.AddTextColumn("name")
        #self.tree_layers_manager.OnSelectionChanged = self.onTreeMenuObjectsSelChanged

        # add origin 
        node = ObjectOrigin(Position(0, 0))
        node.placed = True
        self.all_objects.AddNode(node)

        # add cursor
        node = ObjectOrigin() 
        #ObjectGrid(Position(0, 0), Position(1, 1), Position(10, 10))
        self.cursor = node
        self.all_objects.AddNode(self.cursor)
        
        # add default text fields
        self.part_reference = ObjectTextReference("REF**", Font(Point(1, 1), 0.15))
        self.part_reference.placed = True
        self.component_objects.AddNode(self.part_reference)
#         self.tree_objects_manager.AppendObject('Part', self.part_reference)
        self.part_value = ObjectTextValue("<value>", Font(Point(1, 1), 0.15))
        self.part_value.placed = True
        self.component_objects.AddNode(self.part_value)
#         self.tree_objects_manager.AppendObject('Part', self.part_value)
#         self.part_user = ObjectTextUser("%R", Font(Point(1, 1), 0.15))
#         self.component_objects.AddNode(self.part_user)
#         self.tree_objects_manager.AppendObject('Part', self.part_user)

        # last used objects
        self.last_grid = None
        self.last_pad = None
        
        self.panel_draw.Bind(wx.EVT_CHAR_HOOK, self.keyPressed)

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
        mod.SaveFile(self.filename)
        
    def UpdateAll(self, obj):
        obj.Update()
        for node in obj.nodes:
            self.UpdateAll(node)
            
    def load_object(self, obj, stack=[], level=0, lines=None):
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
            current.placed = True
            current.name = obj.GetName()
            current.SetType(obj.GetType())
            current.SetShape(obj.GetShape())
            self.component_objects.AddNode(current)
#             self.tree_objects_manager.AppendObject('Part', current)
        elif isinstance(obj, kicad_mod_file.KicadFPText):
            if obj.GetKind()=='value':
                current = self.part_value
            elif obj.GetKind()=='reference':
                current = self.part_reference
            else:
                current = ObjectTextUser()
                self.component_objects.AddNode(current)
#                 self.tree_objects_manager.AppendObject('Part', current)
            current.value = obj.GetValue()
            current.placed = True
            stack.append(current)
            pop = True
        elif isinstance(obj, kicad_mod_file.KicadFPArc):
            current = ObjectArc()
            pop = True
            stack.append(current)
            current.placed = True
            self.component_objects.AddNode(current)
#             self.tree_objects_manager.AppendObject('Part', current)
        elif isinstance(obj, kicad_mod_file.KicadFPCircle):
            current = ObjectCircle()
            pop = True
            stack.append(current)
            current.placed = True
            self.component_objects.AddNode(current)
#             self.tree_objects_manager.AppendObject('Part', current)
        elif isinstance(obj, kicad_mod_file.KicadFPLine):
            current = ObjectPolyline()
            pop = True
            stack.append(current)
            current.placed = True
            self.component_objects.AddNode(current)
#             self.tree_objects_manager.AppendObject('Part', current)
        elif isinstance(obj, kicad_mod_file.KicadAt) and current:
            at = obj.GetAt()
            current.Move(at)
            if issubclass(type(current), ObjectText):
                if math.fabs(at.angle)>epsilon:
                    current.orientation = 'vertical'
            else:
                current.StartRotate()
                current.Rotate(current.pos, -at.angle*math.pi/180.)
                current.Validate()
#             self.tree_objects_manager.UpdateItem(self.tree_objects_manager.FindObject(current))
        elif isinstance(obj, kicad_mod_file.KicadSize) and current:
            size = obj.GetSize()
            current.size.x = size.x
            current.size.y = size.y
#             self.tree_objects_manager.UpdateItem(self.tree_objects_manager.FindObject(current))
        elif isinstance(obj, kicad_mod_file.KicadCenter) and current:
            centre = obj.GetCenter()
            current.points[0].pos.x = centre.x
            current.points[1].pos.y = centre.y
#             self.tree_objects_manager.UpdateItem(self.tree_objects_manager.FindObject(current))
        elif isinstance(obj, kicad_mod_file.KicadStart) and current:
            if isinstance(current, ObjectPad):
                current.Move(obj.GetStart())
            elif isinstance(current, ObjectPolyline):
                current.points.append(ObjectPoint(obj.GetStart()))
            elif isinstance(current, ObjectArc) or isinstance(current, ObjectCircle):
                current.points[0].pos = obj.GetStart()
#             self.tree_objects_manager.UpdateItem(self.tree_objects_manager.FindObject(current))
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
#             self.tree_objects_manager.UpdateItem(self.tree_objects_manager.FindObject(current))
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
#             self.tree_objects_manager.UpdateItem(self.tree_objects_manager.FindObject(current))
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
            current.layers = []
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
                current.trapezoidal_direction = 'horz'
            elif math.fabs(rect.y)>epsilon:
                current.trapezoidal_delta = rect.y
                current.trapezoidal_direction = 'vert'
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
    
#         # fusion lines to polylines
#         polylines = []
#         fusion = True
#         while fusion:
#             fusion = False
#             while len(lines)>0:
#                 line = lines[0]
#                 line_start = line.points[0]
#                 line_end = line.points[len(line.points)-1]
#                 for polyline in polylines:
#                     polyline_start = polyline.points[0]
#                     polyline_end = polyline.points[len(polyline.points)-1]
#                     
#                     if math.fabs(polyline.width-line.width)<=epsilon:
#                         if math.fabs(line_start.x-polyline_end.x)<=epsilon and math.fabs(line_start.y-polyline_end.y)<=epsilon:
#                             for p in line.points:
#                                 if p!=line_start:
#                                     polyline.points.append(p)
#                             lines.remove(line)
#                             line = None
#                             fusion = True
#                         if line and math.fabs(line_end.x-polyline_start.x)<=epsilon and math.fabs(line_end.y-polyline_start.y)<=epsilon:
#                             for p in reversed(line.points):
#                                 if p!=line_end:
#                                     polyline.points.insert(0, p)
#                             lines.remove(line)
#                             line = None
#                             fusion = True
#                 if line:
#                     lines.remove(line)
#                     polylines.append(line)
#             lines = polylines
#             polylines = []
#         for polyline in polylines:
#             self.component_objects.AddNode(polyline)
#             self.tree_objects_manager.AppendObject('Part', polyline)
            
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
            node.AddAttribute(str(-obj.angle*180./math.pi))
            pad.AddNode(node)
            node = kicad_mod_file.KicadSize()
            node.AddAttribute(str(obj.size.x))
            node.AddAttribute(str(obj.size.y))
            pad.AddNode(node)
            if math.fabs(obj.trapezoidal_delta)>epsilon:
                node = kicad_mod_file.KicadRectDelta()
                if obj.trapezoidal_direction=='horz':
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
            obj.UnSelect()
            pp = None
            for p in obj.points:
                if pp is not None:
                    line = kicad_mod_file.KicadFPLine()
                    parent.AddNode(line)
                    node = kicad_mod_file.KicadStart()
                    node.AddAttribute(pp.pos.x)
                    node.AddAttribute(pp.pos.y)
                    line.AddNode(node)
                    node = kicad_mod_file.KicadEnd()
                    node.AddAttribute(p.pos.x)
                    node.AddAttribute(p.pos.y)
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

    def GetCurrentPadName(self):
        names = []
        for obj in self.component_objects.nodes:
            if isinstance(obj, ObjectPad) and obj.name!='':
                try:
                    names.append(int(obj.name))
                except:
                    pass
        names.sort()

        if len(names)==0:
            return '1'
        
        pname = 0
        for name in names:
            if name-pname>1:
                return str(pname+1)
            pname = name
        return str(pname+1)
    
    def SelectObjects(self, objs):
        self.Cancel()
                
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
            print("**", objs[0].Description())
    
    def GetObjectsOnPos(self, obj, pos, objs=[]):
        
        if isinstance(obj, ObjectPoint)==False and obj.ContainsPos(pos, self.canvas.px2mm(self.magnet)):
            objs.append(obj)
            
        for node in obj.nodes:
            self.GetObjectsOnPos(node, pos, objs)
                
    def keyPressed( self, event):
        print("keyPressed", type(event), event.GetKeyCode(), event.GetRawKeyFlags(), event.ControlDown())

        if event.GetKeyCode()==27:
            # cancel any operation
            self.Cancel()
        
        event.Skip(True)

    def Cancel(self):
#         for obj in self.state.GetObjects():
#             if obj.Placed()==False:
#                 self.tree_objects_manager.DeleteObject(obj)
#                 if obj.Parent():
#                     obj.Parent().RemoveNode(obj)

        self.state.Cancel()
        self.Render()
        
    def onImageDrawLeftDClick( self, event ):
        self.image_draw.SetFocus()
        
        pospx = event.GetPosition()
        pos = Point(self.canvas.xpx2mm(pospx.x), self.canvas.ypx2mm(pospx.y))
        
        [distance, anchor] = self.all_objects.FindAnchor(pos, self.canvas.px2mm(self.magnet))
        if distance is not None:
            pos = anchor.Pos(pos)
            #pospx = Point(self.canvas.xpx2mm(pos.x), self.canvas.ypx2mm(pos.y))
        self.cursor.pos = pos
        self.cursor.Update()
        
        self.state.DoDClick(pos.x, pos.y, pospx.x, pospx.y)
        self.Render()
    
        if self.current_panel:
            self.current_panel.Update()
    
    def onImageDrawLeftDown( self, event ):
        self.image_draw.SetFocus()
        
        pospx = Point(event.GetPosition().x, event.GetPosition().y)
        pos = Point(self.canvas.xpx2mm(pospx.x), self.canvas.ypx2mm(pospx.y))
        self.left_down_pospx = pospx
                
        self.state.DoLeftDown(pos.x, pos.y, pospx.x, pospx.y)
        self.Render()
    
    def onImageDrawLeftUp( self, event ):
        self.image_draw.SetFocus()

        pospx = Point(event.GetPosition().x, event.GetPosition().y)
        pos = Point(self.canvas.xpx2mm(pospx.x), self.canvas.ypx2mm(pospx.y))
        
        [distance, anchor] = self.all_objects.FindAnchor(pos, self.canvas.px2mm(self.magnet))
        if distance is not None:
            pos = anchor.Pos(pos)
            #pospx = Point(self.canvas.xpx2mm(pos.x), self.canvas.ypx2mm(pos.y))
        self.cursor.pos = pos
        self.cursor.Update()
        
        self.state.DoLeftUp(pos.x, pos.y, pospx.x, pospx.y)
        
        if self.left_down_pospx.Distance(pospx)<=2:
            state = self.state.DoClick(pos.x, pos.y, pospx.x, pospx.y)
            if state is None:
                objs = []
                self.GetObjectsOnPos(self.selectable_objects, pos, objs)
                if len(objs)<=1:
                    self.SelectObjects(objs)
                elif len(objs)>1:
                    self.popupmenu = wx.Menu()
                    for obj in objs:
                        item = self.popupmenu.Append(-1, obj.Description())
                        item.obj = obj
                        #self.Bind(wx.EVT_MENU, self.onPopupItemSelected, item)
                        self.Bind(wx.EVT_MENU, lambda evt, obj=obj: self.onPopupItemSelected(evt, obj), item)
                    self.panel_draw.Bind(wx.EVT_CONTEXT_MENU, self.onShowPopup)
                    
                    self.image_draw.PopupMenu(self.popupmenu, event.GetPosition())
                
        self.Render()
    
        if self.current_panel:
            self.current_panel.Update()
    
    def onImageDrawMiddleDClick( self, event ):
        self.image_draw.SetFocus()
        event.Skip()
    
    def onImageDrawMiddleDown( self, event ):
        self.image_draw.SetFocus()
        event.Skip()
    
    def onImageDrawMiddleUp( self, event ):
        self.image_draw.SetFocus()
        event.Skip()

    def onImageDrawMotion( self, event ):
        pospx = event.GetPosition()
        pos = Point(self.canvas.xpx2mm(pospx.x), self.canvas.ypx2mm(pospx.y))

        exclude_anchors = []
#         if len(self.state.GetMovingObjects())>0:       
#             item = self.tree_objects.GetSelection()
#             obj = None
#             if item.IsOk():
#                 obj = self.tree_objects_manager.ItemToObject(item)
#             self.anchor_objects.r_find_anchors(obj.obj, pos, self.canvas.px2mm(self.magnet), exclude_anchors)
        
        [distance, anchor] = self.all_objects.FindAnchor(pos, self.canvas.px2mm(self.magnet), exclude_anchors)
        if distance is not None:
            pos = anchor.Pos(pos)
            #pospx = Point(self.canvas.xpx2mm(pos.x), self.canvas.ypx2mm(pos.y))
        self.cursor.pos = pos
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
    
    def onPopupItemSelected(self, event, obj=None):
        #item = self.popupmenu.FindItemById(event.GetId())
        #obj = item.obj
        if obj:
            self.SelectObjects([obj])

            print("select: ", obj.Description())
    
    def onShowPopup(self, event):
        pass
        
    def onMenuDrawPadSelection( self, event ):
        node = ObjectPad()
        node.name = self.GetCurrentPadName()
        
        self.component_objects.AddNode(node)
#         obj = self.tree_objects_manager.AppendObject('Part', node)
#         self.tree_objects_manager.Select(obj)
        self.state.DoPlace(node)

        if self.current_panel:
            self.current_panel.Destroy()
        self.current_panel = EditPadFrame(self.panel_edit_object, self.Render, node)

    def onMenuToolDimensionSelection( self, event ):
        node = ObjectDimension()
            
        self.build_objects.AddNode(node)
#         obj = self.tree_objects_manager.AppendObject('Drawing', node)
#         self.tree_objects_manager.Select(obj)
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
#         obj = self.tree_objects_manager.AppendObject('Drawing', node)
#         self.tree_objects_manager.Select(obj)
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
#         obj = self.tree_objects_manager.AppendObject('Drawing', node)
#         self.tree_objects_manager.Select(obj)
        self.state.DoPlace(node)

        if self.current_panel:
            self.current_panel.Destroy()
        self.current_panel = EditAngleFrame(self.panel_edit_object, self.Render, node)
    
    def onMenuToolVerticalSelection( self, event ):
        node = ObjectVerticalLine()
            
        self.build_objects.AddNode(node)
#         obj = self.tree_objects_manager.AppendObject('Drawing', node)
#         self.tree_objects_manager.Select(obj)
        self.state.DoPlace(node)

        if self.current_panel:
            self.current_panel.Destroy()
        #self.current_panel = EditLineFrame(self.panel_edit_object, self.Render, node)
    
    def onMenuToolHorizontalSelection( self, event ):
        node = ObjectHorizontalLine()
            
        self.build_objects.AddNode(node)
#         obj = self.tree_objects_manager.AppendObject('Drawing', node)
#         self.tree_objects_manager.Select(obj)
        self.state.DoPlace(node)

        if self.current_panel:
            self.current_panel.Destroy()
        #self.current_panel = EditLineFrame(self.panel_edit_object, self.Render, node)
    
    def onMenuToolLineSelection( self, event ):
        node = ObjectLine()
            
        self.build_objects.AddNode(node)
#         obj = self.tree_objects_manager.AppendObject('Drawing', node)
#         self.tree_objects_manager.Select(obj)
        self.state.DoPlace(node)

        if self.current_panel:
            self.current_panel.Destroy()
        self.current_panel = EditLineFrame(self.panel_edit_object, self.Render, node)
    
    def onMenuZoomResetSelection( self, event ):
        self.canvas.Zoom(1)
        status = self.GetStatusBar()
        status.SetStatusText("zoom: "+str(self.zoom), 2)

    def onMenuEditMoveSelection( self, event ):
        self.state.DoMove()
    
    def onMenuEditRemoveSelection( self, event ):
        for obj in self.selection:
            if obj.parent:
                obj.parent.RemoveNode(obj)
        self.selection = []
        self.Render()
            
    def onMenuEditRotateSelection( self, event ):
        self.state.DoRotate()

#     def onTreeMenuObjectsSelChanged( self, event ):
#         item = self.tree_objects.GetSelection()
#         if item.IsOk()==False:
#             return
#         obj = self.tree_objects_manager.ItemToObject(item)
#         if isinstance(obj, DataModelObject):
#             self.SelectObjects([obj.obj])
#         self.Render()
    
    def onMenuZoomInSelection( self, event ):
        self.canvas.Zoom(self.canvas.zoom*2.)
        status = self.GetStatusBar()
        status.SetStatusText("zoom: "+str(self.zoom), 2)
        self.Render()
    
    def onMenuZoomOutSelection( self, event ):
        self.canvas.Zoom(self.canvas.zoom/2.)
        status = self.GetStatusBar()
        status.SetStatusText("zoom: "+str(self.zoom), 2)
        self.Render()
    
    def onImageDrawMouseEvents( self, event ):
        event.Skip()
            
    def onMenuDrawPadRowSelection( self, event ):
#         item = self.tree_objects.GetSelection()
#         obj = None
#         if item.IsOk():
#             obj = self.tree_objects_manager.ItemToObject(item)
#         
#         if obj and isinstance(obj.obj, ObjectPad):
#             pad = obj.obj
#             self.tree_objects_manager.Select(pad)
#         else:
        pad = ObjectPad()
        pad.name = self.GetCurrentPadName()

        self.component_objects.AddNode(pad)
#        obj = self.tree_objects_manager.AppendObject('Part', pad)
#        self.tree_objects_manager.Select(obj)
        
        row = ObjectPadRow(self, pad)        
        self.build_objects.AddNode(row)
        self.state.DoPlace(row)

        if self.current_panel:
            self.current_panel.Destroy()
        self.current_panel = EditPadFrame(self.panel_edit_object, self.Render, pad)
            
    
    def onMenuDrawPadArraySelection( self, event ):
#         item = self.tree_objects.GetSelection()
#         obj = None
#         if item.IsOk():
#             obj = self.tree_objects_manager.ItemToObject(item)
#         
#         if obj and isinstance(obj.obj, ObjectPad):
#             pad = obj.obj
#             self.tree_objects_manager.Select(pad)
#         else:
        pad = ObjectPad()
        pad.name = self.GetCurrentPadName()

        self.component_objects.AddNode(pad)
#        obj = self.tree_objects_manager.AppendObject('Part', pad)
#        self.tree_objects_manager.Select(obj)
        
        row = ObjectPadArray(self, pad)        
        self.build_objects.AddNode(row)
        self.state.DoPlace(row)

        if self.current_panel:
            self.current_panel.Destroy()
        self.current_panel = EditPadFrame(self.panel_edit_object, self.Render, pad)
    
    def onMenuDrawPolylineSelection( self, event ):
        item = self.tree_layers.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_layers_manager.ItemToObject(item)
        if obj.layer.active==False:
            return
        
        node = ObjectPolyline([obj.layer.name])
            
        self.component_objects.AddNode(node)
#         obj = self.tree_objects_manager.AppendObject('Part', node)
#         self.tree_objects_manager.Select(obj)
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
#         obj = self.tree_objects_manager.AppendObject('Part', node)
#         self.tree_objects_manager.Select(obj)
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
#         obj = self.tree_objects_manager.AppendObject('Part', node)
#         self.tree_objects_manager.Select(obj)
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
#         obj = self.tree_objects_manager.AppendObject('Part', node)
#         self.tree_objects_manager.Select(obj)
        self.state.DoPlace(node)

        if self.current_panel:
            self.current_panel.Destroy()
        self.current_panel = EditTextFrame(self.panel_edit_object, self.Render, node)

    def onImageDrawSize( self, event ):
        self.canvas.Viewport(self.image_draw.GetRect().width, self.image_draw.GetRect().height)
        self.canvas.Origin(self.image_draw.GetRect().width/2, self.image_draw.GetRect().height/2)
        