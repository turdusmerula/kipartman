from frames.ask_create_parameter_dialog import AskCreateParameterDialog
import api.data.manufacturer
import api.data.parameter
import api.data.parameter_alias
from helper.exception import print_stack
import wx
import helper.unit

def provider_part_to_model_part(parent_frame, provider_part, model_part):
    model_part.name = provider_part.name
    model_part.description = provider_part.description
    
    if provider_part.manufacturer is not None:
        _import_manufacturer(provider_part, model_part)
    
    if provider_part.parameters is not None:
        _import_parameters(parent_frame, provider_part, model_part)
    
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
            print("+++", parameter)

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
#     def addReferenceFromOctopart(self, octopart):
#         octopart_extractor = OctopartExtractor(octopart)
# 
#         reference = octopart_extractor.ExtractReference()
#         if octopart_extractor.has_error():
#             wx.MessageDialog(self, octopart_extractor.get_error_message(), "Octopart processing error", wx.OK | wx.ICON_WARNING)
# 
#         # add references in current part
#         if self.part.references is None:
#             self.part.references = []
#         part_reference =  next((p for p in self.part.references if p.type==reference['type'] and p.uid==reference['uid']), None)
#         if part_reference is None:
#             part_reference = rest.model.PartReference()
#             self.part.references.append(part_reference)
#         part_reference.type = reference['type']
#         part_reference.name = reference['name']
#         part_reference.uid = reference['uid']
#         part_reference.manufacturer = reference['manufacturer']
#         part_reference.description = reference['description']
#          
#     def addParametersFromOctopart(self, octopart):
#         octopart_extractor = OctopartExtractor(octopart)
# 
#         if self.part.parameters is None:
#             self.part.parameters = []
# 
#         # import parameters
#         for spec_name in octopart.item().specs():
#             parameter = octopart_extractor.ExtractParameter(spec_name)            
#             
#             part_parameter = next((p for p in self.part.parameters if p.name==spec_name), None)
#             if part_parameter is None:
#                 part_parameter = rest.model.PartParameter()
#                 self.part.parameters.append(part_parameter)
#             part_parameter.name = parameter['name']
#             part_parameter.description = parameter['description']
#             
#             part_parameter.unit = None
#             if parameter['unit']:
#                 units = []
#                 try:
#                     units = rest.api.find_units(symbol=parameter['unit']['symbol'])
#                 except Exception as e:
#                     print_stack()
#                     wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
#                 unit = None
#                 if len(units)==0:
#                     res = wx.MessageBox("Unit symbol '%s' does not exists, create it?" % (parameter['unit']['symbol']), 'Warning', wx.YES_NO | wx.ICON_QUESTION) 
#                     if res==wx.YES:
#                         try:
#                             unit = rest.model.Unit()
#                             unit.name = parameter['unit']['name']
#                             unit.symbol = parameter['unit']['symbol']
#                             unit = rest.api.add_unit(unit)
#                         except:
#                             print_stack()
#                             wx.MessageBox('%s: error creating unit' % (parameter['unit']['name']), 'Warning', wx.OK | wx.ICON_ERROR)
#                 else:
#                     unit = units[0]
#                 part_parameter.unit = unit        
#             
#             part_parameter.numeric = True
#             if (parameter['min_value'] and parameter['min_value']['numeric']==False) or \
#                 (parameter['nom_value'] and parameter['nom_value']['numeric']==False) or \
#                 (parameter['max_value'] and parameter['max_value']['numeric']==False):
#                 part_parameter.numeric = False
#             
#             part_parameter.min_prefix = None
#             part_parameter.nom_prefix = None
#             part_parameter.max_prefix = None
#             part_parameter.min_value = None            
#             part_parameter.nom_value = None            
#             part_parameter.max_value = None
#             part_parameter.text_value = None   
#             if part_parameter.numeric:
#                 if parameter['min_value']:
#                     part_parameter.min_prefix = None # TODO
#                     part_parameter.min_value = parameter['min_value']['value']
#                 if parameter['nom_value']:
#                     part_parameter.nom_value = None # TODO
#                     part_parameter.nom_value = parameter['nom_value']['value']
#                 if parameter['max_value']:
#                     part_parameter.max_value = None # TODO
#                     part_parameter.max_value = parameter['max_value']['value']
#                 part_parameter.text_value = parameter['display_value']   
#             else:
#                 if parameter['nom_value']:
#                     part_parameter.text_value = parameter['nom_value']['value']
#                 else:
#                     part_parameter.text_value = parameter['display_value']   
#             
#     def addDistributorsFromOctopart(self, octopart):
#         octopart_extractor = OctopartExtractor(octopart)
# 
#         if self.part.distributors is None:
#             self.part.distributors = []
# 
#         octopart_distributors = octopart_extractor.ExtractDistributors()
#         for distributor_name in octopart_distributors:
#             part_distributor = next((p for p in self.part.distributors if p.name==distributor_name), None)
#             if part_distributor is None:
#                 try:
#                     distributors = rest.api.find_distributors(name=distributor_name)
#                     if len(distributors)>0:
#                         distributor = distributors[0]
#                     else:
#                         # distributor does not exists, create it
#                         new_distributor = rest.model.DistributorNew()
#                         new_distributor.name = distributor_name
#                         new_distributor.website = octopart_distributors[distributor_name]['website']
#                         new_distributor.allowed = True
#                         new_distributor = rest.api.add_distributor(new_distributor)
#                 except Exception as e:
#                     print_stack()
#                     wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
#                 
#                 part_distributor = rest.model.PartDistributor()
#                 part_distributor.name = distributor_name
#                 part_distributor.offers = []
#                 self.part.distributors.append(part_distributor)
#             
#             for offer in octopart_distributors[distributor_name]['offers']:
#                 part_offer = next((p for p in part_distributor.offers if p.sku==offer['sku'] and p.quantity==offer['quantity'] and p.packaging_unit==offer['packaging_unit']), None)
#                 if part_offer is None:
#                     part_offer = rest.model.PartOffer()
#                     part_distributor.offers.append(part_offer)
#                 part_offer.packaging_unit = offer['packaging_unit']
#                 part_offer.quantity = offer['quantity']
#                 part_offer.min_order_quantity = offer['min_order_quantity']
#                 part_offer.unit_price = offer['unit_price']
#                 part_offer.available_stock = offer['available_stock']
#                 part_offer.packaging = offer['packaging']
#                 part_offer.currency = offer['currency']
#                 part_offer.sku = offer['sku']
#                 part_offer.updated = offer['updated']
#          
#         # Cleanup old offers
#         for distributor in self.part.distributors:
#             offers_to_remove = []
#             for offer in distributor.offers:
#                 utc = pytz.UTC
#                 try:
#                     if offer.updated<utc.localize(datetime.datetime.now()-datetime.timedelta(days=30)):
#                         offers_to_remove.append(offer)
#                 except:
#                     offers_to_remove.append(offer)
#             for offer in offers_to_remove:
#                 distributor.offers.remove(offer)
# 
#         distributors_to_remove = []
#         for distributor in self.part.distributors:
#             if len(distributor.offers)==0:
#                 distributors_to_remove.append(distributor)
#         for distributor in distributors_to_remove:
#             self.part.distributors.remove(distributor)
#     
#     def addManufacturerFromOctopart(self, octopart):
#         octopart_extractor = OctopartExtractor(octopart)
# 
#         reference = octopart_extractor.ExtractReference()
#         manufacturer_name = reference['manufacturer']
#         
#         manufacturer = None 
#         try:
#             manufacturers = rest.api.find_manufacturers(name=manufacturer_name)
#             if len(manufacturers)>0:
#                 manufacturer = manufacturers[0]
#         except:
#             print_stack()
#             wx.MessageBox('%s: error retrieving manufacturer' % (manufacturer_name), 'Warning', wx.OK | wx.ICON_EXCLAMATION)
#         if manufacturer is None:
#             res = wx.MessageBox("Manufacturer '%s' does not exists, create it?" % (manufacturer_name), 'Warning', wx.YES_NO | wx.ICON_QUESTION) 
#             if res==wx.YES:
#                 try:
#                     manufacturer = rest.model.ManufacturerNew()
#                     manufacturer.name = manufacturer_name
#                     manufacturer.website = octopart.item().manufacturer().homepage_url()
#                     manufacturer = rest.api.add_manufacturer(manufacturer)
#                 except:
#                     manufacturer = None
#                     print_stack()
#                     wx.MessageBox('%s: error creating manufacturer' % (manufacturer_name), 'Warning', wx.OK | wx.ICON_ERROR)
#         if manufacturer:
#             if self.part.manufacturers is None:
#                 self.part.manufacturers = []
# 
#             part_manufacturer = next((p for p in self.part.manufacturers if p.name==manufacturer_name), None)
#             if part_manufacturer is None:
#                 part_manufacturer = rest.model.PartManufacturer()
#                 self.part.manufacturers.append(part_manufacturer)
#             part_manufacturer.name = manufacturer.name
#             part_manufacturer.part_name = manufacturer_name
#     
#     def onSelectOctopartFrameOk(self, event):
#         octoparts = event.data
#         if not octoparts:
#             return
# 
#         import_choice = wx.MultiChoiceDialog(self, "Items to import", "Octopart", 
#             ["Parameters", 
#              "Distributors and prices",
#              "Attachements",
#              "Manufacturers"])
#         import_choice.SetSelections([0, 1, 2, 3])
#         if import_choice.ShowModal()!=wx.ID_OK:
#             return
#         choices = import_choice.GetSelections()
#         
#         octopart_parts = []
#         for octopart in octoparts:
#             # convert octopart to part
#             log.debug("octopart:", octopart.json)
#             
#             # update reference
#             self.addReferenceFromOctopart(octopart)
#             
#             if 0 in choices:
#                 self.addParametersFromOctopart(octopart)
#                 
#             if 1 in choices:
#                 self.addDistributorsFromOctopart(octopart)
# 
#             if 3 in choices:
#                 # update manufacturer
#                 self.addManufacturerFromOctopart(octopart)
# 
#         # update part
#         if len(self.part.references)==1:
#             self.part.name = self.part.references[0].name
#             self.part.description = self.part.references[0].description
#         else:
#             self.part.name = self.edit_part_name.Value
#             self.part.description = self.edit_part_description.Value
#             
#         self.SetPart(self.part)

