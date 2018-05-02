from kicad_object import KicadObject
from kicad_lib_file import KicadLibFile
import os
import Canvas
import re 
import math
import tempfile


class KicadSchematicFile(KicadLibFile):
    def __init__(self):
        super(KicadSchematicFile, self).__init__()

