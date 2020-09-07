# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.utils
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from helper.class_tool import add_method, overload_method
import copy

import django.db.models.manager

@add_method(django.db.models.manager.BaseManager)
def add_pending(self, el):
    instance = self.instance
    field = self.field.remote_field
    if field.one_to_many:
        if hasattr(instance, "_add_pendings_")==False:
            setattr(instance, "_add_pendings_", {})
        add_pendings = getattr(instance, "_add_pendings_")
        if field.name not in add_pendings:
            add_pendings[field.name] = []
    else:
        raise f"{field.name}: add_pending only implemented for one_to_many relation "
    
    if hasattr(el, "_remove_pending_"):
        delattr(el, "_remove_pending_")
        
    add_pendings[field.name].append(el)

@add_method(django.db.models.manager.BaseManager)
def remove_pending(self, el):
    instance = self.instance
    field = self.field.remote_field

    if field.one_to_many:
        if hasattr(instance, "_remove_pendings_")==False:
            setattr(instance, "_remove_pendings_", {})
        remove_pendings = getattr(instance, "_remove_pendings_")
        if field.name not in remove_pendings:
            remove_pendings[field.name] = []
    else:
        raise f"{field.name}: remove_pending only implemented for one_to_many relation "
    
    if el not in remove_pendings[field.name]:
        remove_pendings[field.name].append(el)
    setattr(el, "_remove_pending_", True)


@add_method(django.db.models.manager.BaseManager)
def add_pendings(self):
    instance = self.instance
    field = self.field.remote_field
    if field.one_to_many:
        if hasattr(instance, "_add_pendings_"):
            add_pendings = getattr(instance, "_add_pendings_")
            if field.name in add_pendings:
                return add_pendings[field.name]
    else:
        raise f"{field.name}: pending functionality only implemented for one_to_many relation "

    return []

@add_method(django.db.models.manager.BaseManager)
def remove_pendings(self):
    instance = self.instance
    field = self.field.remote_field
    if field.one_to_many:
        if hasattr(instance, "_remove_pendings_"):
            remove_pendings = getattr(instance, "_remove_pendings_")
            if field.name in remove_pendings:
                return remove_pendings[field.name]
    else:
        raise f"{field.name}: pending functionality only implemented for one_to_many relation "

    return []

@add_method(django.db.models.manager.BaseManager)
def pendings(self):
    instance = self.instance
    field = self.field.remote_field
    res = []
    if field.one_to_many:
        if hasattr(instance, "_add_pendings_"):
            add_pendings = getattr(instance, "_add_pendings_")
            if field.name in add_pendings:
                res += add_pendings[field.name]
        if hasattr(instance, "_remove_pendings_"):
            remove_pendings = getattr(instance, "_remove_pendings_")
            if field.name in remove_pendings:
                res += remove_pendings[field.name]
    else:
        raise f"{field.name}: add_pending only implemented for one_to_many relation "

    return res



@overload_method(models.Model)
def save(self, overload, *args, **kwargs):
    res = overload(self, *args, **kwargs)
    
    if hasattr(self, "_add_pendings_"):
        pendings = getattr(self, "_add_pendings_")
        for field in pendings:
            for el in pendings[field]:
                el.save()
    
    if hasattr(self, "_remove_pendings_"):
        pendings = getattr(self, "_remove_pendings_")
        for field in pendings:
            while(len(pendings[field])>0):
                el = pendings[field].pop()
                el.delete()

    return res

@add_method(models.Model)
def removed_pending(self):
    if hasattr(self, "_remove_pending_"):
        return getattr(self, "_remove_pending_")
    
    return False

# @add_method(models.Model)
# def duplicate(self):
#     res = copy.copy(self)
#     res.pk = None
# 
#     for field in self._meta.get_fields():
#         if field.one_to_many:
#             
#             if hasattr(self, field.name):
#                 attr_name = field.name
#             elif hasattr(self, f"{field.name}_set"):
#                 attr_name = f"{field.name}_set"
#             related_object_manager = getattr(self, attr_name)
#             related_objects = list(related_object_manager.all())
#             if related_objects:
#                 print(f'{attr_name}:', related_objects)
#         elif field.many_to_one:
#             pass
#         elif field.many_to_many:
#             pass
#         
#     return res
# 
# @add_method(models.Model)
# def duplicate2(self):
#     """
#     Duplicate a model instance, making copies of all foreign keys pointing to it.
#     There are 3 steps that need to occur in order:
# 
#         1.  Enumerate the related child objects and m2m relations, saving in lists/dicts
#         2.  Copy the parent object per django docs (doesn't copy relations)
#         3a. Copy the child objects, relating to the copied parent object
#         3b. Re-create the m2m relations on the copied parent object
# 
#     """
#     related_objects_to_copy = []
#     relations_to_set = {}
#     # Iterate through all the fields in the parent object looking for related fields
#     for field in self._meta.get_fields():
#         if field.one_to_many:
#             # One to many fields are backward relationships where many child objects are related to the
#             # parent (i.e. SelectedPhrases). Enumerate them and save a list so we can copy them after
#             # duplicating our parent object.
#             print(f'Found a one-to-many field: {field.name}')
# 
#             # 'field' is a ManyToOneRel which is not iterable, we need to get the object attribute itself
#             if hasattr(self, field.name):
#                 related_object_manager = getattr(self, field.name)
#             elif hasattr(self, f"{field.name}_set"):
#                 related_object_manager = getattr(self, f"{field.name}_set")
#             related_objects = list(related_object_manager.all())
#             if related_objects:
#                 print(f' - {len(related_objects)} related objects to copy')
#                 related_objects_to_copy += related_objects
# 
#         elif field.many_to_one:
#             # In testing so far, these relationships are preserved when the parent object is copied,
#             # so they don't need to be copied separately.
#             print(f'Found a many-to-one field: {field.name}')
# 
#         elif field.many_to_many:
#             # Many to many fields are relationships where many parent objects can be related to many
#             # child objects. Because of this the child objects don't need to be copied when we copy
#             # the parent, we just need to re-create the relationship to them on the copied parent.
#             print(f'Found a many-to-many field: {field.name}')
#             if hasattr(self, field.name):
#                 related_object_manager = getattr(self, field.name)
#             elif hasattr(self, f"{field.name}_set"):
#                 related_object_manager = getattr(self, f"{field.name}_set")
#             relations = list(related_object_manager.all())
#             if relations:
#                 print(f' - {len(relations)} relations to set')
#                 relations_to_set[field.name] = relations
#             
#     # Duplicate the parent object
#     self.pk = None
# #    self.save()
#     print(f'Copied parent object ({str(self)})')
#  
#     # Copy the one-to-many child objects and relate them to the copied parent
#     for related_object in related_objects_to_copy:
#         # Iterate through the fields in the related object to find the one that relates to the
#         # parent model (I feel like there might be an easier way to get at this).
#         for related_object_field in related_object._meta.fields:
#             if related_object_field.related_model == self.__class__:
#                 # If the related_model on this field matches the parent object's class, perform the
#                 # copy of the child object and set this field to the parent object, creating the
#                 # new child -> parent relationship.
#                 related_object.pk = None
#                 setattr(related_object, related_object_field.name, self)
# #                 related_object.save()
#  
#                 text = str(related_object)
#                 text = (text[:40] + '..') if len(text) > 40 else text
#                 print(f'|- Copied child object ({text})')
#  
#     # Set the many-to-many relations on the copied parent
#     for field_name, relations in relations_to_set.items():
#         # Get the field by name and set the relations, creating the new relationships
#         field = getattr(self, field_name)
#         field.set(relations)
#         text_relations = []
#         for relation in relations:
#             text_relations.append(str(relation))
#         print(f'|- Set {len(relations)} many-to-many relations on {field_name} {text_relations}')
# 
#     return self

# def add_pending(obj):
#     def pending(self):
#         return self._pending
#     
#     def add(self, value):
#         self._pending.append(value)
#     
#     def remove(self, value):
#         self._pending.remove(value)
#     
#     setattr(obj, '_pending', [])
#     setattr(obj, 'pending', pending)
#     setattr(obj, 'add', add)
#     setattr(obj, 'remove', remove)

class PartCategory(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True, db_index=True)
    name = models.TextField()
    description = models.TextField(blank=True, default='')
    updated = models.DateTimeField(auto_now=True)
    
    @property
    def path(self):
        res = self.name
        parent = self.parent
        while parent:
            res = parent.name+"/"+res
            parent = parent.parent
        return "/"+res
    
    class MPTTMeta:
        order_insertion_by = ['name']
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)


class Part(models.Model):
    def __init__(self, *args, **kwargs):
        self.child_count = 0
        super(Part, self).__init__(*args, **kwargs)
        
#         add_pending(self.parameters)
#         print("+++", self.parameters._pending)
        
    name = models.TextField()
    description = models.TextField(blank=True, default='')
    comment = models.TextField(blank=True, default='')
    category = models.ForeignKey('PartCategory', on_delete=models.DO_NOTHING, null=True, blank=True, default=None)
    footprint = models.ForeignKey('VersionedFile', related_name='footprint', on_delete=models.DO_NOTHING, null=True, blank=True, default=None)
    symbol = models.ForeignKey('VersionedFile', related_name='symbol', on_delete=models.DO_NOTHING, null=True, blank=True, default=None)
    childs = models.ManyToManyField('Part', blank=True)
    #parameters is defined inside PartParameter by ForeignKey part
    #offers is defined inside PartOffer by ForeignKey part
    #manufacturers is defined inside PartManufacturer by ForeignKey part
    #storages is defined inside PartStorage by ForeignKey part
    #attachements: is defined inside PartAttachement by ForeignKey part
    #references: is defined inside PartReference by ForeignKey part
    value_parameter = models.TextField(null=True, blank=True, default=None)
    updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class PartReference(models.Model):
    part = models.ForeignKey('Part', related_name='references', null=False, blank=False, default=None, on_delete=models.CASCADE)
    type = models.TextField(null=False, blank=False)
    manufacturer = models.TextField(null=False, blank=True, default="")
    name = models.TextField(null=False, blank=False)
    description = models.TextField(null=False, blank=True, default="")
    uid = models.TextField(null=False, blank=False)
    updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return '%d: %s' % (self.id, self.type, self.name, self.uid)
    
class PartParameter(models.Model):
    part = models.ForeignKey('Part', related_name='parameters', null=False, blank=False, default=None, on_delete=models.CASCADE)
    parameter = models.ForeignKey('Parameter', related_name='parameter', on_delete=models.DO_NOTHING, null=False, blank=False)
    text_value = models.TextField(null=True, blank=True)
    min_value = models.FloatField(null=True)
    min_prefix = models.ForeignKey('UnitPrefix', related_name='min', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    nom_value = models.FloatField(null=True)
    nom_prefix = models.ForeignKey('UnitPrefix', related_name='nom', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    max_value = models.FloatField(null=True)
    max_prefix = models.ForeignKey('UnitPrefix', related_name='max', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        if self.id:
            return '%d: %s' % (self.id, self.name)
        else:
            return '<None>: %s' % (self.name)
            


class PartManufacturer(models.Model):
    part = models.ForeignKey('Part', related_name='manufacturers', null=False, blank=False, default=None, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.DO_NOTHING, null=False)
    part_name = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)


class PartOffer(models.Model):
    part = models.ForeignKey('Part', related_name='offers', null=False, blank=False, default=None, on_delete=models.CASCADE)
    distributor = models.ForeignKey('Distributor', on_delete=models.DO_NOTHING, null=True, blank=True, default=None)
    packaging_unit = models.IntegerField(default=1)
    min_order_quantity = models.IntegerField(default=1)
    quantity = models.IntegerField()
    available_stock = models.IntegerField(null=True, blank=True, default=None)
    unit_price = models.FloatField()
    packaging = models.TextField(blank=True)
    currency = models.TextField(blank=True)
    sku = models.TextField(blank=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)
    

class PartStorage(models.Model):
    part = models.ForeignKey('Part', related_name='storages', null=False, blank=False, default=None, on_delete=models.CASCADE)
    storage = models.ForeignKey('Storage', on_delete=models.DO_NOTHING, null=True, blank=True, default=None)
    quantity = models.IntegerField()
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class PartAttachement(models.Model):
    part = models.ForeignKey('Part', related_name='attachements', null=False, blank=False, default=None, on_delete=models.CASCADE)
    file = models.ForeignKey('File', on_delete=models.DO_NOTHING, null=False)
    description = models.TextField(blank=True, default='')
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%d: %d %s' % (self.part.pk, self.file.pk, self.description)

class Parameter(models.Model):
    name = models.TextField()
    description = models.TextField(blank=True)
    unit = models.ForeignKey('Unit', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    numeric = models.BooleanField()
    updated = models.DateTimeField(auto_now=True)

class ParameterAlias(models.Model):
    parameter = models.ForeignKey('Parameter', related_name='alias', null=False, blank=False, default=None, on_delete=models.CASCADE)
    
class Manufacturer(models.Model):
    name = models.TextField(blank=False)
    address = models.TextField(null=True, blank=True, default='')
    website = models.TextField(null=True, blank=True, default='')
    email = models.TextField(null=True, blank=True, default='')
    phone = models.TextField(null=True, blank=True, default='')
    comment = models.TextField(null=True, blank=True, default='')
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)


class Distributor(models.Model):
    name = models.TextField(blank=False)
    address = models.TextField(null=True, blank=True, default='')
    website = models.TextField(null=True, blank=True, default='')
    sku_url = models.TextField(null=True, blank=True, default='')
    email = models.TextField(null=True, blank=True, default='')
    phone = models.TextField(null=True, blank=True, default='')
    comment = models.TextField(null=True, blank=True, default='')
    allowed = models.BooleanField(null=False, default=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)


class File(models.Model):
    source_name = models.TextField()
    storage_path = models.TextField()
    created = models.DateTimeField(null=True, blank=True, default=None)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%d: %s, %s' % (self.id, self.source_name, self.storage_path)


class VersionedFileState(object):
    created = 0
    modified = 1
    deleted = 2
    
class VersionedFile(models.Model):
    source_path = models.TextField()
    storage_path = models.TextField(default='')
    md5 = models.TextField(null=False, blank=True, default='')
    version = models.IntegerField(default=0)
    state = models.IntegerField(default=0)
    metadata = models.TextField(null=True, blank=True, default='')
    category = models.TextField(null=True, blank=True, default='')
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%d: %s' % (self.id, self.source_path)
    
class VersionedFileHistory(models.Model):
    file = models.ForeignKey('VersionedFile', null=False, blank=False, default=None, on_delete=models.CASCADE)
    source_path = models.TextField()
    storage_path = models.TextField(default='')
    md5 = models.TextField(null=False, blank=True, default='')
    version = models.IntegerField(default=0)
    state = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    operation = models.TextField()


class Unit(models.Model):
    name = models.TextField()
    symbol = models.TextField(default='')
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)


class UnitPrefix(models.Model):
    name = models.TextField()
    # suffix name
    symbol = models.TextField()
    # value contains the exponent part
    power = models.TextField()
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class StorageCategory(MPTTModel):
    parent = TreeForeignKey('StorageCategory', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    name = models.TextField()
    description = models.TextField(blank=True, default='')
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class Storage(models.Model):
    category = models.ForeignKey('StorageCategory', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    name = models.TextField()
    description = models.TextField(blank=True, default='')
    comment = models.TextField(blank=True, default='')
    updated = models.DateTimeField(auto_now=True)

class PartStorageHistory(models.Model):
    part = models.ForeignKey('Part', null=False, blank=False, default=None, on_delete=models.CASCADE)
    location = models.ForeignKey('Storage', null=False, blank=False, default=None, on_delete=models.CASCADE)
    reason = models.TextField(blank=False)
    amount = models.IntegerField()
    updated = models.DateTimeField(auto_now=True)

class Currency(models.Model):
    name = models.TextField()
    symbol = models.TextField(default='')
    base = models.TextField(default='EUR')
    ratio = models.IntegerField()
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)
    