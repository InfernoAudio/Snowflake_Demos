/*****************************************************
*     005_CLONE_SAMPLE_DATA.sql
*
*     20240529     EHEILMAN     Initial Setup
*****************************************************/

/*************************************
* CREATE COPIES OF DATA FROM SNOWFLAKE SAMPLES
* INTO DOMO_READ_SCH FOR DEMO 
**************************************/

USE ROLE DOMO_ADMIN_ROLE;
USE DATABASE DOMO_DB;
USE SCHEMA DOMO_READ_SCH;
USE WAREHOUSE DOMO_WRITE_XS_WH;

SET TARGET_DB = 'DOMO_DB';
SET TARGET_SCH = 'DOMO_READ_SCH';

DECLARE
    DYN_SQL STRING;
BEGIN
    LET rsTables RESULTSET :=(
        SELECT
            CONCAT_WS('.',TABLE_CATALOG,TABLE_SCHEMA,TABLE_NAME) AS SRC_TBL,
            CONCAT_WS('.',$TARGET_DB,$TARGET_SCH,TABLE_NAME) AS TGT_TBL
            FROM SNOWFLAKE_SAMPLE_DATA.INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = 'TPCH_SF1'
        );
    LET cTables CURSOR for rsTables;
    FOR t IN cTables DO
        DYN_SQL := 'CREATE OR REPLACE TABLE '|| t.TGT_TBL || ' AS SELECT * FROM ' || t.SRC_TBL;
        EXECUTE IMMEDIATE(:DYN_SQL);
    END FOR;
END;
