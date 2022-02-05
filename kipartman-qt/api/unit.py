from pint import UnitRegistry, set_application_registry

# https://pint.readthedocs.io/en/stable/tutorial.html

ureg = UnitRegistry()
Q_ = ureg.Quantity

set_application_registry(ureg)
