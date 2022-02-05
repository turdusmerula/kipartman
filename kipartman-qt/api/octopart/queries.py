from api.configuration import configuration
from six.moves import urllib
import json
from munch import munchify, DefaultMunch
import os
from string import Template
import yaml

# see https://octopart.com/api/v4/reference
# see https://octopart.com/playground
# https://octopart.com/my/api

class GraphQLClientException(Exception):
    def __init__(self, error):
        super(GraphQLClientException, self).__init__(error)

class GraphQLClient:
    def __init__(self):
        self.endpoint = 'https://octopart.com/api/v4/endpoint'
        self.token = configuration.providers.octopart.api_key
        self.headername = None
        self.introspect = None
        
    def build_introspection_graph(self):
        if self.introspect is not None:
            return

        # https://gist.github.com/a7v8x/c30d92d2ca2458035aadc41702da367d
        query = """
            query IntrospectionQuery {
              __schema {
                queryType { name }
                mutationType { name }
                types {
                  ...FullType
                }
                directives {
                  name
                  description
                  locations
                  args {
                    ...InputValue
                  }
                }
              }
            }
            fragment FullType on __Type {
              kind
              name
              description
              fields(includeDeprecated: true) {
                name
                description
                args {
                  ...InputValue
                }
                type {
                  ...TypeRef
                }
                isDeprecated
                deprecationReason
              }
              inputFields {
                ...InputValue
              }
              interfaces {
                ...TypeRef
              }
              enumValues(includeDeprecated: true) {
                name
                description
                isDeprecated
                deprecationReason
              }
              possibleTypes {
                ...TypeRef
              }
            }
            fragment InputValue on __InputValue {
              name
              description
              type { ...TypeRef }
              defaultValue
            }
            fragment TypeRef on __Type {
              kind
              name
              ofType {
                kind
                name
                ofType {
                  kind
                  name
                  ofType {
                    kind
                    name
                    ofType {
                      kind
                      name
                      ofType {
                        kind
                        name
                        ofType {
                          kind
                          name
                          ofType {
                            kind
                            name
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
        """
        
        self.introspect = json.loads(self.send(query))
        # self.introspect = munchify(json.loads(self.send(query)))
        print(yaml.dump(self.introspect))

    def get_type(self, name):
        for type in self.introspect['data']['__schema']['types']:
            if type['name']==name:
                return type
        raise GraphQLClientException(f"Type unknown: {name}")

    def get_field_type(self, field):
        oftype = field['type']['ofType']
        kind = field['type']['kind']
        name = field['type']['name']
        while oftype is not None:
            kind = oftype['kind']
            name = oftype['name']
            oftype = oftype['ofType']
        return (kind, name)
    
    def type_to_query(self, name, ignore=[], tab="", state=[]):
        res = ""
        type = self.get_type(name)
        for field in type['fields']:
            
            kind, name = self.get_field_type(field)
            state.append(field['name'])

            if '.'.join(state) not in ignore:
                # print(f"++{tab}", field['name'], kind, name, '.'.join(state))
                res += f"{tab}{field['name']}"
                
                if kind=='OBJECT':
                    res += " {\n"
                    res += self.type_to_query(name, ignore=ignore, tab=tab+"  ", state=state)
                    res += f"{tab}}}"

                res += "\n"
            state.pop()
            
        return res
    
    def send(self, query, variables={}):
        data = {'query': query,
                'variables': variables}
        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json'}

        if self.token is not None:
            headers['token'] = self.token

        req = urllib.request.Request(self.endpoint, json.dumps(data).encode('utf-8'), headers)

        try:
            response = urllib.request.urlopen(req)
            return response.read().decode('utf-8')
        except urllib.error.HTTPError as e:
            print((e.read()))
            print('')
            raise e

class OctopartPartQuery(GraphQLClient):
    def __init__(self):
        super(OctopartPartQuery, self).__init__()
    
    def Part_to_query(self, tab=""):
        return """
            part {
              _cache_id
              id
              name
              mpn
              generic_mpn
              manufacturer {
                id
                name
                aliases
                display_flag
                homepage_url
                slug
                is_verified
                is_broker
                is_distributorapi
              }
              manufacturer_url
              free_sample_url
              document_collections {
                name
                documents {
                  name
                  page_count
                  created_at
                  url
                  credit_string
                  credit_url
                  mime_type
                }
              }
              short_description
              descriptions {
                text
                credit_string
                credit_url
              }
              images {
                url_largest
                url_55px
                url_75px
                url_90px
                url
                credit_string
                credit_url
              }
              specs {
                attribute {
                  id
                  name
                  shortname
                  group
                }
                display_value
              }
              slug
              octopart_url
              category {
                id
                parent_id
                name
                path
                relevant_attributes {
                  id
                  name
                  shortname
                  group
                }
                blurb {
                  name
                  path_name
                  description
                  content
                }
                num_parts
              }
              series {
                id
                name
                url
              }
              best_image {
                url_largest
                url_55px
                url_75px
                url_90px
                url
                credit_string
                credit_url
              }
              best_datasheet {
                name
                page_count
                created_at
                url
                credit_string
                credit_url
                mime_type
              }
              reference_designs {
                name
                url
              }
              v3uid
              counts
              median_price_1000 {
                _cache_id
                quantity
                price
                currency
                converted_price
                converted_currency
                conversion_rate
              }
              total_avail
              avg_avail
              sellers (include_brokers: true, authorized_only: false) {
                _cache_id
                company {
                  id
                  name
                  aliases
                  display_flag
                  homepage_url
                  slug
                  is_verified
                  is_broker
                  is_distributorapi
                }
                country
                offers {
                  _cache_id
                  id
                  sku
                  eligible_region
                  inventory_level
                  packaging
                  moq
                  prices {
                    _cache_id
                    quantity
                    price
                    currency
                    converted_price
                    converted_currency
                    conversion_rate
                  }
                  click_url
                  updated
                  factory_lead_days
                  on_order_quantity
                  factory_pack_quantity
                  order_multiple
                  multipack_quantity
                  is_custom_pricing
                }
                is_authorized
                is_broker
                is_rfq
                ships_to_countries {
                  name
                  country_code
                  continent_code
                }
              }
              estimated_factory_lead_days
              aka_mpns
            }
        """
        
    def PartResultSet_to_query(self, tab=""):
        # TODO: build request from introspection
        # self.build_introspection_graph()
        # return self.type_to_query('PartResultSet', ignore=[
        #     'results.part.similar_parts', 
        #     'results.part.companion_products',
        #     'results.part.category.ancestors',
        #     'results.part.category.children',
        #     'category_agg.category.ancestors',
        #     'category_agg.category.children',
        #     'suggested_categories.category.ancestors',
        #     'suggested_categories.category.children',
        #     'applied_category.ancestors.ancestors',
        #     'applied_category.ancestors.children',
        #     'applied_category.children.ancestors',
        #     'applied_category.children.children'
        #     'spec_aggs'],
        #     tab=tab)
        pass
        
    def search(self, name):
        query = """
            query PartSearch {
              search(q: "$name") {
                hits
                results {
                  _cache_id
                  
                  $Part
            
                  explain
                  aka_mpn
                  description
                }
              }
            }        
        """

        query = Template(query).substitute(name=name, Part=self.Part_to_query())
        print(query)
        data = json.loads(self.send(query))
        print(yaml.dump(data))
        