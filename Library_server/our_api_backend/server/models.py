from sqlalchemy import MetaData, Table, Column, Integer, String


metadata = MetaData()

library = Table(
    'table', metadata,
    Column('id', Integer, primary_key=True),
    ...
)
