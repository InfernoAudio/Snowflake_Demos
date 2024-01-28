#IMPORT LIBARRIES
import pandas
from sqlalchemy import create_engine
from snowflake.snowpark import Session as sp
from snowflake.connector.pandas_tools import write_pandas
#SET SQL SERVER OPTIONS
sql_server_options ={
    "server":"SQLSERVERNAME",
    "database":"DBNAME",
    "table_name":"TABLENAME"
}
#BUILD SQL CONNECTION STRING
sql_server_conn_str = (
        f'mssql+pyodbc:///?odbc_connect='
        f'driver=ODBC Driver 17 for SQL Server;'
        f'server={sql_server_options["server"]};'
        f'database={sql_server_options["database"]};'
        f'trusted_connection=yes;'
    )
# Create an SQLAlchemy engine and connect to SQL Server
sql_server_engine = create_engine(sql_server_conn_str)
#READ DATA
sql_df = pandas.read_sql_table(sql_server_options["table_name"],sql_server_engine)
#CONVERT TO STRING AND RENAME COLUMNS TO UPPER
sql_df = sql_df.astype("string")
sql_df.rename(columns=str.upper,inplace=True)
#SET SNOWFLAKE CREDS
snowflake_creds = {
            "account":"ACCOUNTLOCATOR",
            "user":"USERNAME",
            "password":"PASSWORD",    
            "database":"DATABASE",
            "schema":"SCHEMA",
            "role":"ROLE",
            "warehouse":"WAREHOUSE"
        }      
#CONNECT AND WRITE DATA TO SNOWFLAKE
sf_session = sp.builder.configs(snowflake_creds).create()
#CREATE TABLE AND WRITE DATA, DROP TABLE FIRST IF ALREADY EXISTS
sf_session.write_pandas(sql_df,str.upper(sql_server_options["table_name"]),auto_create_table=True,overwrite=True,table_type='transient')