from . import _export_base

from . import Bomsaway_datastore as bDs

import os

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, MetaData, Table, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select



#Base = declarative_base()


class sqlExport(_export_base.KiPartmanExporter):
    extension = 'db'
    wildcard = 'Bomsaway Sqllite (*.db)|*.db'
    table = None

    def getTables(self, base_filename):
        ds = bDs.Datastore(datastore_file)
        meta = MetaData()
        meta.reflect(bind = ds._eng)
        tables = meta.tables
        return tables

    def setTable(self, table_name):
        table = table_name
    

    def export(self, base_filename, components):

        #TODO: Remove this and sort out what variables are required
        # sys.argv[0]
        # base_dir = os.path.split(sys.argv[0])[0]
        # top_sch = os.path.split(sys.argv[0])[-1]
        # top_name = os.path.splitext(top_sch)[0]

        # base_dir,top_sch,top_name

        #location of Boms-Away DB
        config_dir = os.path.join(os.path.expanduser("~"), '.bomsaway.d')

        _legacy_dir = os.path.join( os.path.expanduser("~"), '.kicadbommgr.d',)
        config_file = os.path.join( config_dir, 'BOMSAway.conf')
        datastore_file = os.path.join( config_dir, 'TEST17W46Abommgr.db')

        Base = declarative_base()


        file_path = '{}.{}'.format(base_filename, self.extension)

        ds = bDs.Datastore(file_path)
        meta = MetaData()
        #TODO: Map kipartman.parts to Bomsaway_components
    # theMRP_ProductItems.to_sql('kipartman_parts',ds._eng,flavor='pysqlite', if_exists='append',index=False)

        #FROM: export sqllight
        # session = sessionmaker()
        # session.configure(bind=ds._eng)
        # s = session()
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











