from pint import UnitRegistry, set_application_registry

# https://pint.readthedocs.io/en/stable/tutorial.html

# ureg = UnitRegistry(system='SI')
ureg = UnitRegistry()
ureg.default_format = "P~"
# Q_ = ureg.Quantity

set_application_registry(ureg)

def unit(value, default):
    quantity = ureg.Quantity(value)
    return quantity

