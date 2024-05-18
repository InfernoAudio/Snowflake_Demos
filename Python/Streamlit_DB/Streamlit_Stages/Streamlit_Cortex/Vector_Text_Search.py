#IMPORT STREAMLIT LIBRARY
import streamlit as st
#IMPORT SNOWPARK
import snowflake.snowpark as sp

st.set_page_config(page_title="Snowflake Vector Text Search",layout="wide")

#READ CREDS INTO DICTIONARY
creds = {
            "account":"YOUR ACCOUNT",
            "user":"YOUR USERNAME",
            "password":"YOUR PASSWORD",    
            "database":"YOUR DB",
            "schema":"YOUR SCHEMA",
            "role":"YOUR ROLE",
            "warehouse":"YOUR WAREHOUSE"
        }            

#CREATE LLM OPTIONS
llm_models = ["snowflake-arctic-embed-m",
              "e5-base-v2"]

#ADD SNOWFLAKE LOGO, HEADER AND LLM CHOOSER
st.image(image="https://www.snowflake.com/wp-content/themes/snowflake/assets/img/brand-guidelines/logo-sno-blue-example.svg")
colHeader = st.columns([3,2])
with colHeader[0]:
    st.header("Snowflake Data Similarity Compare")
with colHeader[1]:    
    curr_model = st.selectbox(label=f"Choose Embed Model for Text Vectorization",options=llm_models)

#BUILD UI
session = sp.Session.builder.configs(creds).create()
colInput = st.columns(4)
with colInput[0]:
    new_cust = st.text_input("Enter a customer name to search for:")
with colInput[2]:
    ttl_score = st.slider("Set Total Score Threshold",min_value=.50, max_value=1.0,value=.90)
with colInput[3]:
    num_results = st.number_input("Max Number of Matches to Show",min_value=1,max_value=10,value=5)

if new_cust:
    new_cust = "\'" + new_cust + "\'"
    curr_model = "\'" + curr_model + "\'"
    sql = f'''
SELECT
    {new_cust} AS "NEW CUSTOMER NAME"
    ,CI.FULL_NAME AS "EXISTING CUSTOMER NAME"
    ,VECTOR_COSINE_SIMILARITY(
        SNOWFLAKE.CORTEX.EMBED_TEXT_768({curr_model},CI.FULL_NAME)
        ,SNOWFLAKE.CORTEX.EMBED_TEXT_768({curr_model},{new_cust})
        ) as "VECTOR SIMILARITY SCORE"
    ,VECTOR_L2_DISTANCE(
        SNOWFLAKE.CORTEX.EMBED_TEXT_768({curr_model},CI.FULL_NAME)
        ,SNOWFLAKE.CORTEX.EMBED_TEXT_768({curr_model},{new_cust})
        ) AS "VECTOR DISTANCE SCORE"
    ,JAROWINKLER_SIMILARITY(CI.FULL_NAME,{new_cust})/100.0 AS "JAROWINKLER SIMILARITY SCORE"
    ,("VECTOR SIMILARITY SCORE" + (1-"VECTOR DISTANCE SCORE") + "JAROWINKLER SIMILARITY SCORE") / 3 AS "CALCULATED SUMMARY SCORE"
FROM
    ST_DEMO_DB.RAW_DATA.CUSTOMER_INFO as CI
WHERE
    "CALCULATED SUMMARY SCORE" >= {ttl_score}
QUALIFY
    RANK() OVER(ORDER BY "CALCULATED SUMMARY SCORE" DESC) <= {num_results}
'''
        
    df = session.sql(sql)
    st.dataframe(df,use_container_width=True)



