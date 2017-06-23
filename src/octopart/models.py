
class Model(object):
    def __init__(self, json):
        self.json = json
        
class SearchRequest(Model):
    pass

class SearchResponse(Model):
    pass

class SearchResult(Model):
    def snippet(self):
        return self.json['snippet']

    def item(self):
        return Part(self.json['item'])

class Part(Model):
    def compliance_documents(self):
        list = []
        for compliance_document in self.json['compliance_document']:
            list.append(ComplianceDocument(compliance_document))
        return list

    def uid(self):
        return self.json['uid']

    def mpn(self):
        return self.json['mpn']
    
    def brand(self):
        if self.json['brand']:
            return Brand(self.json['brand'])
        return None
    
    def datasheets(self):
        list = []
        for datasheet in self.json['datasheets']:
            list.append(Datasheet(datasheet))
        return list
    
    def descriptions(self):
        list = []
        for description in self.json['descriptions']:
            list.append(Description(description))
        return list

    def short_description(self):
        return self.json['short_description']
    
    def manufacturer(self):
        if self.json['manufacturer']:
            return Manufacturer(self.json['manufacturer'])
        return None
    
    def octopart_url(self):
        return self.json['octopart_url']
            
    def specs(self):
        list = {}
        for spec in self.json['specs']:
            list[spec] = SpecValue(self.json['specs'][spec])
        return list
    
    def imagesets(self):
        list = []
        for imageset in self.json['imagesets']:
            list.append(Imageset(imageset))
        return list

    def offers(self):
        list = []
        for offer in self.json['offers']:
            list.append(PartOffer(offer))
        return list
    
    def reference_designs(self):
        list = []
        for reference_design in self.json['reference_designs']:
            list.append(ReferenceDesign(reference_design))
        return list


class Asset(Model):
    def url(self):
        return self.json['url']

    def mimetype(self):
        return self.json['mimetype']

    def metadata(self):
        return self.json['metadata']


class Brand(Model):
    def homepage_url(self):
        return self.json['homepage_url']

    def name(self):
        return self.json['name']

    def uid(self):
        return self.json['uid']


class ComplianceDocument(Model):
    def mimetype(self):
        return self.json['mimetype']

    def attribution(self):
        if self.json['attribution']:
            return Attribution(self.json['attribution'])
        return None
    
    def url(self):
        return self.json['url']

    def subtypes(self):
        return self.json['subtypes']

    def metadata(self):
        return self.json['metadata']


class Datasheet(Model):
    def url(self):
        return self.json['url']

    def mimetype(self):
        return self.json['mimetype']

    def metadata(self):
        return self.json['metadata']
    
    def attribution(self):
        if self.json['attribution']:
            return Attribution(self.json['attribution'])
        return None

class Attribution(Model):
    def sources(self):
        list = []
        for source in self.json['sources']:
            list.append(Source(source))
        return list

    def first_acquired(self):
        return self.json['first_acquired']


class Description(Model):
    def attribution(self):
        if self.json['attribution']:
            return Attribution(self.json['attribution'])
        return None
    
    def value(self):
        return self.json['value']


class ExternalLinks(Model):
    def product_url(self):
        return self.json['product_url']

    def freesample_url(self):
        return self.json['freesample_url']

    def evalkit_url(self):
        return self.json['evalkit_url']


class Imageset(Model):
    def medium_image(self):
        if self.json['medium_image']:
            return Asset(self.json['medium_image'])
        return None
    
    def large_image(self):
        if self.json['large_image']:
            return Asset(self.json['large_image'])
        return None
    
    def credit_string(self):
        if self.json['credit_string']:
            return self.json['credit_string']
        return None
    
    def attribution(self):
        if self.json['attribution']:
            return Attribution(self.json['attribution'])
        return None
    
    def small_image(self):
        if self.json['small_image']:
            return Asset(self.json['small_image'])
        return None
    
    def swatch_image(self):
        if self.json['swatch_image']:
            return Asset(self.json['swatch_image'])
        return None
    
    def credit_url(self):
        return self.json['credit_url']


class Manufacturer(Model):
    def name(self):
        return self.json['name']

    def homepage_url(self):
        return self.json['homepage_url']

    def uid(self):
        return self.json['uid']


class PartOffer(Model):
    def sku(self):
        return self.json['sku']

    def packaging(self):
        return self.json['packaging']

    def on_order_eta(self):
        return self.json['on_order_eta']

    def last_updated(self):
        return self.json['last_updated']

    def order_multiple(self):
        return self.json['order_multiple']

    def in_stock_quantity(self):
        return self.json['in_stock_quantity']

    def eligible_region(self):
        return self.json['eligible_region']

    def moq(self):
        return self.json['moq']

    def on_order_quantity(self):
        return self.json['on_order_quantity']

    def octopart_rfq_url(self):
        return self.json['octopart_rfq_url']

    def seller(self):
        if self.json['seller']:
            return Seller(self.json['seller'])
        return None
    
    def product_url(self):
        return self.json['product_url']

    def factory_order_multiple(self):
        return self.json['factory_order_multiple']

    def _naive_id(self):
        return self.json['_naive_id']

    def factory_lead_days(self):
        return self.json['factory_lead_days']

    def prices(self):
        return self.json['prices']

    def is_authorized(self):
        return self.json['is_authorized']

    def is_realtime(self):
        return self.json['is_realtime']


class ReferenceDesign(Model):
    def mimetype(self):
        return self.json['mimetype']

    def attribution(self):
        if self.json['attribution']:
            return Attribution(self.json['attribution'])
        return None
    
    def description(self):
        return self.json['description']

    def title(self):
        return self.json['title']

    def url(self):
        return self.json['url']

    def metadata(self):
        return self.json['metadata']



class Seller(Model):
    def display_flag(self):
        return self.json['display_flag']

    def has_ecommerce(self):
        return self.json['has_ecommerce']

    def name(self):
        return self.json['name']

    def homepage_url(self):
        return self.json['homepage_url']

    def id(self):
        return self.json['id']

    def uid(self):
        return self.json['uid']


class Source(Model):
    def name(self):
        return self.json['name']

    def uid(self):
        return self.json['uid']


class SpecMetadata(Model):
    def datatype(self):
        return self.json['datatype']

    def unit(self):
        if self.json['unit']:
            return UnitOfMeasurement(self.json['unit'])
        return None
    
    def key(self):
        return self.json['key']

    def name(self):
        return self.json['name']


class SpecValue(Model):
    def attribution(self):
        if self.json['attribution']:
            return Attribution(self.json['attribution'])
        return None
    
    def max_value(self):
        return self.json['max_value']

    def min_value(self):
        return self.json['min_value']

    def value(self):
        return self.json['value']

    def display_value(self):
        if 'display_value' in self.json:
            return self.json['display_value']
        return None
    
    def metadata(self):
        if self.json['metadata']:
            return SpecMetadata(self.json['metadata'])
        return None

class UnitOfMeasurement(Model):
    def symbol(self):
        return self.json['symbol']

    def name(self):
        return self.json['name']
