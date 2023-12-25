#IMPORT STREAMLIT LIBRARY
import streamlit as st
#IMPORT SNOWPARK SESSION
from snowflake.snowpark.context import get_active_session
 
#CREATE A SESSION VARIABLE
session = get_active_session()
 
#UPDATE THE PAGE CONFIG SETTINGS
st.set_page_config(layout="wide")

#ADD THE SIDEBAR AND SELECT BOX
with st.sidebar:
    #SET THE SQL COMMAND TO LOAD THE DATAFRAME
    selectbox_sql = """
        SELECT EVT_TYPE
        FROM ST_DEMO_DB.RAW_DATA.TBL_EVT_LOG
        GROUP BY EVT_TYPE;
        """
    #COLLECT THE DATA VALUES INTO A DF
    selectbox_df = session.sql(selectbox_sql).collect()
 
    #CREATE THE SELECT BOX; STORE SELECTED VALUE IN VAR_EVT_TYPE
    var_evt_type=st.selectbox(label="Select Event Type:",options=selectbox_df)
    
    
#BUILD SQL COMMAND
sql = """
SELECT
    EVT_TYPE as TYPE,
    EVT_DESC as DESCRIPTION,
    EVT_TIMESTAMP as TIMESTAMP,
    EVT_USERNAME as USER    
FROM
    ST_DEMO_DB.RAW_DATA.TBL_EVT_LOG
WHERE
    EVT_TYPE = '{evt_typ}'
"""
#FORMAT SQL STRING WITH VARIABLE
sql = sql.format(evt_typ=var_evt_type)
 
#QUERY SNOWFLAKE
df = session.sql(sql).collect()
 
#WRITE TO SCREEN
st.dataframe(data=df,use_container_width=True)    