from api.configuration import configuration
from api.unit import Quantity, QuantityRange
from api.log import log

from diskcache import Cache
import json
import os
from string import Template
import urllib.request
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
        """ Extract all fileds for type to be used in a query """

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
    
        self.ttl = Quantity("1 week", base_unit="s").magnitude
        try:
            self.ttl = Quantity(configuration.providers.octopart.cache_ttl, base_unit="s").magnitude
        except Exception as e:
            log.error(f"Octopart cache_ttl configuration: {e}")
        
        self.limit = configuration.providers.octopart.limit
        if self.limit is None:
            self.limit = 1

        self.cache = Cache(directory=os.path.expanduser('~/.kipartman/cache/octopart'))

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
    
    def _encode_filters(self, filters):
        params = []
        for filter, value in filters.items():
            if isinstance(value, Quantity):
                params.append(f'{filter}: "{str(value)}"')
            elif isinstance(value, QuantityRange):
                min = ""
                if value.min is not None:
                    min = str(value.min)
                max = ""
                if value.max is not None:
                    max = str(value.max)
                params.append(f'{filter}: "({min}__{max})"')
            elif isinstance(value, str):
                params.append(f'{filter}: "{value}"')
            else:
                params.append(f'{filter}: {value}')
        
        return f"filters: {{{', '.join(params)}}}"

    def _set_cache_part_query(self, query, data):
        res = self.cache.set(query, json.dumps(data), expire=self.ttl)
        log.debug(f"add cache query: {query}")
        
        results = None
        if "search" in data:
            results = data['search']['results']
        elif "search_mpn" in data:
            results = data['search_mpn']['results']
            
        if results is not None:
            for result in results:
                self.cache.set(result['part']['id'], json.dumps(result['part']), expire=self.ttl)
                log.debug(f"add cache part: {result['part']['id']}")

        return res
    
    def _get_cache_part_query(self, query):
        c = self.cache.get(query)
        if c is not None:
            log.debug(f"fetch cache query: {query}")
            return json.loads(c)

        return c
        
    def _get_cache_part(self, id):
        c = self.cache.get(id)
        if c is not None:
            log.debug(f"fetch cache part: {id}")
            
        data = json.loads(data)

        return 

    def _search(self, request, q=None, start=0, limit=None, country=None, currency=None, sort='median_price_1000', sort_dir='asc', in_stock_only=None, filters={}):
        query = """
            query PartSearch {
              $request($params) {
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
        
        params = []
        if q is not None:
            params.append(f'q: "{q}"')
        params.append(f"start: {start}")
        if limit is None:
            params.append(f"limit: {self.limit}")
        else:
            params.append(f"limit: {limit}")
        if country is not None:
            params.append(f'country: "{country}"')        
        if currency is not None:
            params.append(f'currency: "{currency}"')
        if sort is not None:
            params.append(f'sort: "{sort}"')
        if sort_dir is not None:
            params.append(f'sort_dir: {sort_dir}')
        if in_stock_only is not None:
            params.append(f'in_stock_only: {int(in_stock_only)}')
        if len(filters)>0:
            params.append(self._encode_filters(filters))
        

        query = Template(query).substitute(request=request, params=", ".join(params), Part=self.Part_to_query())
        query_id = Template("$request($params)").substitute(request=request, params=", ".join(params))
        # log.debug(query)
        log.debug(query_id)
        
        data = self._get_cache_part_query(query_id)
        if data is None:
            try:
                data = json.loads(self.send(query))["data"]
                self._set_cache_part_query(query_id, data)
            except Exception as e:
                log.error(f"{query_id}: {e}")
                return None

        return data
    
    def Search(self, q=None, start=0, limit=None, country=None, currency=None, sort='median_price_1000', sort_dir='asc', in_stock_only=None, filters={}):
        return self._search("search", q, start, limit, country, currency, sort, sort_dir, in_stock_only, filters)

    def SearchMpn(self, q=None, start=0, limit=None, country=None, currency=None, sort='median_price_1000', sort_dir='asc', in_stock_only=None, filters={}):
        return self._search("search_mpn", q, start, limit, country, currency, sort, sort_dir, in_stock_only, filters)

    def SearchPart(self, ids, country=None, currency=None):
        query = """
            query PartSearch {
              parts($params) {
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
        
        params = []
        params.append(f"ids: [{', '.join(ids)}]")
        if country is not None:
            params.append(f'country: "{country}"')        
        if currency is not None:
            params.append(f'currency: "{currency}"')
        
        query = Template(query).substitute(params=", ".join(params), Part=self.Part_to_query())
        print(query)
        data = json.loads(self.send(query))["data"]
        print(yaml.dump(data))        
        return data

    def MultiMatch(self):
        # TODO
        pass

    def Suggest(self):
        # TODO
        pass

    def SpellingCorrection(self):
        # TODO
        pass
    
    def Attributes(self):
        query = """
            query AttributesSearch {
              attributes() {
                id
                name
                shortname
                group
              }
            }        
        """
        res = json.loads(self.send(query))
        return res.data.attributes
    
    def Manufaturers(self):
        # TODO
        pass
    
    def Sellers(self):
        # TODO
        pass

    def Categories(self):
        # TODO
        pass

    def ClearCache(self):
        self.cache.clear()