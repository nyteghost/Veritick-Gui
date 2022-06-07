from veriTableClass import tableShow
import os,sys
import sqlalchemy as sa
from sqlalchemy.engine import URL
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from doorKey import config as cfg
    

### SQL Connection Settings
connection_string = 'Driver={ODBC Driver 17 for SQL Server};''Server='+(cfg['database']['Server'])+';''Database=isolatedsafety;''UID='+(cfg['database']['UID'])+';''PWD='+(cfg['database']['PWD'])+';' 
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
conn = sa.create_engine(connection_url)
rawconn = conn.raw_connection()

unreturned_query = f"EXEC [uspFamUnreturnedDevCheck] " + "147586"  # Checks Unreturned Equipment in SQL by STID
Unreturned = pd.read_sql(unreturned_query , conn)    

dframe = Unreturned



tableShow(dframe)