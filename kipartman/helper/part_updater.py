import rest
from octopart.queries import PartsQuery
from helper.exception import print_stack
from octopart.extractor import OctopartExtractor
import wx
import os, datetime
import pytz
from helper.log import log

class PartReferenceUpdater(): 
    def __init__(self):
        pass
    
    def refresh_distributors(self, part):
        partrefs = rest.api.find_part(part.id, with_distributors=True, with_references=True)
        if partrefs.references:
            log.debug("Part:", partrefs.name, "references:", len(partrefs.references))
        else:
            log.debug("Part:", partrefs.name, "references: none")
        
        if partrefs.references:
            for reference in partrefs.references:
                q = PartsQuery()
                try:
                    q.get(reference.name)
                except Exception as e:
                    print_stack()
                    wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
                for octopart in q.results():
                    item = octopart.item()
                    if item.uid()==reference.uid:
                        self.refresh_distributors_from_octopart(part, octopart)
            
    def refresh_distributors_from_octopart(self, part, octopart):
        octopart_extractor = OctopartExtractor(octopart)

        if part.distributors is None:
            part.distributors = []

        octopart_distributors = octopart_extractor.ExtractDistributors()
        for distributor_name in octopart_distributors:
            part_distributor = next((p for p in part.distributors if p.name==distributor_name), None)
            if part_distributor is None:
                try:
                    distributors = rest.api.find_distributors(name=distributor_name)
                    if len(distributors)>0:
                        distributor = distributors[0]
                    else:
                        # distributor does not exists, create it
                        new_distributor = rest.model.DistributorNew()
                        new_distributor.name = distributor_name
                        new_distributor.website = octopart_distributors[distributor_name]['website']
                        new_distributor.allowed = True
                        new_distributor = rest.api.add_distributor(new_distributor)
                except Exception as e:
                    print_stack()
                    wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
                
                part_distributor = rest.model.PartDistributor()
                part_distributor.name = distributor_name
                part_distributor.offers = []
                part.distributors.append(part_distributor)
            
            for offer in octopart_distributors[distributor_name]['offers']:
                part_offer = next((p for p in part_distributor.offers if p.sku==offer['sku'] and p.quantity==offer['quantity'] and p.packaging_unit==offer['packaging_unit']), None)
                if part_offer is None:
                    part_offer = rest.model.PartOffer()
                    part_distributor.offers.append(part_offer)
                part_offer.packaging_unit = offer['packaging_unit']
                part_offer.quantity = offer['quantity']
                part_offer.min_order_quantity = offer['min_order_quantity']
                part_offer.unit_price = offer['unit_price']
                part_offer.available_stock = offer['available_stock']
                part_offer.packaging = offer['packaging']
                part_offer.currency = offer['currency']
                part_offer.sku = offer['sku']
                part_offer.updated = offer['updated']
         
        # Cleanup old offers
        for distributor in part.distributors:
            offers_to_remove = []
            for offer in distributor.offers:
                utc = pytz.UTC
                try:
                    if offer.updated<utc.localize(datetime.datetime.now()-datetime.timedelta(days=30)):
                        offers_to_remove.append(offer)
                except:
                    offers_to_remove.append(offer)
            for offer in offers_to_remove:
                distributor.offers.remove(offer)

        distributors_to_remove = []
        for distributor in part.distributors:
            if len(distributor.offers)==0:
                distributors_to_remove.append(distributor)
        for distributor in distributors_to_remove:
            part.distributors.remove(distributor)
