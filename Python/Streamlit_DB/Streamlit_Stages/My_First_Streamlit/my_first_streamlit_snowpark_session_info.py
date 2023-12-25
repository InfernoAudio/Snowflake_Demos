#IMPORT STREAMLIT LIBRARY
import streamlit as st
#IMPORT SNOWPARK SESSION
from snowflake.snowpark.context import get_active_session
 
#CREATE A SESSION VARIABLE
session = get_active_session()
 
#WRITE THE HEADER
st.header("My First Streamlit App in Snowflake")
 
#COLLECT SESSION INFORMATION VARIABLES
current_db = session.get_current_database()
current_schema = session.get_current_schema()
current_warehouse = session.get_current_database()
current_role = session.get_current_role()
 
#WRITE TO SCREEN
st.write(f"Current Database: {current_db}")
st.write(f"Current Schema: {current_schema}")
st.write(f"Current Warehouse: {current_warehouse}")
st.write(f"Current Role: {current_role}")

##COLLECT SAME INFO FROM SNOWFLAKE QUERY
#BUILD SQL COMMAND
sql = """
SELECT
    CURRENT_DATABASE() as current_database
    ,CURRENT_SCHEMA() as current_schema
    ,CURRENT_WAREHOUSE() as current_warehouse
    ,CURRENT_ROLE() as current_role;
"""
 
#QUERY SNOWFLAKE
df = session.sql(sql).collect()
 
#WRITE TO SCREEN IN STREAMLIT DATAFRAME
st.dataframe(data=df)