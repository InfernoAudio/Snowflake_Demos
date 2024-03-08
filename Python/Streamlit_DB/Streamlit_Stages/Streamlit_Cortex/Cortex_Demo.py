#IMPORT STREAMLIT LIBRARY
import streamlit as st
#IMPORT SNOWPARK
import snowflake.snowpark as sp
#IMPORT SNOWPARK SESSION
from snowflake.snowpark.context import get_active_session

##CREATE NEW FUNCTION TO TRY GET ACTIVE SESSION FROM SNOWPARK
##OTHERWISE BUILD CONNECTION
def open_session():
    snow_session = None

    try:
      snow_session = get_active_session()
    except:
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
        #BUILD SESSION
        snow_session = sp.Session.builder.configs(creds).create()

    return snow_session


#CREATE A SESSION VARIABLE
session = open_session()

#CREATE LANGUAGE DICT
lang_code = {"English":"en",
             "French":"fr",
             "German":"de",
             "Italian":"it",
             "Japanese":"ja",
             "Korean":"ko",
             "Polish":"pl",
             "Portuguese":"pt",
             "Russian":"ru",
             "Spanish":"es",
             "Swedish":"sv"
            }

#CREATE LLM OPTIONS
llm_models = ["llama2-70b-chat",
              "mistral-large",
              "mixtral-8x7b",
              "mistral-7b",
              "gemma-7b"]

#CORTEX TRANSLATE FUNCTION
def cortex_translate(src_text,src_lang,tgt_lang):
    src_text = src_text.replace("'","\\'")
    src_lang_cd = lang_code[src_lang]
    tgt_lang_cd = lang_code[tgt_lang]
    trans_sql = f"""
    SELECT SNOWFLAKE.CORTEX.TRANSLATE('{src_text}','{src_lang_cd}','{tgt_lang_cd}')
    """
    tgt_text = session.sql(trans_sql).collect()[0][0]

    return tgt_text

def cortex_complete(model_name,prompt):
    prompt = prompt.replace("'","\\'")
    comp_sql = f"""
    SELECT SNOWFLAKE.CORTEX.COMPLETE('{model_name}','{prompt}')    
    """
    comp_text = session.sql(comp_sql).collect()[0][0]

    return comp_text

def cortex_summarize(text):
    text = text.replace("'","\\'")
    summ_sql = f"""
    SELECT SNOWFLAKE.CORTEX.SUMMARIZE('{text}') LIMIT 1
    """
    summ_txt = session.sql(summ_sql).collect()[0][0]

    return summ_txt

#START APP
st.header("Snowflake Cortex Demo")

#SET TABS
tbTranslate,tbComplete,tbSummarize = st.tabs(["Translate","Complete","Summarize"])
#BUILD UI
with tbTranslate:    
    colLang = st.columns(2)
    with colLang[0]:
        src_lang = st.selectbox(label="Choose Source Language",options=dict(sorted(lang_code.items())))
    with colLang[1]:
        tgt_lang = st.selectbox(label="Choose Target Language",options=dict(sorted(lang_code.items())))
    colTrans = st.columns(2)
    with colTrans[0]:
        src_text = st.text_area(label="Enter Source Text")
    with colTrans[1]:        
        tgt_text = cortex_translate(src_text,src_lang,tgt_lang)        
        st.text_area(label="Translation",value=tgt_text)

#COMPLETE
with tbComplete:
    llm_name = st.selectbox(label="Choose an LLM",options=llm_models)
    comp_question = st.text_input(label="Enter your chat prompt:")
    if comp_question:
        comp_answer = cortex_complete(llm_name,comp_question)
        st.write("Snowflake Response:")
        st.write(comp_answer)
#SUMMARIZE
with tbSummarize:
    txt_to_summ = st.text_area(label="Enter text to Summarize:")
    if txt_to_summ:
        st.write(cortex_summarize(txt_to_summ))