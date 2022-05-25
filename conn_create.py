import hashlib
import os.path
import pandas as pd
import sqlalchemy as sa
from sqlalchemy.engine import URL
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from doorKey import config


def open_connection():
    ### SQL Connection Settings
    connection_string = 'Driver={ODBC Driver 17 for SQL Server};''Server='+(config['database']['Server'])+';''Database=isolatedsafety;''UID='+(config['database']['UID'])+';''PWD='+(config['database']['PWD'])+';' 
    connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
    conn = sa.create_engine(connection_url) 
    return conn


def execute_query(sql_query, parameters=None, conn=None):
    """
    Method to query data from Redshift and return pandas dataframe
    Parameters
    ----------
    sql_query : str
        saved SQL query
    parameters : dict, optional
        populates named placeholders in query template. 
    conn : database string URI, optional
        connection created with open_connection()
    Returns
    -------
    df_raw : DataFrame
        Pandas DataFrame with raw data resulting from query
    """

    # If no existing connection object is passed, open a new connection
    new_conn = False
    if conn is None:
        connection = open_connection()
        new_conn = True

    # Hash the query
    query_hash = hashlib.sha1(sql_query.format(parameters).encode()).hexdigest()

    # Create the filepath
    file_path = os.path.join("_cache","{}.csv".format(query_hash))

    # Read the file or execute query 
    if os.path.exists(file_path):
        df_raw = pd.read_csv(file_path)
    else:
        try:
            df_raw = pd.read_sql(sql_query, con=connection, params=parameters)
        except (KeyboardInterrupt, SystemExit):
            connection.close()
        if not os.path.isdir("_cache"):
            os.makedirs("_cache")
        df_raw.to_csv(file_path, index=False)

    # Close single-execution connection
    # if new_conn:
    #     connection.close()

    return df_raw