from . import _import_base

from . import external_sqltables

import os
import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, MetaData, Table, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select



#Base = declarative_base()


class sqlImport(_import_base.KiPartmanImporter):
    extension = 'sql'
    wildcard = 'sqldb|sql'

    def fetch(self, base_filename, importItem):
        

        config_dir = os.path.join(os.path.expanduser("~"), '.bomsaway.d')

        _legacy_dir = os.path.join( os.path.expanduser("~"), '.kicadbommgr.d',)
        config_file = os.path.join( config_dir, 'BOMSAway.conf')
        datastore_file = os.path.join( config_dir, 'TEST17W46Abommgr.db')

        Base = declarative_base()


        file_path = '{}.{}'.format(base_filename, self.extension)

        ds = Datastore(datastore_file)

        connection = ds._eng.connect()
        components = []
        result = connection.execute("select * from Kipartman_Parts")
        for row in result:
            i = importItem.PartNew()
            i.name = row['name']
            i.description = row['description']
            i.comment  = 'NEW IMPORT Timestamp:{:%y-%m-%d %H:%M:%S.%f}'.format(datetime.datetime.now())
            components.append(i)
            print("Name:", row['name'], row['category'],row['description'])
        connection.close()
        
        # for fp in sorted(components):
        #     k_part = external_sqltables.Kipartman_Parts(
        #         id=fp.id,
        #         comment=fp.comment,
        #         name=fp.name,
        #         category='{}'.format(fp.category),
        #         description=fp.description,
        #          )
        #     s.add(k_part)
        #     # wrt.writerow(
        #     #     [format_csv_column_entry(fp, key)
        #     #     for key in 
        #     #     fp.swagger_types.viewkeys()])
        # s.commit()
        # s.close()

        #TODO: Use some of the following in imports
        # connection = ds._eng.connect()
        # result = connection.execute("select default_code from MRP_ProductItems")
        # for row in result:
        #     print("default_code:", row['default_code'])
        # connection.close()


        # con = ds._eng.connect()
        # meta = MetaData(ds._eng)


        # # insp = inspect(ds._eng)
        # # insp.get_table_names()
        # # insp.get_columns('MRP_ProductItems')



        # someMRP_ProductItems = Table('MRP_ProductItems', meta, autoload=True)

        # stm = select([someMRP_ProductItems.c.default_code]).limit(3)
        # rs = con.execute(stm)

        # print( rs.fetchall())
        # con.close()









def format_csv_column_entry(fp, key):
    #return repr(fp.to_dict()[key]).encode('ascii',errors='xmlcharrefreplace')
    field = fp.to_dict()[key]
    #if '{}'.format(type(field)) = "<type 'dict'>":
    if isinstance(field,unicode):
        #print('DEBUG:{}:{}:{}'.format(type(field), key, fp.to_dict()[key].encode('ascii', errors='xmlcharrefreplace')))
        return fp.to_dict()[key].encode('ascii', errors='xmlcharrefreplace')
    else:
        return fp.to_dict()[key]





# {'name': 'CARBON RESISTOR, 510KOHM, 500mW, 5%',
# 'description': 'CARBON RESISTOR, 510KOHM, 500mW, 5%; Product Range:MCRC Series; Resistance:510kohm; Power Rating:500mW; Resistance Tolerance:  5%; Voltage Rating:350V; Resistor Case Style:Axial Leaded; Resistor Eleme 73K0236 ',
# 'barcode': False,
# 'display_name': 'CARBON RESISTOR, 510KOHM, 500mW, 5%',
# 'default_code': 'MCRC1/2G514JT-RH',
# 'id': 492}



class Datastore(object):
    def __init__(self, datastore_path):
        self._initialized = False
        self._eng = None

        self._eng = create_engine('sqlite:///{}'.format(datastore_path))
        external_sqltables.Base.metadata.create_all(self._eng)
        self._initialized = True

    def _new_session(self):
        if not self._initialized:
            raise Exception("Datastore is not initialized!")

        db_session = sessionmaker()
        db_session.configure(bind=self._eng)

        return db_session()











