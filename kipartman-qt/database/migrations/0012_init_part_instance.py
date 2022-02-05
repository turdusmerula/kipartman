from django.db import migrations, models
import django.utils.timezone

def set_part_instance(apps, schema_editor):
    Part = apps.get_model("database", "Part")
    
    parts = Part.objects.all()
    for part in parts:
        if part.metapart==True:
            part.instance = 'metapart'
        else:
            part.instance = 'part'
        part.save()
        
class Migration(migrations.Migration):
                
    dependencies = [
        ('database', '0011_part_instance_alter_partparameter_operator'),
    ]

    operations = [
        migrations.RunPython(set_part_instance)
    ]
