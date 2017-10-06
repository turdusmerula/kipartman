import rest 
import wx
import re

class OctopartExtractor(object):
    
    def __init__(self, octopart):
        self.octopart = octopart 
        
    def GetUnit(self, spec):
        symbol = self.GetUnitSymbol(spec)
        if spec.metadata().unit():
            try:
                return rest.api.find_units(symbol=symbol)[0]
            except Exception as e:
                wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
#            except Exception as e:
                #TODO create unit if not found
#                wx.MessageBox('%s: unit unknown' % (symbol), 'Warning', wx.OK | wx.ICON_EXCLAMATION)

        return None
    
    def GetUnitPrefix(self, spec):
        symbol = self.GetUnitPrefixSymbol(spec)
        if symbol=='' or symbol is None:
            return None
        if spec.metadata().unit():
            try:
                return rest.api.find_unit_prefixes(symbol=symbol)[0]
            except Exception as e:
                wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
#            except:
#                wx.MessageBox('%s: unit prefix unknown' % (symbol), 'Warning', wx.OK | wx.ICON_EXCLAMATION)
        return None
        
    def GetUnitSymbol(self, spec):
        if spec.metadata().unit():
            return spec.metadata().unit().symbol().encode('utf8')
        return ""

    def GetUnitPrefixSymbol(self, spec):
        if spec.display_value() is None:
            return ""
        display_value = spec.display_value().split(" ")
        unit = self.GetUnitSymbol(spec)
        if len(display_value)<2:
            return ""   # there is only a value, no unit
        display_unit = display_value[1]
        # filter non alpha chars
        display_unit = re.sub('[ ,.;]', '', display_unit)
        prefix = display_unit[:-len(unit)]
        return prefix.encode('utf8')
    
    def GetPrefixedValue(self, value, prefix):
        if prefix is None:
            return float(value)
        return float(value)/float(prefix.power)

    def ExtractParameter(self, spec_name):
        parameter = rest.model.PartParameter()
        spec = self.octopart.item().specs()[spec_name]
        print "spec: ", spec.json
        parameter.name = spec_name
        parameter.description = spec.metadata().name()
        parameter.unit = self.GetUnit(spec)
        parameter.nom_prefix = self.GetUnitPrefix(spec)
        parameter.nom_value = None
        parameter.text_value = None
        if spec.value() and len(spec.value())>0:
            try:
                if parameter.unit:
                    parameter.nom_value = self.GetPrefixedValue(spec.value()[0], parameter.nom_prefix)
                else:
                    parameter.nom_value = float(spec.value()[0])
                parameter.numeric = True
            except:
                parameter.text_value = spec.value()[0]
                parameter.numeric = False
        if spec.min_value():
            try:
                if parameter.unit:
                    parameter.min_value = self.GetPrefixedValue(spec.min_value(), parameter.nom_prefix)
                else:
                    parameter.min_value = float(spec.value()[0])
                parameter.min_prefix = parameter.nom_prefix
                parameter.numeric = True
            except:
                parameter.numeric = False
        else:
            parameter.min_value = None
        if spec.max_value():
            try:
                if parameter.unit:
                    parameter.max_value = self.GetPrefixedValue(spec.max_value(), parameter.nom_prefix)
                else:
                    parameter.max_value = float(spec.value()[0])
                parameter.numeric = True
                parameter.max_prefix = parameter.nom_prefix
            except:
                parameter.numeric = False
        else:
            parameter.max_value = None

        return parameter