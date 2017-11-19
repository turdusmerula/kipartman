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

    def fetch(self, base_filename, category, importItem):
        

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
            i.category = category
            i.comment  = 'NEW IMPORT Timestamp:{:%y-%m-%d %H:%M:%S.%f}'.format(datetime.datetime.now())
            components.append(i)
            print("Name:", row['name'], row['category'],row['description'])
        connection.close()
        return components
        


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











