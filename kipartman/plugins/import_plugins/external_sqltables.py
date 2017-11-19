from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

#TODO fully/automaticall covert kipartman part to table schema
# Have only implemented a few fields to test
class Kipartman_Parts(Base):
    __tablename__ = 'Kipartman_Parts'
    id = Column(Integer,
            primary_key=True, 
            autoincrement=False)
    comment = Column(String(1024), 
                nullable=False,
                autoincrement=False)
    name = Column(String(128),
                nullable=False,
                autoincrement=False)
    category = Column(String(128),
                nullable=False,
                autoincrement=False)
    description = Column(String(1024),
                nullable=False,
                autoincrement=False)
    extend_existing = True
