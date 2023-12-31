/************************************************
* 001_STREAMLIT_SETUP
* 
* Creates Snowflake objects needed to run
* sample Streamlit apps natively
*
* 20231217     EHeilman     Initial Setup
* 
************************************************/

/*CREATE STANDALONE STREAMLIT DB; XFER TO ST_DEMO_ROLE*/
USE ROLE ACCOUNTADMIN;
/*CREATE NEW STREAMLIT DB*/
CREATE DATABASE STREAMLIT_DB;
GRANT OWNERSHIP ON DATABASE STREAMLIT_DB
    TO ROLE ST_DEMO_ROLE;

/*CREATE STANDALONE STREAMLIT VWH; XFER TO ST_DEMO_ROLE*/	
CREATE WAREHOUSE STREAMLIT_XS_WH
    WAREHOUSE_SIZE=XSMALL;
GRANT OWNERSHIP ON WAREHOUSE STREAMLIT_XS_WH
    TO ROLE ST_DEMO_ROLE;
	
/*CREATE SCHEMA AND STAGES*/
USE ROLE ST_DEMO_ROLE;
/*SWTICH DB AND WAREHOUSE*/
USE DATABASE STREAMLIT_DB;
USE WAREHOUSE STREAMLIT_XS_WH;
/*CREATE NEW SCHEMA FOR STAGES*/
CREATE SCHEMA STREAMLIT_STAGES;
/*SWITCH TO SCHEMA*/
USE SCHEMA STREAMLIT_STAGES;
/*CREATE STAGE WITH DIRECTORY*/
CREATE STAGE MY_FIRST_STREAMLIT_STG
    DIRECTORY = (ENABLE=TRUE);
/*CREATE NEW APPS SCHEMA*/
CREATE SCHEMA STREAMLIT_APPS;


/*CREATE STREAMLIT APP*/
CREATE STREAMLIT MY_FIRST_STREAMLIT
    ROOT_LOCATION = '@STREAMLIT_DB.STREAMLIT_STAGES.MY_FIRST_STREAMLIT_STG'
    MAIN_FILE = 'my_first_streamlit.py'
    QUERY_WAREHOUSE = STREAMLIT_XS_WH
    COMMENT = 'Streamlit testing app';
	
/*GRANT PRIVILEGES TO APP USERS ROLE TO RUN APP*/
USE SCHEMA STREAMLIT_DB.STREAMLIT_APPS;
GRANT USAGE ON STREAMLIT MY_FIRST_STREAMLIT TO ROLE ST_APP_USERS;

USE DATABASE STREAMLIT_DB;
GRANT USAGE ON DATABASE STREAMLIT_DB TO ROLE ST_APP_USERS;

GRANT USAGE ON SCHEMA STREAMLIT_APPS TO ROLE ST_APP_USERS;