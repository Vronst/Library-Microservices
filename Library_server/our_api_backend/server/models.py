from sqlalchemy import MetaData, Table, Column, Integer, String


metadata: MetaData = MetaData()

library: Table = Table(
    'table', metadata,
    Column('id', Integer, primary_key=True),
    ...
)
