from django.db import migrations, models
import django.utils.timezone

def create_params(apps, schema_editor):
    PartParameter = apps.get_model("api", "PartParameter")
    Parameter = apps.get_model("api", "Parameter")
    
    part_parameters = PartParameter.objects.all()
    for part_parameter in part_parameters:
        try:
            parameter = Parameter.objects.get(name=part_parameter.name)
        except:
            parameter = None
            
        if parameter is None:
            print(f"creating {part_parameter.name}")
            parameter = Parameter()
            parameter.name = part_parameter.name
            parameter.description = part_parameter.description
            parameter.numeric = part_parameter.numeric
            parameter.unit = part_parameter.unit

        part_parameter.parameter = parameter
        
        if parameter.description!=part_parameter.description:
            print(f"Which 'description' to keep for {parameter.name}?")
            print(f"1 (default): {parameter.description}")
            print(f"2          : {part_parameter.description}")
            res = input()
            if res=="":
                res = "1"
            if res=="2":
                parameter.description = part_parameter.description
        if parameter.numeric!=part_parameter.numeric:
            print(f"Which 'numeric' to keep for {parameter.name}?")
            print(f"1 (default): {parameter.numeric}")
            print(f"2          : {part_parameter.numeric}")
            res = input()
            if res=="":
                res = "1"
            if res=="2":
                parameter.numeric = part_parameter.numeric
        if parameter.unit!=part_parameter.unit:
            print(f"Which 'unit' to keep for {parameter.name}?")
            if parameter.unit is not None:
                print(f"1 (default): {parameter.unit.name}")
            else:
                print(f"1 (default): {parameter.unit}")
            if part_parameter.unit is not None:
                print(f"2          : {part_parameter.unit.name}")
            else:
                print(f"2          : {part_parameter.unit}")
                
            res = input()
            if res=="":
                res = "1"
            if res=="2":
                parameter.unit = part_parameter.unit

        parameter.save()
        part_parameter.save()
        
class Migration(migrations.Migration):
                
    dependencies = [
        ('api', '0065_auto_20200903_1825'),
    ]

    operations = [
        migrations.RunPython(create_params)
    ]
