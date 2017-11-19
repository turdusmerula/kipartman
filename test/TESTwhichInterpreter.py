import os,sys
import json,re
import pprint



def removeComments(string):
    string = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,string) # remove all occurance streamed comments (/*COMMENT */) from string
    string = re.sub(re.compile("//.*?\n" ) ,"" ,string) # remove all occurance singleline comments (//COMMENT\n ) from string
    return string



vscodeSettingsJson = json.loads(
    removeComments(
        open(os.path.join(os.getcwd(),'.vscode','settings.json'))
        .read()))
print('.vscode---------------------------Settings.json----------------------')
print (json.dumps(vscodeSettingsJson, 
            indent=4, 
            sort_keys=True))
vscodeLaunchJson = json.loads(
    removeComments(
        open(os.path.join(os.getcwd(),'.vscode','launch.json'))
        .read()))
print('.vscode---------------------------launch.json (configurations)-----------------')

configs = vscodeLaunchJson['configurations']
configPython = configs[0]
print('.vscode--------------------------------------configuration:{}-----------------'
    .format(
        configPython['name']
        ))
print(json.dumps(configPython, indent=4, sort_keys=False))
print('.vscode----CONFIG checks ---------------------------------------------------')
try:
    print('launch.json  INTERPRERTER EXISTS python.pythonPath:{}  EXISTS:{}'.format(
        configPython['python.pythonPath'],
        os.path.isfile(configPython['python.pythonPath'])
    ))
except:
    pass    

print ('CURRENT INTERPRETER EXECUTING    sys.executable={}'.format(sys.executable))
print ('')
try:
    print('EXPECTATION MET : {}  '.format(
        configPython['python.pythonPath']==sys.executable
    )
    )
except:
    pass    
