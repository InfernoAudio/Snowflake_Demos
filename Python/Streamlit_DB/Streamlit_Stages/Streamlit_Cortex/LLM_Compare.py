#IMPORT STREAMLIT LIBRARY
import streamlit as st
#IMPORT SNOWPARK
import snowflake.snowpark as sp
#IMPORT COMPLETE FUNCTION FROM SNOWFLAKE CORTEX
from snowflake.cortex import Complete

st.set_page_config(page_title="Snowflake LLM Comparisons",layout="wide")

#READ CREDS INTO DICTIONARY
creds = creds = {
            "account":"YOUR ACCOUNT",
            "user":"YOUR USERNAME",
            "password":"YOUR PASSWORD",    
            "database":"YOUR DB",
            "schema":"YOUR SCHEMA",
            "role":"YOUR ROLE",
            "warehouse":"YOUR WAREHOUSE"
        }            

#CREATE LLM OPTIONS
llm_models = ["snowflake-arctic",
              "reka-flash",
              "llama2-70b-chat",
              "mistral-large",
              "mixtral-8x7b",
              "mistral-7b",
              "gemma-7b"]

#ADD SNOWFLAKE LOGO, HEADER AND LLM CHOOSER
st.image(image="https://www.snowflake.com/wp-content/themes/snowflake/assets/img/brand-guidelines/logo-sno-blue-example.svg")
colHeader = st.columns([3,2])
with colHeader[0]:
    st.header("Snowflake LLM Compare Demo")
with colHeader[1]:
    mx_llms = 5
    cntLlm = st.number_input(label="Choose number of models to compare",min_value=1,max_value=mx_llms)

#INITIALIZE THE SESSION STATE
if "cntLLM" not in st.session_state:
    st.session_state.cntLLM = 0
if cntLlm != st.session_state.cntLLM:
    #CLEAR ANY EXISTING STATES
    x=0
    while x < mx_llms:
        chatHist = f"chatHist_{x}"
        if chatHist in st.session_state:
            del st.session_state[chatHist]
        if x < cntLlm and chatHist not in st.session_state:
            st.session_state[chatHist] = []
        x+=1
    st.session_state.cntLLM = cntLlm

#BUILD UI
#ENTER PROMPT FIRST
llm = list(range(0,cntLlm))
colChat = st.columns(cntLlm)
prompt = st.chat_input("What's up?")
if prompt:
    session = sp.Session.builder.configs(creds).create()
x=0
while x < cntLlm:
    with colChat[x]:
        chatHist = f"chatHist_{x}"
        llm[x] = st.selectbox(label=f"Choose LLM Model {x+1} ",options=llm_models,key=f"llm_{x}",index=x)  
        for m in st.session_state[chatHist]:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])
        if prompt:            
            st.chat_message("user").markdown(prompt)
            st.session_state[chatHist].append({"role":"user","content":prompt})
            with st.chat_message("assistant"):                
                resp = Complete(llm[x],prompt,session) 
                st.markdown(resp)
                st.session_state[chatHist].append({"role":"assistant","content":resp})
    x+=1