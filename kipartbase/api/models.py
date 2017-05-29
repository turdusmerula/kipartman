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
