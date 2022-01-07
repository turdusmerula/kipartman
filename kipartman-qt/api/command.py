from PyQt6.QtCore import QObject, pyqtSignal
from django.db import transaction
from api.event import events

class Command(QObject):
    beforeDo = pyqtSignal()
    done = pyqtSignal()
    beforeUndo = pyqtSignal()
    undone = pyqtSignal()

    def __init__(self, description=""):
        super(Command, self).__init__()
        
        self.description = description

    def Do(self, *args, **kwargs):
        pass
    
    def Undo(self):
        pass

class CommandStack(QObject):
    beforeDo = pyqtSignal(Command)
    done = pyqtSignal(Command)
    beforeUndo = pyqtSignal(Command)
    undone = pyqtSignal(Command)
    beforeRedo = pyqtSignal(Command)
    redone = pyqtSignal(Command)
    flushed = pyqtSignal(Command)

    def __init__(self):
        super(CommandStack, self).__init__()
        
        self.undo = []
        self.redo = []
        
        self.transaction = None
        
        transaction.set_autocommit(False)
        # django transaction object is made to be called from a with statement, we simulate it
        self.transaction = transaction.atomic(savepoint=True, durable=True)
        self.transaction.__enter__()


    def Do(self, command_type, *args, **kwargs):
        command = command_type(*args, **kwargs)
        
        command.beforeDo.emit()
        self.beforeDo.emit(command)
        
        command.Do()
        self.undo.append(command)
        self.redo = []
        
        command.done.emit()
        self.done.emit(command)
        return command

    def Undo(self):
        command = self.undo.pop()

        command.beforeUndo.emit()
        self.beforeUndo.emit(command)

        command.Undo()
        self.redo.append(command)
        
        command.undone.emit()
        self.undone.emit(command)
        return command

    def Redo(self):
        command = self.redo.pop()
        
        command.beforeDo.emit()
        self.beforeRedo.emit(command)

        command.Do()
        self.undo.append(command)
        
        command.done.emit()
        self.redone.emit(command)
        return command

    def Flush(self):
        """ Validate database transactions and flush the undo list """
        
        self.transaction.__exit__(None, None, None)
        transaction.commit()
        
        self.transaction = transaction.atomic(savepoint=True, durable=True)
        self.transaction.__enter__()
        
        self.undo = []
        self.redo = []
        self.flushed.emit()

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
        print("&&", type(self.object), self.object)
        self.object.save(update_fields=[self.field])
        # self.object.refresh_from_db()
        events.objectUpdated.emit(self.object)
        
    def Undo(self):
        transaction.savepoint_rollback(self.sid)
        # self.object.refresh_from_db()
        setattr(self.object, self.field, self.prev_value)
        events.objectUpdated.emit(self.object)

class CommandAddDatabaseObject(Command):
    def __init__(self, description, object):
        super(CommandAddDatabaseObject, self).__init__(description)
        self.object = object

    def Do(self):
        self.sid = transaction.savepoint()

        self.object.save()
        events.objectAdded.emit(self.object)
        
    def Undo(self):
        transaction.savepoint_rollback(self.sid)
        events.objectDeleted.emit(self.object, self.object.id)
        self.object.id = None

class CommandDeleteDatabaseObject(Command):
    def __init__(self, description, object):
        super(CommandDeleteDatabaseObject, self).__init__(description)
        self.object = object
        self.object_id = object.id
        
    def Do(self):
        self.sid = transaction.savepoint()

        self.object.delete()
        self.object.id = None
        events.objectDeleted.emit(self.object, self.object_id)
        
    def Undo(self):
        transaction.savepoint_rollback(self.sid)
        self.object.id = self.object_id
        events.objectAdded.emit(self.object)

class CommandDeleteDatabaseObjects(Command):
    def __init__(self, description, objects):
        super(CommandDeleteDatabaseObjects, self).__init__(description)
        self.objects = objects
        self.object_to_id = {id(obj):obj.id for obj in objects}
        
    def Do(self):
        self.sid = transaction.savepoint()

        for obj in self.objects:
            id = obj.id
            obj.delete()
            obj.id = None
            events.objectDeleted.emit(obj, id)
        
    def Undo(self):
        transaction.savepoint_rollback(self.sid)
        for obj in self.objects:
            obj.id = self.object_to_id[id(obj)]
            events.objectAdded.emit(obj)

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
