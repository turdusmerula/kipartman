from providers.provider import Provider
import urllib.request
import urllib.parse
import json

# see: https://octopart.com/api/v4/getting-started


# TODO: build request from this result
# {
#   __schema {
#     types {
#       name
#       fields {
#         name
#         description
#       }
#     }
#   }
# }


# type AppliedFilter {
#   shortname: String!
#   name: String!
#   values: [String!]!
#   display_values: [String!]!
# }
# 
# type Attribute {
#   id: ID!
#   name: String!
#   shortname: String!
#   group: String!
# }
# 
# type AttributeGroup {
#   name: String!
#   attributes: [Attribute!]!
# }
# 
# type Blurb {
#   name: String!
#   path_name: String!
#   description: String!
#   content: String!
# }
# 
# type CadBucket {
#   cad_state: String!
#   count: Int
# }
# 
# type Category {
#   id: ID!
#   parent_id: ID!
#   name: String!
#   ancestors: [Category!]!
#   children: [Category!]!
#   path: String!
#   relevant_attributes: [Attribute!]!
#   blurb: Blurb
#   num_parts: Int!
# }
# 
# type CategoryBucket {
#   category: Category!
#   count: Int
# }
# 
query_company = """{
  id
  name
  aliases
  homepage_url
  slug
  is_verified
  is_broker
  is_distributorapi
}"""

# type CompanyBucket {
#   company: Company!
#   count: Int
# }
# 
query_description = """{
  text
  credit_string
  credit_url
}"""

query_spec = """{
  attribute
  display_value
}"""

# 
# type Document {
#   name: String!
#   page_count: Int
#   created_at: Time
#   url: String!
#   credit_string: String!
#   credit_url: String!
#   mime_type: String!
# }
# 
# type DocumentCollection {
#   name: String!
#   documents: [Document!]!
# }
# 
# type Image {
#   url_largest: String! @deprecated(reason: "use `url` instead")
#   url_55px: String! @deprecated(reason: "use `url` instead")
#   url_75px: String! @deprecated(reason: "use `url` instead")
#   url_90px: String! @deprecated(reason: "use `url` instead")
#   url: String!
#   credit_string: String!
#   credit_url: String!
# }
# 
# scalar Map

query_price_point = """{
  quantity
  price
  currency
  converted_price
  converted_currency
  conversion_rate
}"""

query_offer = f"""{{
  id
  sku
  inventory_level
  packaging
  moq
  prices: {query_price_point}
  click_url
  updated:
  factory_lead_days
  on_order_quantity
  factory_pack_quantity
  order_multiple
  multipack_quantity
}}"""

query_part_seller = f"""{{
  company {query_company}
  offers {query_offer}
  is_authorized
  is_broker
  is_rfq
}}"""

query_part = f"""{{
  id
  name
  mpn
  generic_mpn
  manufacturer {query_company}
  manufacturer_url
  free_sample_url
#   document_collections: [DocumentCollection!]!
  short_description
  descriptions {query_description}
#   images: [Image!]!
  specs {query_spec}
#   slug: String!
  octopart_url
#   similar_parts: [Part!]!
#   companion_products: [SponsoredPart!]!
#   category: Category
#   series: PartSeries
#   best_image: Image
#   best_datasheet: Document
#   reference_designs: [ReferenceDesign!]!
#   cad: PartCad
#   cad_request_url: String
#   v3uid: ID!
  counts
  median_price_1000 {query_price_point}
  total_avail
  avg_avail
  sellers(include_brokers: true, authorized_only: true) {query_part_seller}
  estimated_factory_lead_days
  aka_mpns
}}"""

# query_query = f"""{{
#   attributes: [Attribute!]!
#   manufacturers(ids: [String!]): [Company!]!
#   sellers(ids: [String!]): [Company!]!
#   categories(
#     ids: [String!]
#     paths: [String!]
#   ): [Category!]!
#   parts(
#     ids: [String!]!
#     country: String! = "US"
#     currency: String! = "USD"
#     distributorapi: Boolean
#     distributorapi_timeout: String! = "3s"
#   ): [Part]!
#   suggest(
#     q: String!
#     category_id: String
#   ): [Suggestion!]!
#   search(
#     q: String
#     country: String! = "US"
#     currency: String! = "USD"
#     start: Int
#     limit: Int
#     sort: String
#     sort_dir: SortDirection
#     in_stock_only: Boolean
#     filters: Map
#     distributorapi: Boolean
#     distributorapi_timeout: String! = "3s"
#   ): PartResultSet!
#   spelling_correction(q: String!): [SpellingCorrection!]!
#   multi_match(
#     queries: [PartMatchQuery!]!
#     options: PartMatchOptions
#   ): [PartMatch!]!
# }
# }}"""

# type PartCad {
#   add_to_library_url: String
#   has_3d_model: Boolean!
#   has_altium: Boolean!
#   has_eagle: Boolean!
#   has_orcad: Boolean!
#   has_kicad: Boolean!
#   download_url_altium: String!
#   download_url_eagle: String!
#   download_url_orcad: String!
#   download_url_kicad: String!
#   footprint_image_url: String
#   symbol_image_url: String
# }
# 
# type PartMatch {
#   reference: String
#   hits: Int!
#   parts: [Part!]!
#   error: String
# }
# 
# input PartMatchOptions {
#   require_authorized_sellers: Boolean = false
#   require_stock_available: Boolean = false
#   filters: Map
# }
# 
# input PartMatchQuery {
#   mpn: String
#   sku: String
#   mpn_or_sku: String
#   manufacturer: String
#   seller: String
#   start: Int! = 0
#   limit: Int! = 3
#   reference: String
# }
# 
# type PartResult {
#   _cache_id: String!
#   part: Part!
#   explain: String! @deprecated(reason: "always empty")
#   aka_mpn: String
#   description: String!
# }
# 
# type PartResultSet {
#   total: Int! @deprecated(reason: "use `hits` instead")
#   hits: Int!
#   results: [PartResult!]
#   specs_view_attribute_groups: [AttributeGroup!]!
#   warnings: [String!]
#   spec_aggs(
#     attribute_names: [String!]!
#     size: Int! = 10
#   ): [SpecAgg!]!
#   manufacturer_agg(size: Int! = 10): [CompanyBucket!]!
#   distributor_agg(size: Int! = 10): [CompanyBucket!]!
#   category_agg(size: Int! = 10): [CategoryBucket!]!
#   cad_agg: [CadBucket!]!
#   suggested_categories: [CategoryBucket!]!
#   suggested_filters: [Attribute!]!
#   all_filters: [Attribute!]!
#   applied_category: Category
#   applied_filters: [AppliedFilter!]!
# }
# 
# 
# type PartSeries {
#   id: ID!
#   name: String!
#   url: String!
# }
# 
# enum PlanTier {
#   FREE
#   BASIC
#   PRO
#   ENTERPRISE
# }
# 
# # 
# type ReferenceDesign {
#   name: String!
#   url: String!
# }
# 
# enum Role {
#   DISTRIBUTOR
#   CADMODELS
# }
# 
# enum SortDirection {
#   asc
#   desc
# }
# # 
# type SpecAgg {
#   attribute: Attribute!
#   buckets: [SpecBucket!]!
#   min: Float
#   max: Float
#   display_min: String
#   display_max: String
# }
# 
# type SpecBucket {
#   display_value: String!
#   float_value: Float
#   count: Int
# }
# 
# type SpellingCorrection {
#   correction_string: String!
#   hits: Int!
# }
# 
# type SponsoredPart {
#   _cache_id: String!
#   ppid: ID! @deprecated(reason: "use part.id instead")
#   source_id: ID! @deprecated(reason: "unused")
#   part: Part!
#   url: String!
# }
# 
# type Suggestion {
#   text: String!
#   in_category_name: String!
#   in_category_id: String!
# }


class OctopartProvider(Provider):
    name = "octopart_api"
    description = "Octopart api"
    
    baseurl = "https://octopart.com/api/v4/endpoint"
    
    # capabilities
    has_search_part = True
    
    def __init__(self):
        super(OctopartProvider, self).__init__()
    
    def _query(self, ):
        self.url = self.baseurl+path+'?'+urllib.parse.urlencode(self.args)
        print(self.url) 
        data = urllib.request.urlopen(self.url).read()
        return json.loads(data)
        
    def CheckConnection(self):
        # dummy query to check that the server is responding well
        req = "query { search(q: "", limit: 0) { results { part { name } } } }"
    
    def SearchPart(self, text):
        req = f'query {{ search(q: "{text}", limit: 0) {{ results {{ part {query_part} }} }} }}'
        return []
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# directive @HasPlanTier(tier: PlanTier!) on FIELD_DEFINITION
# directive @BlockAll(roles: [Role!]!) on FIELD_DEFINITION
# directive @RequireAny(roles: [Role!]!) on FIELD_DEFINITION
# type AppliedFilter {
#   shortname: String!
#   name: String!
#   values: [String!]!
#   display_values: [String!]!
# }
# 
# type Attribute {
#   id: ID!
#   name: String!
#   shortname: String!
#   group: String!
# }
# 
# type AttributeGroup {
#   name: String!
#   attributes: [Attribute!]!
# }
# 
# type Blurb {
#   name: String!
#   path_name: String!
#   description: String!
#   content: String!
# }
# 
# type CadBucket {
#   cad_state: String!
#   count: Int
# }
# 
# type Category {
#   id: ID!
#   parent_id: ID!
#   name: String!
#   ancestors: [Category!]!
#   children: [Category!]!
#   path: String!
#   relevant_attributes: [Attribute!]!
#   blurb: Blurb
#   num_parts: Int!
# }
# 
# type CategoryBucket {
#   category: Category!
#   count: Int
# }
# # 
# type CompanyBucket {
#   company: Company!
#   count: Int
# }
# 
# 
# type Document {
#   name: String!
#   page_count: Int
#   created_at: Time
#   url: String!
#   credit_string: String!
#   credit_url: String!
#   mime_type: String!
# }
# 
# 
# type Image {
#   url_largest: String! @deprecated(reason: "use `url` instead")
#   url_55px: String! @deprecated(reason: "use `url` instead")
#   url_75px: String! @deprecated(reason: "use `url` instead")
#   url_90px: String! @deprecated(reason: "use `url` instead")
#   url: String!
#   credit_string: String!
#   credit_url: String!
# }
# 
# scalar Map
# 
# type Offer {
#   _cache_id: String!
#   id: ID!
#   sku: String!
#   inventory_level: Int!
#   packaging: String
#   moq: Int
#   prices: [PricePoint!]!
#   click_url: String!
#   updated: Time!
#   factory_lead_days: Int
#   on_order_quantity: Int
#   factory_pack_quantity: Int
#   order_multiple: Int
#   multipack_quantity: Int
# }
 
# part {
#   id
#   name
#   mpn
#   generic_mpn
#   manufacturer {
#     id
#     name
#     aliases
#     homepage_url
#     slug
#     is_verified
#     is_broker
#     is_distributorapi
#   }
#   manufacturer_url
#   free_sample_url
#   document_collections {
#     name
#     documents {
#       name
#       page_count
#       created_at
#       url
#       credit_string
#       credit_url
#       mime_type
#     }
#   }
#   short_description
#   descriptions {
#     text
#     credit_string
#     credit_url
#   }
#   images {
#     url
#     credit_string
#     credit_url
#   }
#   specs {
#     attribute
#     display_value
#   }
#   slug
#   octopart_url
#   similar_parts {
#       name
#   }
#   companion_products: [SponsoredPart!]!
#  category: Category
#   series: PartSeries
#   best_image: Image
#   best_datasheet: Document
#   reference_designs: [ReferenceDesign!]!
#   cad: PartCad
#   cad_request_url: String
#   v3uid: ID!
#   counts: Map!
#   median_price_1000: PricePoint
#   total_avail: Int!
#   avg_avail: Float!
#   sellers(include_brokers: true, authorized_only: false) {
#     company {
#       id
#       name
#       aliases
#       homepage_url
#       slug
#       is_verified
#       is_broker
#       is_distributorapi
#     }     
#     offers: [Offer!]!
#     is_authorized
#     is_broker
#     is_rfq
#   }
#   estimated_factory_lead_days: Int
#   aka_mpns: [String!]!
# }
# 
# type PartCad {
#   add_to_library_url: String
#   has_3d_model: Boolean!
#   has_altium: Boolean!
#   has_eagle: Boolean!
#   has_orcad: Boolean!
#   has_kicad: Boolean!
#   download_url_altium: String!
#   download_url_eagle: String!
#   download_url_orcad: String!
#   download_url_kicad: String!
#   footprint_image_url: String
#   symbol_image_url: String
# }
# 
# type PartMatch {
#   reference: String
#   hits: Int!
#   parts: [Part!]!
#   error: String
# }
# 
# input PartMatchOptions {
#   require_authorized_sellers: Boolean = false
#   require_stock_available: Boolean = false
#   filters: Map
# }
# 
# input PartMatchQuery {
#   mpn: String
#   sku: String
#   mpn_or_sku: String
#   manufacturer: String
#   seller: String
#   start: Int! = 0
#   limit: Int! = 3
#   reference: String
# }
# 
# type PartResult {
#   _cache_id: String!
#   part: Part!
#   explain: String! @deprecated(reason: "always empty")
#   aka_mpn: String
#   description: String!
# }
# 
# type PartResultSet {
#   total: Int! @deprecated(reason: "use `hits` instead")
#   hits: Int!
#   results: [PartResult!]
#   specs_view_attribute_groups: [AttributeGroup!]!
#   warnings: [String!]
#   spec_aggs(
#     attribute_names: [String!]!
#     size: Int! = 10
#   ): [SpecAgg!]!
#   manufacturer_agg(size: Int! = 10): [CompanyBucket!]!
#   distributor_agg(size: Int! = 10): [CompanyBucket!]!
#   category_agg(size: Int! = 10): [CategoryBucket!]!
#   cad_agg: [CadBucket!]!
#   suggested_categories: [CategoryBucket!]!
#   suggested_filters: [Attribute!]!
#   all_filters: [Attribute!]!
#   applied_category: Category
#   applied_filters: [AppliedFilter!]!
# }
# 
# type PartSeller {
#   _cache_id: String!
#   company: Company!
#   offers: [Offer!]!
#   is_authorized: Boolean!
#   is_broker: Boolean!
#   is_rfq: Boolean!
# }
# 
# type PartSeries {
#   id: ID!
#   name: String!
#   url: String!
# }
# 
# enum PlanTier {
#   FREE
#   BASIC
#   PRO
#   ENTERPRISE
# }
# 
# type PricePoint {
#   _cache_id: String!
#   quantity: Int!
#   price: Float!
#   currency: String!
#   converted_price: Float!
#   converted_currency: String!
#   conversion_rate: Float!
# }
# 
# type Query {
#   attributes: [Attribute!]!
#   manufacturers(ids: [String!]): [Company!]!
#   sellers(ids: [String!]): [Company!]!
#   categories(
#     ids: [String!]
#     paths: [String!]
#   ): [Category!]!
#   parts(
#     ids: [String!]!
#     country: String! = "US"
#     currency: String! = "USD"
#     distributorapi: Boolean
#     distributorapi_timeout: String! = "3s"
#   ): [Part]!
#   suggest(
#     q: String!
#     category_id: String
#   ): [Suggestion!]!
#   search(
#     q: String
#     country: String! = "US"
#     currency: String! = "USD"
#     start: Int
#     limit: Int
#     sort: String
#     sort_dir: SortDirection
#     in_stock_only: Boolean
#     filters: Map
#     distributorapi: Boolean
#     distributorapi_timeout: String! = "3s"
#   ): PartResultSet!
#   spelling_correction(q: String!): [SpellingCorrection!]!
#   multi_match(
#     queries: [PartMatchQuery!]!
#     options: PartMatchOptions
#   ): [PartMatch!]!
# }
# 
# type ReferenceDesign {
#   name: String!
#   url: String!
# }
# 
# enum Role {
#   DISTRIBUTOR
#   CADMODELS
# }
# 
# enum SortDirection {
#   asc
#   desc
# }
# 
# type Spec {
#   attribute: Attribute!
#   display_value: String!
# }
# 
# type SpecAgg {
#   attribute: Attribute!
#   buckets: [SpecBucket!]!
#   min: Float
#   max: Float
#   display_min: String
#   display_max: String
# }
# 
# type SpecBucket {
#   display_value: String!
#   float_value: Float
#   count: Int
# }
# 
# type SpellingCorrection {
#   correction_string: String!
#   hits: Int!
# }
# 
# type SponsoredPart {
#   _cache_id: String!
#   ppid: ID! @deprecated(reason: "use part.id instead")
#   source_id: ID! @deprecated(reason: "unused")
#   part: Part!
#   url: String!
# }
# 
# type Suggestion {
#   text: String!
#   in_category_name: String!
#   in_category_id: String!
# }
# 
# scalar Time

