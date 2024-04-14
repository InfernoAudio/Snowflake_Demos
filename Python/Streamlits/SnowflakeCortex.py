#IMPORT SNOWFLAKE LIBARIES
from snowflake.snowpark import Session as sp
from snowflake import cortex as cx
import streamlit as st
#IMPORT "EXTRA" LIBRARIES
import requests
from bs4 import BeautifulSoup

#SET SNOWFLAKE CREDS
snowflake_creds = {
            "account":"YOUR ACCOUNT",
            "user":"YOUR USERNAME",
            "password":"YOUR PASSWORD",            
            "database":"YOUR DB",
            "schema":"YOUR SCHEMA",
            "role":"YOUR ROLE",
            "warehouse":"YOUR WAREHOUSE"
        }      


st.set_page_config(page_title="Snowflake Cortext URL Summarizer")
st.header("Snowflake Cortex URL Summarizer")
#EXTRACT TEXT FROM PUBLIC WEBSITE WITH "GET"
summary_url = st.text_input(label="Enter url to summarize (must be public)")
#IF A URL IS PROVIDED GET THE SUMMARY
if summary_url:
    #ADD A PROGRESS BAR TO SHOW ACTION AND THE CHAT WINDOW
    progress_bar = st.progress(0,text="Requesting Content from URL...")
    chat_out = st.chat_message
    #GET THE URL RESPONSE
    response = requests.get(summary_url)
    #MAKE SOUP
    progress_bar.progress(25,text="Making BeautifulSoup...")           
    soup = BeautifulSoup(response.content,features='html.parser')        
    #CONNECT TO SNOWFLAKE
    progress_bar.progress(50,"Connecting to Snowflake")    
    sf_session = sp.builder.configs(snowflake_creds).create()
    progress_bar.progress(75,text=f"Summarizing {soup.find('title').string}")
    #ADD USER'S ENTRY TO CHAT BOX
    with chat_out(name="user"):
        st.write(f"Please provide a summary of {soup.find('title').string} from URL: {summary_url}")
    #RUN SUMMARY        
    content_summary = cx.Summarize(soup.get_text(),sf_session)    
    progress_bar.progress(100,text="Summary complete")
    #WRITE RESPONSE TO CHAT BOT AND HIDE PROGRESS BAR
    with chat_out(name="ai"):
        st.write(content_summary)
    progress_bar.empty()