from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Sequence
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///inventory.db')
metadata = MetaData()
table = Table('items', metadata, autoload=True, autoload_with=engine)

s = select([table])
my_inventory = engine.execute(s)
inventory = []
for i in my_inventory:
    inventory.append(i)

order = []
