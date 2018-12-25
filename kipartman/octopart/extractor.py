import rest 
import wx
import re
from helper.exception import print_stack
import datetime
import dateutil.parser
import pytz

class OctopartExtractorError(BaseException):
    def __init__(self, error):
        self.error = error

class OctopartExtractor(object):
    
    def __init__(self, octopart):
        self.octopart = octopart 
        self.errors = []
    
    def has_error(self):
        if len(self.errors)>0:
            return True
        return False
    
    def get_error_message(self):
        message = None
        for error in self.errors:
            if message is None:
                message = ""
            else:
                message = message+"\n"+error
        self.errors.clear()
        return message
         
    def GetUnitPrefix(self, spec):
        symbol = self.GetUnitPrefixSymbol(spec)
        if symbol=='' or symbol is None:
            return None
        return symbol
        
    def GetUnitSymbol(self, spec):
        if spec.metadata().unit():
            return spec.metadata().unit().symbol()
        return ""

    def GetUnitPrefixSymbol(self, spec):
        if spec.display_value() is None:
            return ""
        display_value = spec.display_value().split(" ")
        unit = self.GetUnitSymbol(spec)
        if len(display_value)<2:
            return ""   # there is only a value, no unit
        display_unit = display_value[1]
        # filter non alpha chars
        display_unit = re.sub('[ ,.;]', '', display_unit)
        prefix = display_unit[:-len(unit)]
        return prefix
    
#     def GetPrefixedValue(self, value, prefix):
#         if prefix is None:
#             return float(value)
#         return float(value)/float(prefix.power)

    def ExtractParameter(self, spec_name):
        spec = self.octopart.item().specs()[spec_name]

        parameter = {
            'name': spec_name,
            'description': spec.metadata().name(),
            'unit': None,
            'display_value': '',
            'min_value': None,
            'nom_value': None,
            'max_value': None
        }
                
        if spec.metadata().unit():
            parameter['unit'] = {
                'unit': spec.metadata().unit().symbol(),
                'prefix': self.GetUnitPrefix(spec)
            }
        
        parameter['display_value'] = spec.display_value()
        
        if spec.value() and len(spec.value())>0:
            try:
                parameter['nom_value'] = {
                    'value': float(spec.value()[0]),
                    'numeric': True
                }
            except Exception as e:
                parameter['nom_value'] = {
                    'value': spec.value()[0],
                    'numeric': True
                }

        if spec.min_value() and len(spec.min_value())>0:
            try:
                parameter['min_value'] = {
                    'value': float(spec.min_value()[0]),
                    'numeric': True
                }
            except Exception as e:
                parameter['min_value'] = {
                    'value': spec.min_value()[0],
                    'numeric': True
                }

        if spec.max_value() and len(spec.max_value())>0:
            try:
                parameter['min_value'] = {
                    'value': float(spec.max_value()[0]),
                    'numeric': True
                }
            except Exception as e:
                parameter['min_value'] = {
                    'value': spec.max_value()[0],
                    'numeric': True
                }

        return parameter
    
    def ExtractParameters(self):
        parameters = []
        # import parameters
        for spec_name in self.octopart.item().specs():
            parameter = self.ExtractParameter(spec_name)            
            parameters.append(parameter)
        
        return parameters

    def ExtractDistributors(self):
        # import distributors
        part_distributors = {}
        for offer in self.octopart.item().offers():
            distributor_name = offer.seller().name()
            if distributor_name not in part_distributors:
                part_distributors[distributor_name] = {
                    'name': distributor_name,
                    'website': offer.seller().homepage_url(),
                    'offers': []
                }
            
            for price_name in offer.prices():
                correct_quantity = False   # correct a bug with, sometimes quantity is given for on packaging unit and not total quantity amount 
                for quantity in offer.prices()[price_name]:
                    part_offer = { 
                        'distributor': distributor_name,
                        'currency': price_name,
                        'packaging_unit': 1,
                        'min_order_quantity': None,
                        'quantity': None,
                        'unit_price': None,
                        'available_stock': None,
                        'packaging': None,
                        'updated': None,
                        'sku': None,
                    }
                        
                    if offer.order_multiple() is not None:
                        part_offer['packaging_unit'] = offer.order_multiple()
                    elif offer.multipack_quantity() is not None:
                        try:
                            part_offer['packaging_unit'] = int(offer.multipack_quantity())
                        except Exception as e:
                            print_stack()
                            self.errors.append(format(e))
                        
                    if offer.moq() is not None:
                        part_offer['min_order_quantity'] = offer.moq()
                    else:
                        part_offer['min_order_quantity'] = 1
                    
                    part_offer['quantity'] = quantity[0]
                    try:
                        part_offer['unit_price'] = float(quantity[1])
                    except Exception as e:
                        print_stack()
                        self.errors.append(format(e))
                    
                    if ( correct_quantity==False and part_offer['quantity']<part_offer['packaging_unit'] ) or correct_quantity==True:
                        part_offer['quantity'] = part_offer['quantity']*part_offer['packaging_unit']
                        part_offer['min_order_quantity'] = part_offer['packaging_unit']
                        part_offer['unit_price'] = part_offer['unit_price']/part_offer['quantity']
                        correct_quantity = True
                        
                    if offer.in_stock_quantity() is not None:
                        part_offer['available_stock'] = offer.in_stock_quantity()
                    if offer.packaging() is not None:
                        part_offer['packaging'] = offer.packaging()
                    
                    try:
                        # extract date from string
                        updated = dateutil.parser.parse(offer.last_updated())
                    except:
                        # if failed set now
                        updated = datetime.datetime.now()
                        print_stack()
                        self.errors.append(format(e)) 
                    try:
                        # switch to UTC
                        utc = pytz.UTC
                        part_offer['updated'] = utc.localize(updated)
                    except Exception as e:
                        part_offer['updated'] = updated
                    
                    part_offer['sku'] = offer.sku()
                    part_distributors[distributor_name]['offers'].append(part_offer)

        return part_distributors
        
    def ExtractReference(self):
        return {'type': 'octopart', 
                'name': self.octopart.item().mpn(), 
                'manufacturer': self.octopart.item().manufacturer().name(),
                'uid': self.octopart.item().uid(),
                'description': self.octopart.snippet()}
