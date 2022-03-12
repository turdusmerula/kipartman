from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtCore import QModelIndex
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTreeView, QHeaderView, QAbstractItemView,\
    QMessageBox

from api.command import Command, CommandUpdateDatabaseObject, CommandAddDatabaseObject, commands
from api.event import events
from api.log import log
from api.ndict import ndict
from api.unit import Quantity
from database.models import Part, PartInstance, Parameter, ParameterType, PartParameter
from helper.dialog import ShowDialog, ShowErrorDialog
from enum import Enum

import json
import yaml

class CommandUpateOctopart(CommandUpdateDatabaseObject):
    def __init__(self, part, fields):
        super(CommandUpateOctopart, self).__init__(object=part, fields=fields,
                                            description=f"update part '{part.name}' from octopart")

class CommandAddOctopart(CommandAddDatabaseObject):
    def __init__(self, part, fields):
        super(CommandAddOctopart, self).__init__(object=part, fields=fields,
                                            description=f"add part '{fields['name']}' from octopart")

class CommandUpdateOctopartParameter(CommandUpdateDatabaseObject):
    def __init__(self, part_parameter, name, fields):
        super(CommandUpdateOctopartParameter, self).__init__(object=part_parameter, fields=fields,
                                            description=f"update part parameter '{name}' from octopart")

class CommandAddOctopartParameter(CommandAddDatabaseObject):
    def __init__(self, part_parameter, name, fields):
        super(CommandAddOctopartParameter, self).__init__(object=part_parameter, fields=fields,
                                            description=f"add part parameter '{name}' from octopart")

def import_octopart(octopart, category):
    octopart = ndict(octopart)
    
    if category is None:
        log.info(f"import from octopart '{octopart.mpn}'")
    else:
        log.info(f"import from octopart '{octopart.mpn}' on category '{category.name}'")
    
    # check if part already exists
    part = Part.objects.filter(uid=octopart.id).first()
    if part is None:
        part = Part.objects.filter(name=octopart.mpn).first()
        
    part_fields = {
        'name': octopart.mpn,
        'description': octopart.short_description,
        'instance': PartInstance.PART,
        'provider': 'octopart',
    }
    if part is None:
        part = Part()
        part_fields['category'] = category  # category is set only for new parts
        commands.Begin(CommandAddOctopart, part=part, fields=part_fields)
    else:
        res = ShowDialog("Import from octopart", text=f"Part '{octopart.mpn}' already exists, update it from octopart?", icon=QMessageBox.Icon.Question, buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if res==QMessageBox.StandardButton.Yes:
            commands.Begin(CommandUpateOctopart, part=part, fields=part_fields)
        else:
            return None

    # add part parameters
    for spec in octopart.specs:
        parameter = Parameter.objects.filter(name=spec.attribute.name).first()
        if parameter is None:
            # TODO ask for parameter creation instead of error
            ShowErrorDialog("Import from octopart", text=f"Parameter '{spec.attribute.name}' unknown", detailed_text=yaml.safe_dump(spec))
            commands.CancelAll()
            return None
        
        part_parameter = PartParameter.objects.filter(part=part.id, parameter=parameter.id).first()
        part_parameter_fields = {
            'part': part,
            'parameter': parameter,
            'metaparameter': False,
            'operator': None,
        }
        if parameter.value_type in [ParameterType.INTEGER, ParameterType.FLOAT]:
            try:
                if parameter.unit is None:
                    if parameter.value_type==ParameterType.FLOAT:
                        part_parameter_fields['value'] = {
                            'value': Quantity(spec.display_value).magnitude,
                            'integer': False
                        }
                    else:
                        part_parameter_fields['value'] = {
                            'value': Quantity(spec.display_value, integer=True).magnitude,
                            'integer': True
                        }
                        
                else:
                    if parameter.value_type==ParameterType.FLOAT:
                        value = Quantity(spec.display_value, base_unit=parameter.unit)
                    else:
                        value = Quantity(spec.display_value, base_unit=parameter.unit, integer=True)
                        
                    part_parameter_fields['value'] = {
                        'value': value.magnitude,
                        'unit': str(value.base_unit),
                        'show_as': str(value.unit),
                        'integer': value.integer,
                    }
            except Exception as e:
                log.error(f"{e}")
                ShowErrorDialog("Import from octopart", text=f"Import failed for '{spec.attribute.name}'", detailed_text=f"{e}\n\n{yaml.safe_dump(spec)}")
                commands.CancelAll()
                return None
        elif parameter.value_type==ParameterType.TEXT:
            part_parameter_fields['value'] = {
                'value': spec.display_value
            }
        else:
            ShowErrorDialog("Import from octopart", text=f"Parameter type {parameter.value_type} not implemented", detailed_text=f"{yaml.safe_dump(spec)}")
            commands.CancelAll()
            return None
        
        if part_parameter is None:
            part_parameter = PartParameter()
            commands.Continue(CommandAddOctopartParameter, part_parameter=part_parameter, name=parameter.name, fields=part_parameter_fields)            
        else:
            commands.Continue(CommandUpdateOctopartParameter, part_parameter=part_parameter, name=parameter.name, fields=part_parameter_fields)            
        
    commands.End()
    return part
