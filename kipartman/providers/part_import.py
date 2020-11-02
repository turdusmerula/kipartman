import api.data.manufacturer
from helper.exception import print_stack
import wx

def provider_part_to_model_part(provider_part, model_part):
    model_part.name = provider_part.name
    model_part.description = provider_part.description
    
    if provider_part.manufacturer is not None:
        manufacturer = _import_manufacturer(provider_part.manufacturer, model_part)
    
    if provider_part.parameters is not None:
        pass
    
    if provider_part.offers is not None:
        pass
    
    return model_part

def _import_manufacturer(provider_part, model_part):
    provider_manufacturer = provider_part.manufacturer
    
    manufacturers = api.data.manufacturer.find([api.data.manufacturer.FilterName(provider_manufacturer)])
    if len(manufacturers)==0:
        res = wx.MessageBox(f"Manufacturer '{provider_manufacturer}' does not exists, create it?", 'Warning', wx.YES_NO | wx.ICON_QUESTION) 
        if res==wx.YES:
            try:
                manufacturer = api.data.manufacturer.create(name=provider_manufacturer)
                api.data.manufacturer.save(manufacturer)
            except:
                manufacturer = None
                print_stack()
                wx.MessageBox(f'{provider_manufacturer}: error creating manufacturer', 'Warning', wx.OK | wx.ICON_ERROR)
    else:
        manufacturer = manufacturers[0]

    if manufacturer:
        model_manufacturers = model_part.manufacturers.all()
        if model_part.manufacturers is None:
            model_part.manufacturers = []
    
    
        part_manufacturer = next((p for p in model_part.manufacturers.all() if p.part.name==provider_manufacturer), None)
        part_manufacturer = next((p for p in model_part.manufacturers.add_pendings() if p.part.name==provider_manufacturer), None)
        print("---", part_manufacturer)
        if part_manufacturer is None:
            part_manufacturer = api.data.part_manufacturer.create(part=model_part, manufacturer=manufacturer, part_name=provider_part.name)
            model_part.manufacturers.add_pending(part_manufacturer)
