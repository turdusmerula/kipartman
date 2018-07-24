import math
import cairo
import re
import wx


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
    def __init__(self, canvas, name, color):
        self.canvas = canvas
        self.name = name
        self.color = color

        self.Resize()

    def Resize(self):
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.canvas.viewport.x, self.canvas.viewport.y)
        self.ctx = cairo.Context(self.surface)
        
    def Clear(self):
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.canvas.viewport.x, self.canvas.viewport.y)
        self.ctx = cairo.Context(self.surface)
#         self.ctx.set_operator(cairo.OPERATOR_CLEAR)
#        self.ctx.rectangle(0, 0, self.canvas.viewport.x, self.canvas.viewport.y)
#        self.ctx.fill()
    
    def Apply(self, ctx):
        ctx.set_source_rgb(self.color.r, self.color.g, self.color.b)

    def Render(self, ctx):
        pass

class Position(object):
    def __init__(self, x=0, y=0, angle=0):
        super(Position, self).__init__()
        self.x = x
        self.y = y
        self.angle = angle
    
    def Apply(self, ctx):
        ctx.move_to(self.x, self.y)
        ctx.rotate(self.angle)
        
class Drawing(object):
    def __init__(self):
        pass
    
    def Render(self, ctx):
        pass    

class Point(Drawing):
    def __init__(self, x=0, y=0):
        super(Point, self).__init__()
        self.x = x
        self.y = y
    
class Pad(Drawing):
    def __init__(self, smd=False, rect=False, thru_hole=False, oval=False):
        super(Pad, self).__init__()
        self.smd = smd
        self.thru_hole = thru_hole
        self.rect = rect
        self.oval = oval
        self.at = Point()
        self.size = Point()
        self.drill = 0
        
    def Render(self, ctx):
        ctx.set_line_width(0)
        if self.rect:
            ctx.rectangle(self.at.x-self.size.x/2, self.at.y-self.size.y/2, self.size.x, self.size.y)
            ctx.fill()
        elif self.oval:
            ctx.arc(self.at.x, self.at.y, self.size.x/2 , 0, 2*math.pi)
            ctx.fill()
        if self.thru_hole:
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

    def Render(self, ctx):
        ctx.set_line_width(self.width)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.move_to(self.start.x, self.start.y)
        ctx.line_to(self.end.x, self.end.y)
        ctx.stroke()
        
class PolyLine(Drawing):
    def __init__(self, points=[], width=0, fill=False):
        super(PolyLine, self).__init__()
        self.points = points
        self.width = width
        self.fill = fill
        
    def Render(self, ctx):
        ctx.set_line_width(self.width)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.move_to(self.points[0].x, self.points[0].y)
        for p in range(1, len(self.points)):
            ctx.line_to(self.points[p].x, self.points[p].y)
        if self.fill:
            ctx.fill()  
        else:
            ctx.stroke()

class MultiLine(Drawing):
    def __init__(self, lines=[], width=0):
        super(MultiLine, self).__init__()
        self.lines = lines
        self.width = width
        
    def Render(self, ctx):
        ctx.set_line_width(self.width)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        for l in self.lines:
            ctx.move_to(l[0].x, l[0].y)
            ctx.line_to(l[1].x, l[1].y)
        ctx.stroke()

class Circle(Drawing):
    def __init__(self, centre=Point(), end=Point(), width=0, fill=False):
        super(Circle, self).__init__()
        self.centre = centre
        self.end = end
        self.width = width
        self.fill = fill

    def Render(self, ctx):
        ctx.set_line_width(self.width)
        x1 = self.end.x-self.centre.x
        y1 = self.end.y-self.centre.y
        ctx.move_to(self.end.x, self.end.y)
        ctx.arc(self.centre.x, self.centre.y, math.sqrt(x1*x1+y1*y1), 0, 2*math.pi)
        if self.fill:
            ctx.fill()
        else:
            ctx.stroke()

class Rect(Drawing):
    def __init__(self, start=Point(), end=Point(), width=0, fill=False):
        super(Rect, self).__init__()
        self.start = start
        self.end = end
        self.width = width
        self.fill = fill

    def Render(self, ctx):
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
    def __init__(self, value=""):
        super(Text, self).__init__()
        self.value = value
        self.at = Position()
        self.anchor_x = 'left'
        self.anchor_y = 'top'
        
    def Render(self, ctx):
        ctx.save()
#        self.at.Apply(ctx)
        x, y, width, height, x_advance, y_advance=ctx.text_extents(self.value)
        posx = self.at.x
        posy = self.at.y

        if self.anchor_x=='center':
            posx = posx-width/2*math.cos(self.at.angle)
            posy = posy-width/2*math.sin(self.at.angle)
        
        if self.anchor_y=='center':
            posx = posx-height/2*math.sin(self.at.angle)
            posy = posy-height/2*math.cos(self.at.angle)
        
        ctx.move_to(posx, posy)
        ctx.rotate(self.at.angle)

        ctx.show_text(self.value)
        ctx.restore()

class Font(object):
    def __init__(self, size=Point(), thickness=0):
        self.size = size
        self.thickness = thickness

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
    
    def Update(self):
        for node in self.nodes:
            node.Update()

    def Render(self, canvas):
        for node in self.nodes:
            node.Render(canvas)
    
    def AddNode(self, node):
        node.parent = self
        self.nodes.append(node)

class Canvas(object):

    def __init__(self):
        self.layers = []
        self.layer_names = {}
        
        self.background = ColorRGB.Black()
        self.font = Font()
                
        self.zoom = float(1)
        self.origin = Point(0, 0)   # in px
        self.viewport = Point(100, 100) # in px
    
    def Zoom(self, zoom):
        self.zoom = zoom
        
    def Origin(self, x, y):
        self.origin = Point(x, y)   # in mm

    def Viewport(self, width, height):
        self.viewport = Point(width, height)   # in mm
        for layer in self.layers:
            layer.Resize()
            
    def AddLayer(self, name, color=ColorRGB.Black()):
        if name in self.layer_names:
            return self.layer_names[name]
        
        layer = Layer(self, name, color)
        self.layers.append(layer)
        self.layer_names[name] = layer
        
        return layer

    def SetFont(self, font):
        self.font = font

    def px2mm(self, pixels):
        px = float(wx.GetDisplaySize()[1])
        mm = float(wx.GetDisplaySizeMM()[1])
        mmperpx = mm/self.zoom/px
        return mmperpx*float(pixels)
    
    def mm2px(self, millimeters):
        px = float(wx.GetDisplaySize()[1])
        mm = float(wx.GetDisplaySizeMM()[1])
        pxpermm = px/mm/self.zoom
        return float(pxpermm)*millimeters

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
            
    def Draw(self, obj, layer_names):
        for name in layer_names:
            layer = self.layer_names[name]
            
            layer.Apply(layer.ctx)
            self.font.Apply(layer.ctx)
            obj.Render(layer.ctx)

    def Render(self, obj):
        obj.Render(self)
        
        # create image with whole drawing content
        img_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.viewport.x, self.viewport.y)
        img_ctx = cairo.Context(img_surface)
                
        # draw background
        img_ctx.rectangle(0, 0, self.viewport.x, self.viewport.y)
        img_ctx.set_source_rgb(self.background.r, self.background.g, self.background.b)
        img_ctx.fill() 

        for layer in self.layers:
            img_ctx.set_source_surface(layer.surface, 0, 0)
            img_ctx.paint()

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
#     def to_view_width(self, width):
#         x, y = self.ctx.device_to_user_distance(width, width)
#         return x 
    
class FootprintCanvas(Canvas):
    def __init__(self):
        super(FootprintCanvas, self).__init__()
                
        # add default layers
        self.AddLayer("editor", ColorRGB.Grey())

        self.AddLayer("B.Cu", ColorRGB.Blue())
        self.AddLayer("F.Cu", ColorRGB.Red())
#        self.AddLayer("B.Adhes")
#        self.AddLayer("F.Adhes")
#        self.AddLayer("B.Paste")
#        self.AddLayer("F.Paste")
        self.AddLayer("B.SilkS", ColorRGB.Grey())
        self.AddLayer("F.SilkS", ColorRGB.Grey())
#        self.AddLayer("B.Mask")
#        self.AddLayer("F.Mask")
        self.AddLayer("Dwgs.User", ColorRGB.Grey())
        self.AddLayer("Cmts.User", ColorRGB.Grey())
#        self.AddLayer("Eco1.User")
#        self.AddLayer("Eco2.User")
#        self.AddLayer("Edge.Cuts", ColorRGB.Grey())
#        self.AddLayer("Margin")
#        self.AddLayer("B.CrtYd", ColorRGB.Grey())
#        self.AddLayer("F.CrtYd", ColorRGB.Grey())
        self.AddLayer("B.Fab", ColorRGB.Grey())
        self.AddLayer("F.Fab", ColorRGB.Grey())

        self.AddLayer("selection", ColorRGB.Yellow())
        self.AddLayer("anchor", ColorRGB.Red())

class LibraryCanvas(Canvas):
    def __init__(self):
        super(LibraryCanvas, self).__init__()

        self.background = ColorRGB.White()
             
        # add default layers
        self.AddLayer("Label", ColorRGB.Black())
        self.AddLayer("Drawing", ColorRGB.Black())
