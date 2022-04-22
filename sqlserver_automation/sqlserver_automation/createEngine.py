import urllib
import sqlalchemy
import pandas as pd
import DatabaseConfig

def runEngine(conn_param):
    params = urllib.parse.quote_plus(conn_param)

    try:
        myeng = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
        myeng.connect()
    except (sqlalchemy.exc.DBAPIError,sqlalchemy.exc.InterfaceError) as err:
        myeng = None
    finally:
        return myeng


        

