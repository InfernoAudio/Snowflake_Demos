#IMPORT STREAMLIT LIBRARY
import streamlit as st
#IMPORT SNOWPARK SESSION
from snowflake.snowpark.context import get_active_session
#IMPORT PANDAS
import pandas as pd
 
#CREATE A SESSION VARIABLE
session = get_active_session()
 
#UPDATE THE PAGE CONFIG SETTINGS
st.set_page_config(layout="wide")

##ADD SOME COLUMNS FOR SELECTION BOXES
col1,col2 = st.columns(2)
 
#COL1 = REGION
with col1:    
    region_sql ="""
    SELECT
        REGION_NAME
    FROM
        STREAMLIT_DATA.VW_SALES_DATA
    GROUP BY 
        REGION_NAME
    ORDER BY
        REGION_NAME;    
    """
    region_df = session.sql(region_sql).collect()
    region_name = st.selectbox("Choose a region:",options=region_df)
 
#COL2 = COUNTRY
with col2:
    country_sql=f"""
    SELECT
        COALESCE(COUNTRY_NAME,'ALL') AS ST_COUNTRY_NAME
    FROM
        STREAMLIT_DATA.VW_SALES_DATA
    WHERE
        REGION_NAME = '{region_name}'
    GROUP BY 
        COUNTRY_NAME
    ORDER BY
        COUNTRY_NAME ASC NULLS FIRST;    
    """
    country_df = session.sql(country_sql).collect()
    country_name = st.selectbox("Choose a country:",options=country_df)
 
#SETUP ROW TWO COLUMNS
r2col1,r2col2 = st.columns([1.5,4])
 
#BUILD A BAR CHART
#STEP 1: BUILD SQL - SALES IN MILLIONS BY YEAR,INCLUDE AN INDEX COLUMN FOR CHART BUILDING
sql_bar_chart = f"""
SELECT
    ROW_NUMBER() OVER (ORDER BY ORDER_YEAR) AS DF_IDX,    
    ORDER_YEAR,
    PART_MFG,
    ROUND((TOTAL_SALES / 1000000),3)::NUMERIC(19,3) as SALES_IN_MILLIONS
FROM
    STREAMLIT_DATA.VW_SALES_DATA
WHERE
    REGION_NAME = '{region_name}'
    AND
    COALESCE(COUNTRY_NAME,'ALL')='{country_name}'
ORDER BY
    DF_IDX
"""
#STEP 2: COLLECT THE DATAFRAME
bar_chart_df = session.sql(sql_bar_chart).collect()
#STEP 3: CONVERT TO A PANDAS DATAFRAME
bar_pandas_df = pd.DataFrame(bar_chart_df,columns=["DF_IDX","ORDER_YEAR","PART_MFG","SALES_IN_MILLIONS"]).set_index("DF_IDX")
#STEP 4: CONVERT TO PROPER DATATYPES
bar_pandas_df = bar_pandas_df.astype({"ORDER_YEAR": "object","SALES_IN_MILLIONS":"float","PART_MFG":"object"})

with r2col1:
    #STEP 6: SHOW UNDERLYING DATA
    st.subheader("Underlying Chart Data")
    st.dataframe(data=bar_pandas_df)
with r2col2:
   #STEP 5: CREATE THE CHART
   st.subheader("Total Sales (in Millions) by Year")
   #CREATE THE ALTAIR CHART DATA
    chart = alt.Chart(bar_pandas_df).mark_bar().encode(
        x = alt.X("ORDER_YEAR",title="ORDER YEAR",type="nominal")
       ,y=alt.Y("SALES_IN_MILLIONS",title="SALES IN MILLIONS")
        ,color= alt.Color("PART_MFG",title="PARTS MANUFACTURER")
    )
 
st.altair_chart(chart,use_container_width=True,theme="streamlit")