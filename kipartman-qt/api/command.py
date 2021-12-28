from PyQt6.QtCore import QObject, pyqtSignal
from django.db import transaction
from click.decorators import command

class Command(QObject):
    def __init__(self, description=""):
        self.description = description

    def Do(self, *args, **kwargs):
        pass
    
    def Undo(self):
        pass

class CommandStack(QObject):
    on_do = pyqtSignal()
    on_undo = pyqtSignal()
    on_redo = pyqtSignal()
    on_flush = pyqtSignal()

    def __init__(self):
        super(CommandStack, self).__init__()
        
        self.undo = []
        self.redo = []
        
        self.transaction = None
        
        transaction.set_autocommit(False)
        self.transaction = transaction.atomic(savepoint=True, durable=True)
        self.transaction.__enter__()


    def Do(self, command_type, *args, **kwargs):
        command = command_type(*args, **kwargs)
        command.Do()
        self.undo.append(command)
        self.redo = []
        self.on_do.emit()
        
    def Undo(self):
        command = self.undo.pop()
        command.Undo()
        self.redo.append(command)
        self.on_undo.emit()
        return command

    def Redo(self):
        command = self.redo.pop()
        command.Do()
        self.undo.append(command)
        self.on_redo.emit()

    def Flush(self):
        """ Validate database transactions and flush the undo list """
        self.transaction.__exit__(None, None, None)
        transaction.commit()
        
        self.transaction = transaction.atomic(savepoint=True, durable=True)
        self.transaction.__enter__()
        
        self.undo = []
        self.redo = []
        self.on_flush.emit()

    @property
    def HasUndo(self):
        return len(self.undo)>0

    @property
    def HasRedo(self):
        return len(self.redo)>0

    @property
    def LastUndo(self):
        return self.undo[-1]

    @property
    def LastRedo(self):
        return self.redo[-1]
    
commands = CommandStack()


class CommandUpdateDatabaseField(Command):
    def __init__(self, description, object, field, value):
        super(CommandUpdateDatabaseField, self).__init__(description)
        self.object = object
        self.field = field
        self.value = value

        self.prev_value = getattr(self.object, self.field)

    def Do(self):
        self.sid = transaction.savepoint()

        setattr(self.object, self.field, self.value)
        self.object.save(update_fields=[self.field])
        self.object.refresh_from_db()
        
    def Undo(self):
        transaction.savepoint_rollback(self.sid)
        self.object.refresh_from_db()


# class CommandAdd(Command):
#     def __init__(self, *args, **kwargs):
#         super(CommandAdd, self).__init__(*args, **kwargs)
#
# class CommandUpdate(Command):
#     def __init__(self, *args, **kwargs):
#         super(CommandUpdate, self).__init__(*args, **kwargs)
#
# class CommandDelete(Command):
#     def __init__(self, *args, **kwargs):
#         super(CommandUpdate, self).__init__(*args, **kwargs)
