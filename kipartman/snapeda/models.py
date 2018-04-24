
class Model(object):
    def __init__(self, json):
        self.json = json

class SearchPage(Model):
    #TODO
    pass

class SearchResult(Model):
    def package(self):
        if self.json['package']:
            return Package(self.json['package'])
        return None

    def part_number(self):
        return self.json["part_number"]

    def availability_description(self):
        return self.json["availability_description"]

    def average_price(self):
        return self.json["average_price"]

    def availability_count(self):
        return self.json["availability_count"]

    def coverart(self):
        list = []
        # try:
        #     pass
        # except expression as identifier:
        #     pass
        if self.json.has_key("coverart"):
            for item in self.json["coverart"]:
                list.append(Url(item))
        return list
    
    def uniqueid(self):
        return self.json["uniqueid"]

    def availability(self):
        return self.json["availability"]

    def organization_image_100_20(self):
        return self.json["organization_image_100_20"]

    def manufacturer(self):
        return self.json["manufacturer"]

    def name(self):
        return self.json["name"]

    def urlmanufacturer(self):
        return self.json["urlmanufacturer"]

    def has_datasheet(self):
        return self.json["has_datasheet"]

    def has_footprint(self):
        return self.json["has_footprint"]

    def short_description(self):
        return self.json["short_description"]

    def has_symbol(self):
        return self.json["has_symbol"]

    def _links(self):
        if self.json['_links']:
            return Link(self.json['_links'])
        return None

    def urlname(self):
        return self.json["urlname"]

    def models(self):
        list = []
        if self.json.has_key("models"):
            for item in self.json["models"]:
                list.append(ResultModel(item))
        return list

class Package(Model):
    def name(self):
        return self.json["name"]

class Link(Model):
    def self(self):
        if self.json['self']:
            return Self(self.json['self'])
        return None

class Url(Model):
    def url(self):
        return self.json["url"]
        
class ResultModel(Model):
    def symbol_medium(self):
        if self.json['symbol_medium']:
            return Url(self.json['symbol_medium'])
        return None
        
    def package_medium(self):
        if self.json['package_medium']:
            return Url(self.json['package_medium'])
        return None

    def model_type(self):
        return self.json["model_type"]
    
class Self(Model):
    def href(self):
        return self.json["href"]
