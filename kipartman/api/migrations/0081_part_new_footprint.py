# Generated by Django 3.1 on 2020-09-22 09:29

from django.db import migrations, models
import django.db.models.deletion
import os
import re

def migrate_footprints(apps, schema_editor):
    Part = apps.get_model("api", "Part")
    KicadFootprint = apps.get_model("api", "KicadFootprint")
    KicadFootprintLibrary = apps.get_model("api", "KicadFootprintLibrary")
    
    for part in Part.objects.all():
        print("-", part.name)
        if part.footprint is not None:
#             if part.symbol.source_path
            footprint = None
            library_path = os.path.dirname(part.footprint.source_path)
            library = None
            footprint_name = re.sub(r".*/(.*)\.kicad_mod$", r"\1", part.footprint.source_path)
            
            for lf in KicadFootprintLibrary.objects.all():
                if lf.path==library_path:
                    library = lf
                    break 
            if library is None:
                print(f"no match found for library {library_path}")
            
            for s in KicadFootprint.objects.all():
                if footprint_name==s.name:
                    footprint = s
                    break
            if footprint is None:
                print(f"no match found for footprint {footprint_name}")
            part.new_footprint = footprint
            part.save()

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0080_auto_20200921_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='new_footprint',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='new_footprint', to='api.kicadfootprint'),
        ),
        migrations.RunPython(migrate_footprints)
    ]