
class Model(object):
    def __init__(self, json):
        self.json = json

class SearchPage(Model):
    #TODO
    pass

class SearchResult(Model):
    def has_footprint(self):
        return self.json["has_footprint"]

    def average_price(self):
        return self.json["average_price"]

    def has_datasheet(self):
        return self.json["has_datasheet"]

    def has_symbol(self):
        return self.json["has_symbol"]

    def urlname(self):
        return self.json["urlname"]

    def _links(self):
        if self.json['_links']:
            return Link(self.json['_links'])
        return None

    def part_number(self):
        return self.json["part_number"]

    def availability_count(self):
        return self.json["availability_count"]

    def pin_count(self):
        if self.json.has_key("pin_count"):
            return self.json["pin_count"]
        return None
    
    def availability(self):
        return self.json["availability"]

    def image(self):
        return self.json["image"]

    def urlmanufacturer(self):
        return self.json["urlmanufacturer"]

    def short_description(self):
        return self.json["short_description"]

    def name(self):
        return self.json["name"]

    def uniqueid(self):
        return self.json["uniqueid"]

    def package_type(self):
        return self.json["package_type"]

    def organization_image_100_20(self):
        return self.json["organization_image_100_20"]

    def manufacturer(self):
        return self.json["manufacturer"]

    def availability_description(self):
        return self.json["availability_description"]


class Link(Model):
    def self(self):
        if self.json['self']:
            return Self(self.json['self'])
        return None


class Self(Model):
    def href(self):
        return self.json["href"]
