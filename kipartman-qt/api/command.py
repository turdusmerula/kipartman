from PyQt6.QtCore import QObject, pyqtSignal

class Command(QObject):
    def __init__(self, description=""):
        self.description = description

    def Do(self, *args, **kwargs):
        pass
    
    def Undo(self):
        pass

class CommandStack(QObject):
    on_undo = pyqtSignal(Command)
    on_redo = pyqtSignal(Command)

    def __init__(self):
        super(CommandStack, self).__init__()
        
        self.undo = []
        self.redo = []
    

    def Do(self, command, *args, **kwargs):
        command.Do(*args, **kwargs)
        self.undo.append(command)
        self.redo = []
        
    def Undo(self):
        command = self.undo.pop()
        command.Undo()
        self.redo.append(command)
        return command

    def Redo(self):
        command = self.redo.pop()
        command.Do()
        self.undo.append(command)
    
    def Flush(self):
        self.undo = []
        self.redo = []

    def HasUndo(self):
        return len(self.undo)>0

    def HasRedo(self):
        return len(self.undo)>0
    
commands = CommandStack()



class CommandAdd(Command):
    def __init__(self, *args, **kwargs):
        super(CommandAdd, self).__init__(*args, **kwargs)

class CommandUpdate(Command):
    def __init__(self, *args, **kwargs):
        super(CommandUpdate, self).__init__(*args, **kwargs)

class CommandDelete(Command):
    def __init__(self, *args, **kwargs):
        super(CommandUpdate, self).__init__(*args, **kwargs)
