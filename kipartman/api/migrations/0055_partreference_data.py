# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-01 13:36
from __future__ import unicode_literals

from django.db import migrations
import api.models

# Add default values to database

# create default values for units
def migrate_references(apps, schema_editor):
    fparts = api.models.Part.objects.all()
    for fpart in fparts:
        if fpart.octopart and fpart.octopart_uid:
            if len(fpart.references.all())==0:
                print("Migrate octopart data for ", fpart.id)
                fpart_reference = api.models.PartReference()
                fpart_reference.part = fpart
                fpart_reference.type = 'octopart'
                fpart_reference.name = fpart.octopart
                fpart_reference.uid = fpart.octopart_uid
                fpart_reference.updated = None
                fpart_reference.save() 
                fpart.references.set([fpart_reference])

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0054_partreference'),
    ]

    operations = [
        migrations.RunPython(migrate_references)
    ]