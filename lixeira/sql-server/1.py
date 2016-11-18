# -*- coding: utf-8 -*-
print 'inicio'
import pyodbc
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=PH\SQL;DATABASE=TCC;UID=sa;PWD=123')
cursor = cnxn.cursor()
# cursor.execute("SELECT TOP 100 destinoEstado AS estado, destinoCidade AS cidade, destinoObjeto AS objeto, aspectos FROM avaliacoesDosTop20AspectosPositivos WHERE aspectos IS NOT NULL ORDER BY newid()")
#
# rows = cursor.fetchall()
# for row in rows:
#     print row.estado

import pandas as pd

sql = "SELECT TOP 100 destinoEstado AS estado, destinoCidade AS cidade, destinoObjeto AS objeto, destinoTipo AS tipo, aspectos FROM avaliacoesDosTop20AspectosPositivos WHERE aspectos IS NOT NULL ORDER BY newid()"
df = pd.read_sql(sql, cnxn)

print df