import rest

class PartsCache(object):
    def __init__(self):
        self.parts = {}
    
    def Find(self, part_id):
        if part_id in self.parts:
            return self.parts[part_id]
        part = rest.api.find_part(part_id, with_childs=True, with_storages=True, with_distributors=True, with_references=True)
        self.parts[part_id] = part
        return part

    def Clear(self):
        self.parts = {} 
