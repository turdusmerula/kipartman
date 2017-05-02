# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class PartCategory(models.Model):
    parent = models.ForeignKey('PartCategory', models.DO_NOTHING, null=True, default=None, blank=True)
    name = models.TextField()
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class Part(models.Model):
    category = models.ForeignKey('PartCategory', models.DO_NOTHING)
    metapart = models.BooleanField()
    name = models.TextField()
    description = models.TextField(blank=True)
    footprint = models.ForeignKey('Footprint', models.DO_NOTHING, null=True, default=None, blank=True)
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class FootprintCategory(models.Model):
    parent = models.ForeignKey('FootprintCategory', models.DO_NOTHING, null=True, default=None, blank=True)
    name = models.TextField()
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class Footprint(models.Model):
    category = models.ForeignKey('FootprintCategory', models.DO_NOTHING)
    name = models.TextField()
    description = models.TextField(blank=True)
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)
    
