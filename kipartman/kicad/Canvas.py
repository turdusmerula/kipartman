import math
import cairo
import re
import wx
import numpy as np
import copy

epsilon=1e-9

class ColorRGB(object):
    def __init__(self, r=0, g=0, b=0, l=1):
        self.r = r
        self.g = g
        self.b = b
        self.l = l

    @staticmethod
    def Red():
        return ColorRGB(1, 0, 0)

    @staticmethod
    def Blue():
        return ColorRGB(0, 0, 1)
    
    @staticmethod
    def Yellow():
        return ColorRGB(0.5, 0.5, 0)

    @staticmethod
    def White():
        return ColorRGB(1, 1, 1)
    
    @staticmethod
    def Black():
        return ColorRGB(0, 0, 0)

    @staticmethod
    def Grey():
        return ColorRGB(0.5, 0.5, 0.5)

class Layer(object):    
    def __init__(self, canvas, name, color, layer_type='', active=True):
        self.canvas = canvas
        self.name = name
        self.color = color
        self.layer_type = layer_type
        self.active = active

        self.recording = False
        
        self.Resize()

    def GetCtx(self):
        if self.recording:
            return self.recording_ctx
        return self.ctx

    def GetSurface(self):
        if self.recording:
            return self.recording_surface
        return self.surface
    
    def Resize(self):
        if self.recording:
            self.recording_surface = cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA, None)
            self.recording_ctx = cairo.Context(self.recording_surface)
        else:
            self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.canvas.viewport.x, self.canvas.viewport.y)
            self.ctx = cairo.Context(self.surface)
    
    def Recording(self, value):
        self.recording = value
        self.Clear()
        
    def Clear(self):
        self.Resize()
#         self.ctx.set_operator(cairo.OPERATOR_CLEAR)
#        self.ctx.rectangle(0, 0, self.canvas.viewport.x, self.canvas.viewport.y)
#        self.ctx.fill()
    
    def Apply(self, ctx):
        ctx.set_source_rgb(self.color.r, self.color.g, self.color.b)

    def Render(self, canvas):
        pass

class Drawing(object):
    def __init__(self):
        pass
    
    def Render(self, ctx, canvas):
        pass    
    
    def Apply(self, ctx):
        pass
    
class Point(Drawing):
    def __init__(self, x=0., y=0.):
        super(Point, self).__init__()
        self.x = x
        self.y = y

    def Rotate(self, origin, angle):
        dx = self.x-origin.x
        dy = self.y-origin.y
        c = math.cos(angle)
        s = math.sin(angle)
        return Point(origin.x+dx*c-dy*s, origin.y+dx*s+dy*c)

    # return angle between two points with self as origin in [-pi, pi]
    def GetAngle(self, p0, p1):
        v0 = np.array([p0.x-self.x, p0.y-self.y])
        v1 = np.array([p1.x-self.x, p1.y-self.y])
        angle = np.math.atan2(np.linalg.det([v0,v1]), np.dot(v0,v1))
        return angle
    
    # set angle of p1 relative to p0 with self as origin in [-pi, pi]
    def SetAngle(self, p0, p1, angle):
        d1x = p1.x-self.x
        d1y = p1.y-self.y
        d1 = math.sqrt(d1x*d1x+d1y*d1y)
        angle_start = self.GetAngle(Point(self.x+1, self.y), p0)
        p1.x = self.x+d1*math.cos(angle+angle_start)
        p1.y = self.y+d1*math.sin(angle+angle_start)
 
    def Distance(self, p):
        dx = self.x-p.x
        dy = self.y-p.y
        return math.sqrt(dx*dx+dy*dy)
    
class Position(Point):
    def __init__(self, x=0., y=0., angle=0.):
        super(Position, self).__init__(x, y)
        self.angle = angle
    
    def Apply(self, ctx):
        ctx.move_to(self.x, self.y)
        ctx.rotate(self.angle)
        
    def Rotate(self, origin, angle):
        dx = self.x-origin.x
        dy = self.y-origin.y
        c = math.cos(angle)
        s = math.sin(angle)
        return Position(origin.x+dx*c-dy*s, origin.y+dx*s+dy*c, self.angle)

class Pad(Drawing):
    def __init__(self, type='smd', shape='rect', at=Position(), size=Point(), drill=0):
        super(Pad, self).__init__()
        self.type = type # smd or thru_hole
        self.shape = shape # rect or oval
        self.at = at
        self.size = size
        self.drill = drill
        
    def Render(self, ctx, canvas):
        ctx.set_line_width(0)
        if self.shape=='rect':
            ctx.rectangle(self.at.x-self.size.x/2, self.at.y-self.size.y/2, self.size.x, self.size.y)

#             cx = self.size.x/2*math.cos(self.at.angle)
#             cy = self.size.y/2*math.sin(self.at.angle)
#             print "++", cx, cy
#             points = [Point(self.at.x-cx, self.at.y-cy), 
#                       Point(self.at.x+cx, self.at.y-cy), 
#                       Point(self.at.x+cx, self.at.y+cy),
#                       Point(self.at.x-cx, self.at.y+cy)]
#             ctx.set_line_width(0)
#             ctx.move_to(points[0].x, points[0].y)
#             for p in range(1, len(points)):
#                 ctx.line_to(points[p].x, points[p].y)
#             ctx.line_to(points[0].x, points[0].y)
            ctx.fill()
        elif self.shape=='oval':
            ctx.arc(self.at.x, self.at.y, self.size.x/2 , 0, 2*math.pi)
            ctx.fill()
        if self.type=='thru_hole':
            ctx.save()
            color = ColorRGB.Blue()
            ctx.set_source_rgb(color.r, color.g, color.b)
            #ctx.set_operator(cairo.OPERATOR_CLEAR)
            ctx.arc(self.at.x, self.at.y, self.drill/2 , 0, 2*math.pi)
            ctx.fill()
            ctx.restore()
            

class Line(Drawing):
    def __init__(self, start=Point(), end=Point(), width=0):
        super(Line, self).__init__()
        self.start = start
        self.end = end
        self.width = width

    def Render(self, ctx, canvas):
        ctx.set_line_width(self.width)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.move_to(self.start.x, self.start.y)
        ctx.line_to(self.end.x, self.end.y)
        ctx.stroke()

    # return the a and b coef of line equation y=a*x+b
    def get_ab(self):
        if math.fabs(self.end.x-self.start.x)<epsilon:
            a = None
            b = self.start.x
        else:
            a = (self.end.y-self.start.y)/(self.end.x-self.start.x)
            b = self.start.y-a*self.start.x
        return [a, b]
    
    # retrieve b from y=a*x+b given a point on the line and a
    @staticmethod
    def get_b(a, p0):
        b = p0.y-a*p0.x
        return b
    
    def get_center(self):
        pcx = math.fabs(self.start.x+self.end.x)
        pcy = math.fabs(self.start.y+self.end.y)
        
        return Point(pcx, pcy)
        
    # get projection of point on line
    def get_projection(self, p):
        a, b = self.get_ab()
        if a is None:
            return Point(b, p.y)
        if math.fabs(a)<epsilon:
            return Point(p.x, b)
        a1 = -1/a
        b1 = p.y-a1*p.x
        return Point((b-b1)/(a1-a), (b*a1-a*b1)/(a1-a))
    
    def get_intersection(self, line):
        p1 = self.start
        p2 = self.end
        p3 = line.start
        p4 = line.end
        
        u = (p4.y-p3.y)*(p2.x-p1.x)-(p4.x-p3.x)*(p2.y-p1.y)
        if math.fabs(u)>epsilon:
            v = ((p4.x-p3.x)*(p1.y-p3.y)-(p4.y-p3.y)*(p1.x-p3.x))/u
            w = ((p2.x-p1.x)*(p1.y-p3.y)-(p2.y-p1.y)*(p1.x-p3.x))/u
            if v>0. and v<1. and w>0. and w<1.:
                return Point(p1.x+v*(p2.x-p1.x), p1.y+w*(p2.y-p1.y))
        return None
    
class StraightLine(Line):
    def __init__(self, start=Point(), end=Point(), width=0):
        super(StraightLine, self).__init__(start, end, width)

    def Render(self, ctx, canvas):
        ctx.set_line_width(self.width)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        
        a, b = self.get_ab()
        if a is None:
            ctx.move_to(b, 0)
            ctx.line_to(b, canvas.viewport.y)
        else:
            ctx.move_to(1, b)
            ctx.line_to(canvas.viewport.x, a*canvas.viewport.x+b)
        ctx.stroke()

    def get_intersection(self, line):
        p1 = self.start
        p2 = self.end
        p3 = line.start
        p4 = line.end
        
        u = (p4.y-p3.y)*(p2.x-p1.x)-(p4.x-p3.x)*(p2.y-p1.y)
        if math.fabs(u)>epsilon:
            v = ((p4.x-p3.x)*(p1.y-p3.y)-(p4.y-p3.y)*(p1.x-p3.x))/u
            #w = ((p2.x-p1.x)*(p1.y-p3.y)-(p2.y-p1.y)*(p1.x-p3.x))/u
            return Point(p1.x+v*(p2.x-p1.x), p1.y+v*(p2.y-p1.y))

        return None
        

class PolyLine(Drawing):
    def __init__(self, points=[], width=0, fill=False):
        super(PolyLine, self).__init__()
        self.points = points
        self.width = width
        self.fill = fill
        
    def Render(self, ctx, canvas):
        ctx.set_line_width(self.width)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.move_to(self.points[0].x, self.points[0].y)
        for p in self.points:
            ctx.line_to(p.x, p.y)
        if self.fill:
            ctx.fill()  
        else:
            ctx.stroke()
        
class MultiLine(Drawing):
    def __init__(self, lines=[], width=0):
        super(MultiLine, self).__init__()
        self.lines = lines
        self.width = width
        
    def Render(self, ctx, canvas):
        ctx.set_line_width(self.width)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        for l in self.lines:
            ctx.move_to(l[0].x, l[0].y)
            ctx.line_to(l[1].x, l[1].y)
        ctx.stroke()

class Arrow(Drawing):
    def __init__(self, p0, p1, width=0):
        super(Arrow, self).__init__()
        self.p0 = p0
        self.p1 = p1
        self.width = width
        
        self.angle = math.pi/4
        self.length = 10
        
    def Render(self, ctx, canvas):
        ctx.set_line_width(self.width)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)

        ctx.move_to(self.p0.x, self.p0.y)
        ctx.line_to(self.p1.x, self.p1.y)
        
        #angle = math.atan2(self.p1.y,self.p1.x) - math.atan2(self.p0.y,self.p0.x)
        angle = math.atan2( self.p1.x-self.p0.x,  self.p1.y-self.p0.y)
        a0 = Point(self.p0.x+self.length*math.sin(angle+self.angle), self.p0.y+self.length*math.cos(angle+self.angle))
        a1 = Point(self.p0.x+self.length*math.sin(angle-self.angle), self.p0.y+self.length*math.cos(angle-self.angle))
        a2 = Point(self.p1.x+self.length*math.sin(angle+self.angle+math.pi), self.p1.y+self.length*math.cos(angle+self.angle+math.pi))
        a3 = Point(self.p1.x+self.length*math.sin(angle-self.angle+math.pi), self.p1.y+self.length*math.cos(angle-self.angle+math.pi))
        
        ctx.move_to(self.p0.x, self.p0.y)
        ctx.line_to(a0.x, a0.y)
        
        ctx.move_to(self.p0.x, self.p0.y)
        ctx.line_to(a1.x, a1.y)

        ctx.move_to(self.p1.x, self.p1.y)
        ctx.line_to(a2.x, a2.y)
        
        ctx.move_to(self.p1.x, self.p1.y)
        ctx.line_to(a3.x, a3.y)

        ctx.stroke()
        
        
class Circle(Drawing):
    def __init__(self, centre=Point(), end=Point(), width=0, fill=False):
        super(Circle, self).__init__()
        self.centre = centre
        self.end = end
        self.width = width
        self.fill = fill

    def Render(self, ctx, canvas):
        ctx.set_line_width(self.width)
        x1 = self.end.x-self.centre.x
        y1 = self.end.y-self.centre.y
        radius = math.sqrt(x1*x1+y1*y1)
        ctx.move_to(self.centre.x+radius, self.centre.y)
        ctx.arc(self.centre.x, self.centre.y, radius, 0, 2.*math.pi)
        if self.fill:
            ctx.fill()
        else:
            ctx.stroke()

    def get_projection(self, p):
        pref = Point(self.centre.x+1., self.centre.y)
        angle = self.centre.GetAngle(pref, p)
        dx = self.centre.x-self.end.x
        dy = self.centre.y-self.end.y
        radius = math.sqrt(dx*dx+dy*dy)
        return Point(self.centre.x+radius*math.cos(angle), self.centre.y+radius*math.sin(angle))

    
class Arc(Drawing):
    def __init__(self, centre=Point(), radius=0., angle_start=0., angle_end=0., width=0, fill=False):
        super(Arc, self).__init__()
        self.centre = centre
        self.radius = radius
        self.angle_start = angle_start
        self.angle_end = angle_end
        self.width = width
        self.fill = fill

    def Render(self, ctx, canvas):
        ctx.set_line_width(self.width)
        ctx.move_to(self.centre.x+self.radius*math.cos(self.angle_start), self.centre.y+self.radius*math.sin(self.angle_start))
        ctx.arc(self.centre.x, self.centre.y, self.radius, self.angle_start, self.angle_end)
        if self.fill:
            ctx.fill()
        else:
            ctx.stroke()

    def norm(self, angle):
        while angle>2.*math.pi:
            angle = angle-2.*math.pi
        while angle<0:
            angle = angle+2.*math.pi
        return angle
    
    def angle_len(self, start, end):
        if start<end:
            return end-start
        else:
            return 2.*math.pi-math.fabs(start-end)
    
    # get projection of point on line
    def get_projection(self, p):
        pref = Point(self.centre.x+1, self.centre.y)
        angle = self.norm(self.centre.GetAngle(pref, p)+math.pi)
        angle_point = self.centre.GetAngle(pref, p)

        angle_start = self.norm(self.angle_start)
        angle_end = self.norm(self.angle_end)
        angle_len = self.angle_len(angle_start, angle_end)

        if angle<angle_start:
            angle = angle+2.*math.pi
        if angle>=angle_start and angle<=angle_start+angle_len:
            return Point(self.centre.x+self.radius*math.cos(angle_point), self.centre.y+self.radius*math.sin(angle_point))            
        return None
    
class Rect(Drawing):
    def __init__(self, start=Point(), end=Point(), width=0, fill=False):
        super(Rect, self).__init__()
        self.start = start
        self.end = end
        self.width = width
        self.fill = fill

    def Render(self, ctx, canvas):
        ctx.set_line_width(self.width)
        ctx.move_to(self.start.x, self.start.y)
        ctx.line_to(self.start.x, self.end.y)
        ctx.line_to(self.end.x, self.end.y)
        ctx.line_to(self.end.x, self.start.y)
        ctx.line_to(self.start.x, self.start.y)
        
        #ctx.rectangle(self.start.x, self.start.y, self.end.x, self.end.y)
        if self.fill:
            ctx.fill()
        else:
            ctx.stroke()

class Text(Drawing):
    def __init__(self, value="", at=Position(), anchor_x='left', anchor_y='top', anchor_margin=0):
        super(Text, self).__init__()
        self.value = value
        self.at = at
        self.anchor_x = anchor_x # left | center | right
        self.anchor_y = anchor_y # top | center | bottom
        self.anchor_margin = anchor_margin
        
    def Render(self, ctx, canvas):
        ctx.save()
#        self.at.Apply(ctx)
        x, y, width, height, x_advance, y_advance=ctx.text_extents(self.value)
        posx = self.at.x-self.anchor_margin*math.cos(self.at.angle+math.pi/2.)
        posy = self.at.y-self.anchor_margin*math.sin(self.at.angle+math.pi/2.)
        
        if self.anchor_x=='center':
            posx = posx-width/2.*math.cos(self.at.angle)
            posy = posy-width/2.*math.sin(self.at.angle)
         
        if self.anchor_y=='center':
            posx = posx+height/2.*math.cos(self.at.angle+math.pi/2.)
            posy = posy+height/2.*math.sin(self.at.angle+math.pi/2.)
        
#        posx = posx+self.anchor_margin*math.cos(self.at.angle)
#        posY = posy+self.anchor_margin*math.sin(self.at.angle)

        ctx.move_to(posx, posy)
        ctx.rotate(self.at.angle)

        ctx.show_text(self.value)
        ctx.restore()

class Font(object):
    def __init__(self, size=Point(), thickness=0, style='normal'):
        self.size = size
        self.thickness = thickness
        self.style = style  # normal italic
        
    def Apply(self, ctx):
        if self.size.x>self.size.y:
            ctx.set_font_size(self.size.x)
        else:
            ctx.set_font_size(self.size.y)


def regex_match(value1, value2):
    value1 = value1.replace('.', '\.').replace('*', '.*')
    pattern = re.compile(value1)
    return pattern.match(value2)

class Object(object):
    def __init__(self, layers):
        self.parent = None
        self.layers = layers
        self.nodes = []
        
        self.surface = None
    
    def Copy(self, obj):
        obj.parent = self.parent
        obj.layers = copy.copy(self.layers)
        obj.nodes = []
        
        obj.surface = self.surface
        
    def Update(self):
        for node in self.nodes:
            node.Update()

    def Render(self, canvas):
        for node in self.nodes:
            node.Render(canvas)
    
    def AddNode(self, node):
        node.parent = self
        self.nodes.append(node)

    def RemoveNode(self, node):
        self.nodes.remove(node)
    
    def ClearNodes(self):
        self.nodes = []
        
    def Parent(self):
        return self.parent
        
class Canvas(object):

    def __init__(self):
        self.layers = []
        self.layer_names = {}
        self.selected_layers = []
        
        self.background = ColorRGB.Black()
        self.font = Font()
                
        self.zoom = float(1)
        self.origin = Point(0, 0)   # in px
        self.viewport = Point(100, 100) # in px
    
        # create image with whole drawing content
        self.img_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.viewport.x, self.viewport.y)
        self.img_ctx = cairo.Context(self.img_surface)

    def Zoom(self, zoom):
        self.zoom = zoom
            
    def Origin(self, x, y):
        self.origin = Point(x, y)   # in mm

    def Viewport(self, width, height):
        self.viewport = Point(width, height)   # in mm
        for layer in self.layers:
            layer.Resize()
        
        # create image with whole drawing content
        self.img_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.viewport.x, self.viewport.y)
        self.img_ctx = cairo.Context(self.img_surface)

            
    def AddLayer(self, name, color=ColorRGB.Black(), layer_type='', active=True):
        if name in self.layer_names:
            return self.layer_names[name]
        
        layer = Layer(self, name, color, layer_type, active)
        self.layers.append(layer)
        self.layer_names[name] = layer
        
        return layer

    def SelectLayer(self, layer):
        self.selected_layers = [layer]
        
    def SelectLayers(self, layers):
        self.selected_layers = layers

    def SetFont(self, font):
        self.font = font

    def px2mm(self, pixels):
        px = float(wx.GetDisplaySize()[1])
        mm = float(wx.GetDisplaySizeMM()[1])
        mmperpx = mm/px
        return mmperpx*float(pixels)/self.zoom
    
    def mm2px(self, millimeters):
        px = float(wx.GetDisplaySize()[1])
        mm = float(wx.GetDisplaySizeMM()[1])
        pxpermm = px/mm
        return pxpermm*millimeters*self.zoom

    # get x position in pixels from mm
    def xmm2px(self, posmm):
        return self.mm2px(self.px2mm(self.origin.x)+posmm)
        
    # get y position in pixels from mm
    def ymm2px(self, posmm):
        return self.mm2px(self.px2mm(self.origin.y)+posmm)

    # get x position in mm from px
    def xpx2mm(self, pospx):
        return self.px2mm(pospx)-self.px2mm(self.origin.x)
        
    # get y position in pixels from mm
    def ypx2mm(self, pospx):
        return self.px2mm(pospx)-self.px2mm(self.origin.y)

    def Clear(self, layer_names=None):
        if layer_names:
            for name in layer_names:
                self.layer_names[name].Clear()
        else:
            for layer in self.layers:
                layer.Clear()
            
    def Draw(self, obj, layer_names=None):
        if not layer_names:
            layer_names = self.selected_layers

        for layer_name in layer_names:
            if layer_name.startswith('*'):
                layer = self.layer_names[layer_name.replace("*", "F")]
                layer.Apply(layer.GetCtx())
                self.font.Apply(layer.GetCtx())
                obj.Render(layer.GetCtx(), self)

                layer = self.layer_names[layer_name.replace("*", "B")]
                layer.Apply(layer.GetCtx())
                self.font.Apply(layer.GetCtx())
                obj.Render(layer.GetCtx(), self)
            else:
                layer = self.layer_names[layer_name]
                layer.Apply(layer.GetCtx())
                self.font.Apply(layer.GetCtx())
                obj.Render(layer.GetCtx(), self)

    def Render(self, obj):
        obj.Render(self)
                
        # draw background
        self.img_ctx.rectangle(0, 0, self.viewport.x, self.viewport.y)
        self.img_ctx.set_source_rgb(self.background.r, self.background.g, self.background.b)
        self.img_ctx.fill() 

        for layer in self.layers:
            self.img_ctx.set_source_surface(layer.surface, 0, 0)
            self.img_ctx.paint()

        return self.img_surface

    def RenderFit(self, obj):
        for layer in self.layers:
            layer.Recording(True)
            
        obj.Render(self)

        s_x = None
        s_y = None
        s_width = None
        s_height = None

        for layer in self.layers:
            x, y, width, height = layer.GetSurface().ink_extents()
            if math.fabs(x)>epsilon and math.fabs(y)>epsilon and math.fabs(width)>epsilon and math.fabs(height)>epsilon:
                if s_x is None:
                    s_x, s_y, s_width, s_height = x, y, width, height
                else:
                    if x<s_x:
                        s_x = x
                    if y<s_y:
                        s_y = y
                    if width>s_width:
                        s_width = width
                    if height>s_height:
                        s_height = height
        if s_x is None:
            s_x, s_y, s_width, s_height = 0., 0., 0., 0.
        print("--", s_x, s_y, s_width, s_height)
        
        # create image with whole drawing content
        img_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.viewport.x, self.viewport.y)
        img_ctx = cairo.Context(img_surface)
                
        ratio = s_width
        decx = 0.
        decy = math.fabs(s_width-s_height)/2.
        if s_height>s_width:
            ratio = s_height
            decx = math.fabs(s_width-s_height)/2.
            decy = 0.
        if math.fabs(ratio)>epsilon:
            img_ctx.scale(self.viewport.x/ratio, self.viewport.y/ratio) # Normalizing the canvas
         
        # draw background
        img_ctx.rectangle(0, 0, self.viewport.x, self.viewport.y)
        img_ctx.set_source_rgb(self.background.r, self.background.g, self.background.b)
        img_ctx.fill() 
 
        for layer in self.layers:
            x, y, width, height = layer.GetSurface().ink_extents()
            img_ctx.set_source_surface(layer.GetSurface(), -x+decx, -y+decy)
            img_ctx.paint()

        for layer in self.layers:
            layer.Recording(False)
        
        return img_surface
        
#     def Render(self, width, height):
#         # create drawing
#         surface = cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA, None)
#         self.ctx = cairo.Context (surface)
# 
#         s_x, s_y, s_width, s_height = surface.ink_extents()
# 
#         # create image with whole drawing content
#         WIDTH, HEIGHT = 256, 256        
#         img_surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, width, height)
#         img_ctx = cairo.Context (img_surface)
#         
#         ratio = s_width
#         decx = 0
#         decy = math.fabs(s_width-s_height)/2
#         if s_height>s_width:
#             ratio = s_height
#             decx = math.fabs(s_width-s_height)/2
#             decy = 0
#         if ratio>0:
#             img_ctx.scale (WIDTH/ratio, HEIGHT/ratio) # Normalizing the canvas
#         
#         # draw background
#         img_ctx.rectangle(0, 0, WIDTH*ratio, HEIGHT*ratio)
#         img_ctx.set_source_rgb(self.background.r, self.background.g, self.background.b)
#         img_ctx.fill() 
# 
#         img_ctx.set_source_surface(surface, -s_x+decx, -s_y+decy)
#         img_ctx.paint()
# 
#         return img_surface
#     
    def to_view_width(self, width):
        x, y = self.img_ctx.device_to_user_distance(width, width)
        return x 
    
class FootprintCanvas(Canvas):
    def __init__(self):
        super(FootprintCanvas, self).__init__()
                
        self.AddLayer("B.Adhes", layer_type='Layer')
        self.AddLayer("F.Adhes", layer_type='Layer')
        self.AddLayer("B.Paste", layer_type='Layer')
        self.AddLayer("F.Paste", layer_type='Layer')
        self.AddLayer("B.SilkS", ColorRGB.Grey(), layer_type='Layer')
        self.AddLayer("F.SilkS", ColorRGB.Grey(), layer_type='Layer')
        self.AddLayer("B.Mask", layer_type='Layer')
        self.AddLayer("F.Mask", layer_type='Layer')
        self.AddLayer("Dwgs.User", ColorRGB.Grey(), layer_type='Layer', active=False)
        self.AddLayer("Cmts.User", ColorRGB.Grey(), layer_type='Layer', active=False)
        self.AddLayer("Eco1.User", layer_type='Layer', active=False)
        self.AddLayer("Eco2.User", layer_type='Layer', active=False)
        self.AddLayer("Edge.Cuts", ColorRGB.Grey(), layer_type='Layer', active=False)
        self.AddLayer("Margin", layer_type='Layer', active=False)
        self.AddLayer("B.CrtYd", ColorRGB.Grey(), layer_type='Layer')
        self.AddLayer("F.CrtYd", ColorRGB.Grey(), layer_type='Layer')
        self.AddLayer("B.Fab", ColorRGB.Grey(), layer_type='Layer')
        self.AddLayer("F.Fab", ColorRGB.Grey(), layer_type='Layer')
        self.AddLayer("B.Cu", ColorRGB.Blue(), layer_type='Layer', active=False)
        self.AddLayer("F.Cu", ColorRGB.Red(), layer_type='Layer', active=False)

        # add default layers
        self.AddLayer("Pads Front", ColorRGB.Yellow(), layer_type='Render', active=False)
        self.AddLayer("Pads Back", ColorRGB.Yellow(), layer_type='Render', active=False)
        self.AddLayer("Hidden Text", ColorRGB.Yellow(), layer_type='Render', active=False)
        self.AddLayer("Grid", ColorRGB.Yellow(), layer_type='Render', active=False)
        self.AddLayer("Values", ColorRGB.Yellow(), layer_type='Render', active=False)
        self.AddLayer("References", ColorRGB.Yellow(), layer_type='Render', active=False)

        self.AddLayer("Selection", ColorRGB.Yellow(), layer_type='Render', active=False)
        self.AddLayer("Hole", layer_type='Render', active=False)
        self.AddLayer("Editor", ColorRGB.Grey(), layer_type='Render', active=False)
        self.AddLayer("Anchor", ColorRGB.Yellow(), layer_type='Render', active=False)

class LibraryCanvas(Canvas):
    def __init__(self):
        super(LibraryCanvas, self).__init__()

        self.background = ColorRGB.White()
             
        # add default layers
        self.AddLayer("Label", ColorRGB.Black())
        self.AddLayer("Drawing", ColorRGB.Black())
