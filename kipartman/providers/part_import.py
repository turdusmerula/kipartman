from frames.ask_create_parameter_dialog import AskCreateParameterDialog
import api.data.manufacturer
import api.data.parameter
import api.data.parameter_alias
import api.data.part_reference
from helper.exception import print_stack
import wx
import helper.unit

def provider_part_to_model_part(parent_frame, provider_part, model_part):
    model_part.name = provider_part.name
    model_part.description = provider_part.description
    
    if provider_part.manufacturer is not None:
        _import_manufacturer(parent_frame, provider_part, model_part)
    
    if provider_part.parameters is not None:
        _import_parameters(parent_frame, provider_part, model_part)
    
    if provider_part.offers is not None:
        _import_offers(parent_frame, provider_part, model_part)

    
    _import_reference(parent_frame, provider_part, model_part)
    
    return model_part

def _import_manufacturer(parent_frame, provider_part, model_part):
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
    
    
        part_manufacturer = next((p for p in model_part.manufacturers.all() if p.manufacturer.name==provider_manufacturer), None)
        part_manufacturer = next((p for p in model_part.manufacturers.add_pendings() if p.manufacturer.name==provider_manufacturer), part_manufacturer)

        if part_manufacturer is None:
            part_manufacturer = api.data.part_manufacturer.create(part=model_part, manufacturer=manufacturer, part_name=provider_part.name)
            model_part.manufacturers.add_pending(part_manufacturer)

def _import_parameters(parent_frame, provider_part, model_part):
    for provider_parameter in provider_part.parameters:
        parameters = api.data.parameter.find([api.data.parameter.FilterName(provider_parameter.name)])
        paramaters_alias = api.data.parameter_alias.find([api.data.parameter_alias.FilterName(provider_parameter.name)])
        if len(parameters)==0 and len(paramaters_alias)==0:
            dialog = AskCreateParameterDialog(parent_frame, provider_parameter)
            if dialog.ShowModal()==wx.ID_OK:
                parameter = dialog.parameter
        elif len(parameters)>0:
            parameter = parameters[0]
        elif len(paramaters_alias)>0:
            parameter = paramaters_alias[0].parameter

        if parameter is not None:
            part_parameter = next((part_parameter for part_parameter in model_part.parameters.all() if part_parameter.parameter.id==parameter.id), None)
            part_parameter = next((part_parameter for part_parameter in model_part.parameters.pendings() if part_parameter.parameter.id==parameter.id), part_parameter)
            if part_parameter is None:
                part_parameter = api.data.part_parameter.create(part=model_part, parameter=parameter)
            
            error = False
            if parameter.value_type==api.models.ParameterType.TEXT:
                part_parameter.text_value = provider_parameter.value
                part_parameter.value = None
                part_parameter.prefix = None
            else:
                num, prefix, unit = helper.unit.cut_unit_value(provider_parameter.value)
                if (unit!="" and parameter.unit is None) or (unit=="" and parameter.unit is not None) or (unit!="" and parameter.unit is not None and parameter.unit.symbol!=unit):
                    wx.MessageBox(f"Import '{provider_parameter.name}' with value '{provider_parameter.value}' failed, unit mismatch", 'Error', wx.OK | wx.ICON_ERROR)
                    error = True
                if prefix!="" and parameter.unit is not None and parameter.unit.prefixable==False:
                    wx.MessageBox(f"Import '{provider_parameter.name}' with value '{provider_parameter.value}' failed, unit cannot be prefixed", 'Error', wx.OK | wx.ICON_ERROR)
                    error = True
                
                prefix_power = 1.
                if prefix is not None:
                    found_prefix = api.data.unit_prefix.find([api.data.unit_prefix.FilterSymbol(prefix)])
                    if len(found_prefix)==0:
                        wx.MessageBox(f"Import '{provider_parameter.name}' with value '{provider_parameter.value}' failed, invalid prefix '{prefix}'", 'Error saving parameter', wx.OK | wx.ICON_ERROR)
                        error = True
                    else:
                        prefix_power = float(found_prefix[0].power)
                        part_parameter.prefix = found_prefix[0]

                if parameter.value_type==api.models.ParameterType.INTEGER:
                    try:
                        part_parameter.value = int(float(num)*prefix_power)
                    except Exception as e:
                        print_stack()
                        wx.MessageBox(f"Import '{provider_parameter.name}' with value '{provider_parameter.value}' failed, invalid integer value '{num}'", 'Error saving parameter', wx.OK | wx.ICON_ERROR)
                        error = True
                else:
                    try:
                        part_parameter.value = float(num)*prefix_power
                    except Exception as e:
                        print_stack()
                        wx.MessageBox(f"Import '{provider_parameter.name}' with value '{provider_parameter.value}' failed, invalid float value '{num}'", 'Error saving parameter', wx.OK | wx.ICON_ERROR)
                        error = True
                
        
            if error==False:
                model_part.parameters.add_pending(part_parameter)


def _import_offers(parent_frame, provider_part, model_part):
    for provider_offer in provider_part.offers:
        distributors = api.data.distributor.find([api.data.distributor.FilterSearchDistributor(provider_offer.distributor)])
        if len(distributors)==0:
            res = wx.MessageBox(f"distributor '{provider_offer.distributor}' does not exists, create it?", 'Warning', wx.YES_NO | wx.ICON_QUESTION) 
            if res==wx.YES:
                try:
                    distributor = api.data.distributor.create(name=provider_offer.distributor)
                    api.data.distributor.save(distributor)
                except:
                    distributor = None
                    print_stack()
                    wx.MessageBox(f'{provider_offer.distributor}: error creating manufacturer', 'Warning', wx.OK | wx.ICON_ERROR)
        else:
            distributor = distributors[0]
    
        if distributor:
            for provider_price in provider_offer.prices:
                
                model_offers = model_part.offers.all()
                if model_part.offers is None:
                    model_part.offers = []
        
                part_offer = next((o for o in model_part.offers.all() if o.distributor.id==distributor.id and o.quantity==provider_price.quantity), None)
                part_offer = next((o for o in model_part.offers.pendings() if o.distributor.id==distributor.id and o.quantity==provider_price.quantity), part_offer)
    
                if part_offer is None:
                    part_offer = api.data.part_offer.create(part=model_part, distributor=distributor)

                part_offer.packaging_unit =  min(provider_offer.prices, key=lambda price: price.quantity).quantity
                part_offer.quantity = provider_price.quantity
                part_offer.available_stock = provider_offer.stock
                part_offer.unit_price = provider_price.price_per_item
                part_offer.currency = provider_offer.currency
                part_offer.sku = provider_offer.sku
                
                model_part.offers.add_pending(part_offer)
                
def _import_reference(parent_frame, provider_part, model_part):
    part_reference = next((r for r in model_part.references.all() if r.type==provider_part.provider.name and r.name==provider_part.name), None)
    part_reference = next((r for r in model_part.references.pendings() if r.type==provider_part.provider.name and r.name==provider_part.name), part_reference)

    if part_reference is None:
        part_reference = api.data.part_reference.create(part=model_part)
    
    part_reference.type = provider_part.provider.name
    part_reference.manufacturer = provider_part.manufacturer
    part_reference.name = provider_part.name
    part_reference.description = provider_part.description
    part_reference.uid = provider_part.uid
    
    model_part.references.add_pending(part_reference)
    
    