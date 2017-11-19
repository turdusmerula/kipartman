#DB Tests
import os,sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, MetaData, Table, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select


sys.argv[0]
base_dir = os.path.split(sys.argv[0])[0]
top_sch = os.path.split(sys.argv[0])[-1]
top_name = os.path.splitext(top_sch)[0]

base_dir,top_sch,top_name

config_dir = os.path.join(os.path.expanduser("~"), '.bomsaway.d')

_legacy_dir = os.path.join( os.path.expanduser("~"), '.kicadbommgr.d',)
config_file = os.path.join( config_dir, 'BOMSAway.conf')
datastore_file = os.path.join( config_dir, 'TEST17W46Abommgr.db')

Base = declarative_base()

# {'name': 'CARBON RESISTOR, 510KOHM, 500mW, 5%',
# 'description': 'CARBON RESISTOR, 510KOHM, 500mW, 5%; Product Range:MCRC Series; Resistance:510kohm; Power Rating:500mW; Resistance Tolerance:  5%; Voltage Rating:350V; Resistor Case Style:Axial Leaded; Resistor Eleme 73K0236 ',
# 'barcode': False,
# 'display_name': 'CARBON RESISTOR, 510KOHM, 500mW, 5%',
# 'default_code': 'MCRC1/2G514JT-RH',
# 'id': 492}

# class MRP_ProductItems(Base):
#     __tablename__ = 'MRP_ProductItems'
#     id = Column(Integer, primary_key=True, autoincrement=False)
#     default_code = Column(String(64), nullable=False, autoincrement=False)
#     name = Column(String(128), nullable=False, autoincrement=False)
#     display_name = Column(String(128), nullable=False, autoincrement=False)
#     description = Column(String(1024), nullable=False, autoincrement=False)
#     barcode = Column(Boolean, nullable=False, autoincrement=False)
#     extend_existing = True


class Datastore(object):
    def __init__(self, datastore_path):
        self._initialized = False
        self._eng = None

        self._eng = create_engine('sqlite:///{}'.format(datastore_path))
        Base.metadata.create_all(self._eng)
        self._initialized = True

    def _new_session(self):
        if not self._initialized:
            raise Exception("Datastore is not initialized!")

        db_session = sessionmaker()
        db_session.configure(bind=self._eng)

        return db_session()



ds = Datastore(datastore_file)
ds._eng.engine.driver
ds._eng.engine.driver

meta = MetaData()
meta.reflect(bind=ds._eng)

[table for table in meta.tables]


connection = ds._eng.connect()
result = connection.execute("select * from Kipartman_Parts")
for row in result:
    print("Name:", row['name'], row['category'],row['description'])
connection.close()


con = ds._eng.connect()
meta = MetaData(ds._eng)

# DROP A TABLE
#meta.tables['Kipartman_Parts'].drop(ds._eng)


# insp = inspect(ds._eng)
# insp.get_table_names()
# insp.get_columns('MRP_ProductItems')



# someMRP_ProductItems = Table('Kipartman_Parts', meta, autoload=True)

# stm = select([someMRP_ProductItems.c.name,]).limit(3)
# rs = con.execute(stm)

# print( rs.fetchall())
# con.close()
