from providers.provider import Provider, Part, Parameter, Offer, Price
import urllib.request
import urllib.parse
import json
import cfscrape
from bs4 import BeautifulSoup
import re

baseurl = "https://octopart.com"

scraper = cfscrape.create_scraper()

def convert_int(value):
    value = value.replace(",", "")
    return int(value)

class OctopartProvider(Provider):
    name = "Octopart"
        
    # capabilities
    has_search_part = True
    
    def __init__(self):
        super(OctopartProvider, self).__init__()
            
    def CheckConnection(self):
        pass
    
    def SearchPart(self, text):
        req = f"{baseurl}/search?q={text}&currency=EUR&specs=1"
        content = scraper.get(req).content
        soup = BeautifulSoup(content)

#         print(soup.prettify())
        parts = []
        
        dom_parts = soup.findAll("div", {"class": re.compile(".* part")})
        for dom_part in dom_parts:
#             print("----")
#             print(dom_part.prettify())
            part = OctopartPart(dom_part)
            parts.append(part)
        
        print(parts)
        for part in parts:
            print("---")
            print("name:", part.name)
            print("description:", part.description)
            print("manufacturer:", part.manufacturer)
            print("parameters:")
            for parameter in part.parameters:
                print(f"\t{parameter.name}:", parameter.value)
            print("offers:")
            for offer in part.offers:
                print(f"\t{offer.distributor}:")
                print(f"\t\tsku:", offer.sku)
                print(f"\t\tstock:", offer.stock)
                print(f"\t\tcurrency:", offer.currency)
                print(f"\t\tprices:")
                for price in offer.prices:
                    print(f"\t\t\tquantity:", price.quantity)
                    print(f"\t\t\tprice_per_item:", price.price_per_item)
                    
        return parts

class OctopartPart(Part):
    def __init__(self, _data):
        super(OctopartPart, self).__init__(_data)
        self._part_data = None
        self._part_offers = None
    
    def _load_part_data(self):
        if self._part_data is not None:
            return
        dom_middle = self._data.find("div", {"class": re.compile(".* middle")})
        dom_url = dom_middle.find("a")
        url = dom_url.attrs["href"]
        
        req = f"{baseurl}{url}"
        content = scraper.get(req).content
        self._part_data = BeautifulSoup(content)
        
    def _load_part_offers(self):
        self._load_part_data()
        
        if self._part_offers is not None:
            return
        dom_offers_tables = self._part_data.find("div", {"class": re.compile(".* offers-tables$")})
        if dom_offers_tables is not None:
            dom_url = dom_offers_tables.find("a")
            url = dom_url.attrs["href"]
            
            req = f"{baseurl}{url}"
            content = scraper.get(req).content
            self._part_offers = BeautifulSoup(content)
        else:
            self._part_offers = BeautifulSoup("")

    @property
    def name(self):
        dom_name = self._data.find("div", {"class": re.compile(".* mpn")})
        return dom_name.text.strip()

    @property
    def description(self):
        dom_description = self._data.find("div", {"class": re.compile(".* description")})
        return dom_description.text.strip()

    @property
    def manufacturer(self):
        dom_manufacturer = self._data.find("div", {"class": re.compile(".* manufacturer-name")})
        return dom_manufacturer.text.strip()

    @property
    def parameters(self):
        self._load_part_data()
        
        parameters = []
        dom_pdp = self._part_data.find("div", {"class": re.compile(".* pdp-section$")})
        dom_params = dom_pdp.findAll("tr")
        for dom_param in dom_params:
            dom_cols = dom_param.findAll("td")
            if len(dom_cols)==2:
                parameters.append(OctopartParameter(dom_param))
        
        return parameters

    @property
    def offers(self):
        self._load_part_offers()

        offers = []
        dom_offers_table = self._part_offers.find("table", {"class": re.compile("pdp-all-breaks-table$")})
        if dom_offers_table is not None:
#         print(dom_offers_table.prettify())
            quantities = []
            dom_offers_table_thead = dom_offers_table.find("thead")
            dom_offers_table_thead_quantities = dom_offers_table_thead.findAll("th", {"class": ["pdp-sort"]})
            for dom_offers_table_thead_quantity in dom_offers_table_thead_quantities:
                if len(dom_offers_table_thead_quantity.attrs['class'])==1:
                    quantities.append(convert_int(dom_offers_table_thead_quantity.text.strip()))
    #         print(dom_offers_table.prettify())
    
            dom_offers_table_tbody = dom_offers_table.find("tbody")
            dom_offers_table_tbody_offers = dom_offers_table_tbody.findAll("tr")
            for dom_offers_table_tbody_offer in dom_offers_table_tbody_offers:
                offer = OctopartOffer(dom_offers_table_tbody_offer, quantities)
                if len(offer.prices)>0:
                    offers.append(offer)
        
        return offers

class OctopartParameter(Parameter):
    def __init__(self, _data):
        super(OctopartParameter, self).__init__(_data)

    @property
    def name(self):
        dom_cols = self._data.findAll("td")
        return dom_cols[0].text.strip()
    
    @property
    def value(self):
        dom_cols = self._data.findAll("td")
        return dom_cols[1].text.strip()

class OctopartOffer(Offer):
    def __init__(self, _data, quantities):
        super(OctopartOffer, self).__init__(_data)
        self.quantities = quantities
        
    @property
    def distributor(self):
        dom_distributor = self._data.find("td", {"class": "col-seller"})
        return dom_distributor.text.strip()

    @property
    def sku(self):
        dom_sku = self._data.find("td", {"class": "col-sku"})
        return dom_sku.text.strip()
    
    @property
    def stock(self):
        dom_stock = self._data.find("td", {"class": "col-avail"})
        return convert_int(dom_stock.text.strip())

    @property
    def currency(self):
        dom_currency = self._data.find("td", {"class": "col-curr"})
        return dom_currency.text.strip()

    @property
    def prices(self):
        prices = []
        dom_prices = self._data.findAll("td")
        quantity_index = 0
        for dom_price in dom_prices:
#             print(dom_price.prettify())
            if 'class' not in dom_price.attrs:
                quantity_index += 1
            elif 'pdp-all-breaks-price-cell' in dom_price.attrs['class']:
                prices.append(OctopartPrice(dom_price, self.quantities[quantity_index]))
                quantity_index += 1
            elif 'pdp-all-breaks-span-cell' in dom_price.attrs['class']:
                quantity_index += 1
        
        return prices

class OctopartPrice(Price):
    def __init__(self, _data, quantity):
        super(OctopartPrice, self).__init__(_data)
        self._quantity = quantity
        
    @property
    def quantity(self):
        return self._quantity

    @property
    def price_per_item(self):
        return float(self._data.text.strip())
