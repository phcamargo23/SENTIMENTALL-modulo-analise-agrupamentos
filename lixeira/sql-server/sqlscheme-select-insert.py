# -*- coding: utf-8 -*-
import sqlalchemy as sa
import pyodbc
import pandas as pd
# engine = sa.create_engine('mssql+pyodbc://sa:123@PH\SQL/TCC?driver=SQL+Server+Native+Client+10.0')
# engine = sa.create_engine('mssql+pyodbc://sa:123@PH/TCC?driver=SQL+Server+Native+Client+10.0')
# engine = sa.create_engine('mssql+pyodbc://sa:123@PH/TCC')
engine = sa.create_engine('mssql+pyodbc://sa:123@PH/TCC?driver=SQL Server')

# sql = "SELECT TOP 100 destinoEstado AS estado, destinoCidade AS cidade, destinoObjeto AS objeto, destinoTipo AS tipo, aspectos FROM avaliacoesDosTop20AspectosPositivos WHERE aspectos IS NOT NULL ORDER BY newid()"
# df = pd.read_sql(sql, engine)
#
# print df

sql = "select * from teste"
df = pd.read_sql(sql, engine)


# df = pd.DataFrame(columns=('a'))
# df.append('1')

# df = pd.DataFrame({'a': ['A0', 'A1', 'A2', 'A3']},index=[0, 1, 2, 3])

print df
# write the DataFrame to a table in the sql database
df.to_sql("teste", engine, if_exists='append')