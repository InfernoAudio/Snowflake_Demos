/************************************************
* 001_INITIAL_SETUP
* 
* Creates demo Snowflake objects
*
* 20231217     EHeilman     Initial Setup
* 
************************************************/


/*CREATE NEW ROLE(S)*/
USE ROLE SECURITYADMIN;
CREATE OR REPLACE ROLE ST_DEMO_ROLE;
CREATE OR REPLACE ROLE ST_APP_USERS;

/*ASSIGN CURRENT USER TO ROLES*/
SET current_user = CURRENT_USER();
GRANT ROLE ST_DEMO_ROLE TO USER IDENTIFIER($current_user);
GRANT ROLE ST_APP_USERS TO USER IDENTIFIER($current_user);

/*SET ROLE HIERARCHY*/
GRANT ROLE ST_DEMO_ROLE TO ROLE SYSADMIN;
GRANT ROLE ST_APP_USERS TO ROLE ST_DEMO_ROLE;


/*CREATE XS VIRTUAL WAREHOUSE*/
USE ROLE ACCOUNTADMIN;
CREATE OR REPLACE WAREHOUSE ST_DEMO_XS_WH
    WAREHOUSE_SIZE = XSMALL
    MIN_CLUSTER_COUNT = 1
    MAX_CLUSTER_COUNT = 1
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    ;
	
/*TRANSFER VWH OWNERSHIP TO ST_DEMO_ROLE*/
GRANT OWNERSHIP ON WAREHOUSE ST_DEMO_XS_WH TO ROLE ST_DEMO_ROLE;

/*GRANT USAGE TO THE APP USERS ROLE*/	
GRANT USAGE ON WAREHOUSE ST_DEMO_XS_WH TO ROLE ST_APP_USERS;

/*SETUP DEMO DATABASE AND XFER TO ST_DEMO_ROLE*/
USE ROLE ACCOUNTADMIN;
CREATE OR REPLACE DATABASE ST_DEMO_DB;
GRANT OWNERSHIP ON DATABASE ST_DEMO_DB TO ROLE ST_DEMO_ROLE;


/*CREATE SCHEMAS FOR RAW DATA AND INTERNAL STAGES*/
USE ROLE ST_DEMO_ROLE;
USE DATABASE ST_DEMO_DB;
CREATE OR REPLACE SCHEMA ST_INTERNAL_STAGES;
CREATE OR REPLACE SCHEMA RAW_DATA;

/*CREATE A STAGE FOR LANDING DATA*/
CREATE OR REPLACE STAGE ST_INTERNAL_STAGES.ST_DEMO_STAGE
    DIRECTORY = (ENABLE=TRUE);

/*CREATE SAMPLE EVENT LOG TABLE AND PROC*/
USE SCHEMA ST_DEMO_DB.RAW_DATA;
	
/*CREATE TABLE*/
CREATE TABLE TBL_EVT_LOG(
	evt_id INT AUTOINCREMENT START WITH 1 INCREMENT BY 1
	,evt_type VARCHAR(10)
	,evt_desc VARCHAR(1000)
	,evt_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP()
	,evt_username VARCHAR(50) DEFAULT CURRENT_USER()
	);

/*CREATE STORED PROC WITH OPTIONAL EVT_TYPE PARAMETER*/	
CREATE OR REPLACE PROCEDURE USP_EVT_LOG("EVT_DESC" VARCHAR(1000),"EVT_TYPE" VARCHAR(10) DEFAULT NULL)
RETURNS BOOLEAN
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
BEGIN
    INSERT INTO TBL_EVT_LOG(EVT_TYPE,EVT_DESC)
    VALUES(COALESCE(:EVT_TYPE,'INFO'),:EVT_DESC);
    RETURN TRUE;
END
$$;	
