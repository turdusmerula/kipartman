import os, sys
import yaml

# os.sys.path.append(os.path.dirname(os.path.abspath(__file__)))
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
xpl_path = os.path.abspath(os.path.dirname(__file__))
os.chdir(base_path)
sys.path.append(base_path)

from api.log import log
from api.ndict import ndict
from api.unit import QuantityRange, Quantity, ureg
from api.octopart.queries import OctopartPartQuery

os.environ['DJANGO_SETTINGS_MODULE'] = "database.config.settings"
import django
django.setup()
from database.models import Parameter, ParameterType

log.setLevel('DEBUG')

query = OctopartPartQuery()
attributes = {}

def save_attribute(attribute):
    name = attribute.attribute.name
    value = attribute.display_value
    
    if name in attributes:
        if attributes[name].display_values is None:
            attributes[name].display_values = []
        if value not in attributes[name].display_values:
            attributes[name].display_values.append(value)
    print(f"add: {name}={value}", attribute)

def query_attribute(attribute, value):
    res = False
    req = ndict(query.Search(filters={attribute.shortname: value}))
    if req is not None:
        for part in req.search.results or {}:
            res = True
            for spec in part.part.specs:
                save_attribute(spec)
    return res

def main(args=None):
    global query
    global attributes
    
    log.info("export attributes")
    
    try:
        with open(os.path.join(xpl_path, "../attributes.yaml"), "r") as f:
            attributes = ndict(yaml.safe_load(f))
    except Exception as e:
        pass
    
    # get attributes from octopart
    attrs = ndict(query.Attributes())
    for attr in attrs:
        # add new attributes to list
        if attr.name not in attributes:
            attributes[attr.name] = attr

    for name, attribute in attributes.items():
        # print(f"+ {attribute}")
        if attribute.display_values is None:
            # print(f"-> {name}")
            req = query_attribute(attribute, QuantityRange(-1000, 1000))
            if req is None:
                i = 0
                while req is None and i<10:
                    req = query_attribute(attribute, Quantity(i))
                    i += 1 
                    
            print(req)

    # # guess attribute type
    # for name, attribute in attributes.items():
    #     if len(attribute.display_values or [])==0:
    #         print(f"{name} / {attribute.shortname}: no value")

    with open(os.path.join(xpl_path, "../attributes.yaml"), "w") as f:
        f.write(yaml.safe_dump(attributes))
    
    print("---")
    print("Synchronize database")
    # synchronize database
    for name, attribute in attributes.items():
        if attribute.value_type is not None:
            add = True
            parameter = Parameter.objects.filter(name=name).first()
            if parameter is None:
                parameter = Parameter()
                parameter.name = name
                parameter.show = True
            
            if attribute.value_type=='float':
                parameter.value_type = ParameterType.FLOAT
            elif attribute.value_type=='int':
                parameter.value_type = ParameterType.INTEGER
            elif attribute.value_type=='text':
                parameter.value_type = ParameterType.TEXT
            
            if attribute.unit is not None:
                try:
                    # a = ureg.parse_units(attribute.unit)
                    # unit = Quantity(attribute.unit, base_unit=attribute.unit).unit
                    parameter.unit = str(ureg.parse_units(attribute.unit)).replace("Δ", "")
                except Exception as e:
                    print(f"{name} / {attribute.shortname}: {e}")
                    add = False
            
            if add==True:
                parameter.save()
        else:
            print(f"{name} / {attribute.shortname}: no value")
        
if __name__ == "__main__":
    main()

