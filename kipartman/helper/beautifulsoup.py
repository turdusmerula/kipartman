from bs4 import BeautifulSoup as bs
import re

class BeautifulSoupException(Exception):
    def __init__(self, message):
        self.message = message


class BeautifulSoup(object):
    def __init__(self, url):
        super(BeautifulSoup, self).__init__()
        self.bs = bs(url, 'lxml')

    def find(self, name=None, attrs={}, recursive=True, text=None, **kwargs):
        res = self.bs.find(name=name, attrs=attrs, recursive=recursive, text=text, **kwargs)
       
        if res is None:
            criterias = ""
            if name is not None:
                criterias += f"{name}"
            if len(attrs)>0:
                for t, v in attrs.items():
                    criterias += f" {t}={v}"
            if text is not None:
                criterias += f" '{text}'"
            raise BeautifulSoupException(f"item not found: {criterias}")
        
        return res

    def find_all(self, name=None, attrs={}, recursive=True, text=None, **kwargs):
        res = self.bs.find_all(name=name, attrs=attrs, recursive=recursive, text=text, **kwargs)
       
        if len(res)==0:
            criterias = ""
            if name is not None:
                criterias += f"{name}"
            if len(attrs)>0:
                for t, v in attrs.items():
                    criterias += f" {t}={v}"
            if text is not None:
                criterias += f" '{text}'"
            raise BeautifulSoupException(f"no item found: {criterias}")
        
        return res

    def select(self, selector, _candidate_generator=None, limit=None):
        res = self.bs.select(selector=selector, _candidate_generator=_candidate_generator, limit=limit)
        
        if res is None:
            raise BeautifulSoupException(f"item not found: {selector}")
        
        return res
        
    def select_first(self, selector, _candidate_generator=None, limit=None):
        res = self.bs.select(selector=selector, _candidate_generator=_candidate_generator, limit=limit)
        
        if len(res)==0:
            raise BeautifulSoupException(f"item not found: {selector}")
        
        return res[0]
        

# class test(re):
#     def __init__(self, **kwargs):
#         super(test, self).__init__(self, *args, **kwargs)
#         
#     def match(self, value):
#         print("++++")

def contains(pattern):
    return re.compile(f".*{pattern}.*")