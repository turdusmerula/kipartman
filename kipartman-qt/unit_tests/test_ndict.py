from unit_tests.helper import raised, run, redirect_stdout, redirect_stderr
import unittest
from api.ndict2 import ndict, nlist, Merge

# def TestNDictSuite():
#     test_suite = unittest.TestSuite()
#     test_suite.addTest(unittest.makeSuite(TestNDict))
#     test_suite.addTest(unittest.makeSuite(TestNList))
#     # test_suite.addTest(unittest.makeSuite(TestFactory))
#     return test_suite

class TestNDict(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        pass
        
    @classmethod
    def tearDownClass(cls):
        pass


    def test_empty_dict(self):
        d = ndict()
    
    def test_init_dict(self):
        d = ndict({'foo': 'bar'})
        d = ndict(foo='bar')
        d = ndict([('foo', 'bar')])
    
    def test_get_value(self):
        d = ndict({'foo': 'bar'})
        assert(d.foo=='bar')
        assert(d['foo']=='bar')
    
    def test_set_value(self):
        d = ndict({'foo': 'bar'})
        d.foo = 'barbar'
        assert(d.foo=='barbar')
        assert(d['foo']=='barbar')
        d['foo'] = 'barbaz'
        assert(d.foo=='barbaz')
        assert(d['foo']=='barbaz')
        
    # def test_proxy(self):
    #     d = ndict({'foo': 'bar', 'f': 'b'})
    #     assert(list(d.values())==['bar', 'b'])
        
class TestNList(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        pass
        
    @classmethod
    def tearDownClass(cls):
        pass

    def test_get_item(self):
        l = nlist([1, 2, 3])
        assert(l[0]==1)
        
    def test_set_item(self):
        l = nlist([1, 2, 3])
        l[1] = 10
        assert(l[1]==10)

    def test_eq(self):
        l1 = nlist([1, 2, 3])
        l2 = nlist([1, 2, 3])
        l3 = nlist([1, 2, 3, 4])
        assert(l1==l2)
        assert(l1!=l3)
        assert(l1==[1, 2, 3])

class TestFactory(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        pass
        
    @classmethod
    def tearDownClass(cls):
        pass

    def test_sub_dict(self):
        d = ndict({
            'foo': [
                {'foobar': 1},
                {'foobaz': 2}
            ]
        })
        assert(isinstance(d.foo, nlist))
        assert(d.foo[0]=={'foobar': 1})
        assert(d.foo[0].foobar==1)

    def test_set_sub_dict(self):
        d = ndict({
            'foo': [
                {'foobar': 1},
                {'foobaz': 2},
                {'subfoo': [
                    {'foofoo': 3}
                ]}
            ]
        })
        d.foo[0].foobar = 10
        assert(d.foo[0].foobar==10)
        d.foo[2].subfoo[0].foofoo = 13
        assert(d.foo[2].subfoo[0].foofoo==13)
        d.foo[1] = {'test': 2}
        assert(d.foo[1]=={'test': 2})

    def test_set_sub_dict2(self):
        d = ndict({
            'foo': [
                {'foobar': 1},
                {'foobaz': 2}
            ]
        })
        d.foo[0]['foobar'] = 10
        assert(d.foo[0]['foobar']==10)

class TestDefault(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        pass
        
    @classmethod
    def tearDownClass(cls):
        pass

    def test_no_default(self):
        d = ndict()
        # print(d.foo)
        assert(raised(lambda: d.foo)[0]==KeyError)

    def test_dict_default(self):
        d = ndict({},
            default={'foo': 0})
        assert(d.foo==0)
        assert(d['foo']==0)
    
    def test_dict_sub_default(self):
        d = ndict({},
            default={
                'foo': {
                    'bar': 0
                },
            })
        assert(d.foo.bar==0)
        assert(d['foo']['bar']==0)

    def test_dict_sub_default2(self):
        d = ndict({
                'foo': {
                    'baz': 1
                }
            },
            default={
                'foo': {
                    'bar': 0
                },
            })
        assert(d.foo.bar==0)
        assert(d['foo']['bar']==0)

    def test_dict_recursive(self):
        d1 = ndict({},
            default={
                'foo': [
                    { 'baz': 1 }
                ]
            })
        d2 = ndict({
            },
            default=d1
        )
        assert(len(d2.foo)==1)

    # def test_dict_recursive2(self):
    #     d1 = ndict({},
    #         default={
    #             'foo': [
    #                 {
    #                     'baz': [
    #                         {'foo': 'a'},
    #                         {'bar': 'a'},
    #                     ] 
    #                 }
    #             ]
    #         })
    #     d2 = ndict({
    #         },
    #         default=d1
    #     )
    #     assert(len(d2.foo)==1)

class TestSerialization(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        pass
        
    @classmethod
    def tearDownClass(cls):
        pass

    def test_yaml_ndict(self):
        import yaml
        
        d = {
            'foo': {
                'foobar': 1,
                'foobaz': 2
            }
        }
        nd = ndict(d)
        s = yaml.dump(d)
        ns = yaml.dump(nd.to_dict()) 
        assert(s==ns)

    def test_yaml_nlist(self):
        import yaml
        
        d = {
            'foo': [
                {'foobar': 1},
                {'foobaz': 2}
            ]
        }
        nd = ndict(d)
        s = yaml.dump(d)
        ns = yaml.dump(nd.to_dict())
        assert(s==ns)

    def test_yaml_ndict_default(self):
        import yaml
        
        d0 = {
            'foo': {
                'foofoo': 0,
                'foofoofoo': 4
            },
            'bar': 3,
            'foo_list': [
                {'foofoo': 0}
            ]
        }
        d1 = {
            'foo': {
                'foofoo': 3,
                'foobar': 1,
                'foobaz': 2
            },
            'foo_list': [
                {'foobar': 1},
                {'foobaz': 2}
               ]
        }
        
        nd1 = ndict(d1, default=d0)
        s = yaml.dump(d1)
        ns = yaml.dump(nd1.to_dict(recursive=False))
        assert(s==ns)

        from mergedeep import merge, Strategy
        
        r = {}
        merge(r, d0, d1, strategy=Strategy.REPLACE)
        s = yaml.dump(r)
        ns = yaml.dump(nd1.to_dict(recursive=True, strategy=Strategy.REPLACE))
        assert(s==ns)
        
        r = {}
        merge(r, d0, d1, strategy=Strategy.ADDITIVE)
        s = yaml.dump(r)
        ns = yaml.dump(nd1.to_dict(recursive=True, strategy=Strategy.ADDITIVE))
        assert(s==ns)
        
class TestSerialization(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        pass
        
    @classmethod
    def tearDownClass(cls):
        pass

    def test_iterator(self):
        d0 = {
            'foo': {
                'foofoo': 0,
                'foofoofoo': 4
            },
            'bar': 3,
            'foo_list': [
                {'foofoo': 0}
            ]
        }
        d1 = {
            'foo': {
                'foofoo': 3,
                'foobar': 1,
                'foobaz': 2
            },
            'foo_list': [
                {'foobar': 1},
                {'foobaz': 2}
               ]
        }
        
        nd1 = ndict(d1, default=d0)

        for item in nd1:
            print(item)
        print(list(nd1.keys()))
        