from unit_tests.helper import raised, run, redirect_stdout, redirect_stderr
import unittest
from api.unit import Quantity
import json
import math

epsilon = 1e-5  

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

    def test_unit(self):
        v = Quantity("10V")
        assert(str(v)=="10.0 V")
        assert(v.format()=="10 V")
        assert(str(v.unit)=="V")
        assert(v.magnitude==10)

        v = Quantity("10µV")
        assert(str(v)=="10.0 µV")
        assert(v.format()=="10 µV")
        assert(str(v.unit)=="µV")
        assert(math.fabs(v.magnitude-10)<epsilon)

    def test_base_unit(self):
        v = Quantity("10µV", base_unit="V")
        assert(str(v)=="10.0 µV")
        assert(str(v.unit)=="µV")
        assert(str(v.base_unit)=="V")
        assert(v.format()=="10 µV")
        
        v = Quantity("10", base_unit="V")
        assert(str(v)=="10.0 V")
        assert(str(v.unit)=="V")
        assert(str(v.base_unit)=="V")

    def test_format(self):
        v = Quantity("10.1V")
        assert(v.format(digits=3, trailing_zeros=True)=="10.1 V")
        assert(v.format(digits=3, trailing_zeros=False)=="10.1 V")

        v = Quantity("10.0004V")
        assert(v.format(digits=3, trailing_zeros=True)=="10.0 V")
        assert(v.format(digits=3, trailing_zeros=False)=="10. V")
    
    def test_percent(self):
        v = Quantity("10%")
        assert(str(v)=="10.0 %")
        assert(str(v.unit)=="%")
        
    def test_offset_unit(self):
        v = Quantity("°C")
        assert(str(v.unit)=="°C")

        v = Quantity("10 °C")
        assert(str(v.unit)=="°C")
        assert(math.fabs(v.magnitude-10)<epsilon)
        assert(v.format()=="10 °C")
        assert(v.to("°C").format()=="10 °C")

        v = Quantity("10 °C", base_unit="°C")
        assert(str(v.unit)=="°C")
        assert(v.magnitude==10)
        assert(v.format()=="10 °C")

    def test_offset_unit2(self):
        v = Quantity("10 ppm/°C")
        assert(str(v.unit)=="ppm/°C")
        assert(v.magnitude==10)
        assert(v.format()=="10 ppm/°C")

        v = Quantity("10 ppm/°C", base_unit="ppm/°C")
        assert(str(v.unit)=="ppm/°C")
        assert(v.magnitude==10)
        assert(v.format()=="10 ppm/°C")
        assert(v.to("ppm/°C").format()=="10 ppm/°C")

    def test_dict(self):
        v = Quantity("10 ppm/°C", base_unit="ppm/°C")
        d = v.to_dict()
        assert(d=={'value': 10.0, 'unit': 'ppm/°C', 'integer': False})
        
        v = Quantity("10 °C", base_unit="K")
        d = v.to_dict()
        assert(d=={'value': 283.15, 'unit': 'K', 'show_as': '°C', 'integer': False})

    