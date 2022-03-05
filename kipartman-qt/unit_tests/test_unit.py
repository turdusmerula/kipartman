from unit_tests.helper import raised, run, redirect_stdout, redirect_stderr
import unittest
from api.unit import Quantity

# def TestNDictSuite():
#     test_suite = unittest.TestSuite()
#     test_suite.addTest(unittest.makeSuite(TestNDict))
#     test_suite.addTest(unittest.makeSuite(TestNList))
#     # test_suite.addTest(unittest.makeSuite(TestFactory))
#     return test_suite

class TestQuantity(unittest.TestCase):
    
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

    def test_value(self):
        v = Quantity("10V")
        assert(str(v)=="10 V")
        assert(str(v.unit)=="V")
    
    def test_base_unit(self):
        v = Quantity("10µV", base_unit="V")
        assert(str(v)=="10 µV")
        assert(str(v.unit)=="µV")
        assert(str(v.base_unit)=="V")
    
        v = Quantity("10", base_unit="V")
        assert(str(v)=="10 V")
        assert(str(v.unit)=="V")
        assert(str(v.base_unit)=="V")
    
    def test_percent(self):
        v = Quantity("10%")
        print(v.unit, str(v))
        assert(str(v)=="10 %")
        assert(str(v.unit)=="%")
         