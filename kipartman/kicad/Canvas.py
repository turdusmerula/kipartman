import math
import cairo

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
    def White():
        return ColorRGB(1, 1, 1)
    
    @staticmethod
    def Black():
        return ColorRGB(0, 0, 0)

    @staticmethod
    def Grey():
        return ColorRGB(0.5, 0.5, 0.5)

class Layer(object):    
    def __init__(self, name, color):
        self.name = name
        self.color = color
        
    def Apply(self, ctx):
        ctx.set_source_rgb(self.color.r, self.color.g, self.color.b)
        
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
    def __init__(self, smd=False, rect=False):
        super(Pad, self).__init__()
        self.smd = smd
        self.rect = rect
        self.at = Point()
        self.size = Point()
        self.drill = 0
        
    def Render(self, ctx):
        ctx.set_line_width(0)
        if self.rect:
            ctx.rectangle(self.at.x-self.size.x/2, self.at.y-self.size.y/2, self.size.x, self.size.y)
            ctx.fill()
            
class Line(Drawing):
    def __init__(self):
        super(Line, self).__init__()
        self.start = Point()
        self.end = Point()
        self.width = 0

    def Render(self, ctx):
        ctx.set_line_width(self.width)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.move_to(self.start.x, self.start.y)
        ctx.line_to(self.end.x, self.end.y)
        ctx.stroke()
        
class Rect(Drawing):
    def __init__(self, effect=None):
        super(Rect, self).__init__()
        self.at = Point()
        self.size = Point()

class Circle(Drawing):
    def __init__(self, effect=None):
        super(Circle, self).__init__()

class Text(Drawing):
    def __init__(self, effect=None):
        super(Text, self).__init__()

class Canvas(object):

    def __init__(self):
        self.layers = []
        self.current_layers = []
        self.background = ColorRGB.Black()
                
    def AddLayer(self, name, color=ColorRGB.Black()):
        for layer in self.layers:
            if layer.name==name:
                return layer
        
        layer = Layer(name, color)
        self.layers.append(layer)
        return layer

    def SelectLayer(self, name):
        self.current_layers = []
        for layer in self.layers:
            if layer.name==name:
                self.current_layers.append(layer)
                return

    def SelectLayers(self, names):
        self.current_layers = []
        for name in names:
            for layer in self.layers:
                if layer.name==name:
                    self.current_layers.append(layer)
    
    def Draw(self, obj):
        for layer in self.current_layers:
            print "--", layer.name
            layer.Apply(self.ctx)
            obj.Render(self.ctx)
                
    def Render(self, obj):
        
        # create drawing
        surface = cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA, None)
        self.ctx = cairo.Context (surface)
        
        # draw all objects
        for node in obj.nodes:
            node.Render(self)

        x, y, width, height = surface.ink_extents()

        # create image with whole drawing content
        WIDTH, HEIGHT = 256, 256        
        img_surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
        img_ctx = cairo.Context (img_surface)
        
        ratio = width
        decx = 0
        decy = math.fabs(width-height)/2
        if height>width:
            ratio = height
            decx = math.fabs(width-height)/2
            decy = 0
        img_ctx.scale (WIDTH/ratio, HEIGHT/ratio) # Normalizing the canvas
        
        # draw background
        img_ctx.rectangle(0, 0, WIDTH, HEIGHT)
        img_ctx.set_source_rgb(self.background.r, self.background.g, self.background.b)
        img_ctx.fill() 

        img_ctx.set_source_surface(surface, -x+decx, -y+decy)
        img_ctx.paint()

        return img_surface
    
    
class FootprintCanvas(Canvas):
    def __init__(self):
        super(FootprintCanvas, self).__init__()
                
        # add default layers
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
        self.AddLayer("Cmts.User")
#        self.AddLayer("Eco1.User")
#        self.AddLayer("Eco2.User")
#        self.AddLayer("Edge.Cuts", ColorRGB.Grey())
#        self.AddLayer("Margin")
#        self.AddLayer("B.CrtYd", ColorRGB.Grey())
#        self.AddLayer("F.CrtYd", ColorRGB.Grey())
#        self.AddLayer("B.Fab")
#        self.AddLayer("F.Fab")

        # add default effects
    