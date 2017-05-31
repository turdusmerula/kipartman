# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class PartCategory(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True, db_index=True)
    name = models.TextField()
    class MPTTMeta:
        order_insertion_by = ['name']
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)


class Part(models.Model):
    name = models.TextField()
    description = models.TextField(blank=True)
    category = models.ForeignKey('PartCategory', on_delete=models.DO_NOTHING, null=True, blank=True, default=None)
    footprint = models.ForeignKey('Footprint', on_delete=models.DO_NOTHING, null=True, blank=True, default=None)
    comment = models.TextField(null=True, blank=True, default='')
    parts = models.ManyToManyField('Part', blank=True)
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class PartParameter(models.Model):
    name = models.TextField()
    description = models.TextField(blank=True)
    unit = models.ForeignKey('Unit', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    numeric = models.BooleanField()
    text_value = models.TextField(null=True, blank=True)
    min_value = models.FloatField(null=True)
    min_exponent = models.ForeignKey('Exponent', related_name='min', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    nom_value = models.FloatField(null=True)
    nom_exponent = models.ForeignKey('Exponent', related_name='nom', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    max_value = models.FloatField(null=True)
    max_exponent = models.ForeignKey('Exponent', related_name='max', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)


class FootprintCategory(MPTTModel):
    parent = TreeForeignKey('FootprintCategory', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    name = models.TextField()
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class Footprint(models.Model):
    category = models.ForeignKey('FootprintCategory', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    name = models.TextField()
    description = models.TextField(blank=True)
    comment = models.TextField(null=True, blank=True, default='')
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)
    
class File(models.Model):
    filename = models.TextField()
    uuid = models.TextField()
    def __unicode__(self):
        return '%d: %s' % (self.uuid, self.filename)


class Unit(models.Model):
    name = models.TextField()
    description = models.TextField(blank=True)
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class Exponent(models.Model):
    name = models.TextField()
    # suffix name
    suffix = models.TextField()
    description = models.TextField(blank=True)
    # value contains the exponent part
    value = models.IntegerField()
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

