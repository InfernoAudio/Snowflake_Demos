USE ROLE ST_DEMO_ROLE;
USE SCHEMA ST_DEMO_DB.RAW_DATA;
USE WAREHOUSE ST_DEMO_XS_WH;


/*CREATE A SAMPLE DATA SET*/
SET MODEL_NAME = 'snowflake-arctic';

SELECT SNOWFLAKE.CORTEX.COMPLETE($MODEL_NAME,'GENERATE A SNOWFLAKE SQL STATEMENT TO CREATE OR REPLACE A TRANSIENT TABLE IN ST_DEMO_DB.RAW_DATA SCHEMA CONTAINING AUTOINCREMENTING CUSTOMER ID called CUST_ID, FIRST NAME, LAST NAME AND FULL NAME WITH DEFAULT VALUE OF CONCAT_WS(\' \',FIRST NAME,LAST NAME). NAME TABLE CUSTOMER_INFO INCLUDE INSERT SCRIPT TO POPULATE 25 SAMPLE RECORDS. WRITE THE SQL STATEMENTS ONLY, NO EXPLANATIONS AND FORMATTED TO RUN NATIVELY IN SNOWSIGHT. EXCLUDE ANY FOMATTING CODE');


-- Create or replace transient table in ST_DEMO_DB.RAW_DATA schema
CREATE OR REPLACE TRANSIENT TABLE ST_DEMO_DB.RAW_DATA.CUSTOMER_INFO (
  CUST_ID INT AUTOINCREMENT,
  FIRST_NAME STRING,
  LAST_NAME STRING,
  FULL_NAME STRING DEFAULT CONCAT_WS(' ', FIRST_NAME, LAST_NAME)
);

-- Insert script to populate 25 sample records
INSERT INTO ST_DEMO_DB.RAW_DATA.CUSTOMER_INFO (FIRST_NAME, LAST_NAME)
VALUES
('John', 'Doe'),
('Jane', 'Doe'),
('Alice', 'Smith'),
('Bob', 'Smith'),
('Charlie', 'Johnson'),
('David', 'Johnson'),
('Evelyn', 'Brown'),
('Frank', 'Brown'),
('Grace', 'Davis'),
('Henry', 'Davis'),
('Isabella', 'Miller'),
('Jack', 'Miller'),
('Kate', 'Wilson'),
('Larry', 'Wilson'),
('Mary', 'Taylor'),
('Nathan', 'Taylor'),
('Olivia', 'Anderson'),
('Peter', 'Anderson'),
('Quinn', 'Thomas'),
('Rachel', 'Thomas'),
('Sophia', 'Jackson'),
('Thomas', 'Jackson'),
('Victoria', 'White'),
('William', 'White'),
('Xavier', 'Harris'),
('Yvonne', 'Harris'),
('Zoe', 'Martin');

      


SET VECT_MDL_NM = 'snowflake-arctic-embed-m';
SET NEW_CUST = 'Petey Andersen';
SET TTL_SCORE = .50;
SET MAX_MATCH = 5;
SELECT
    $NEW_CUST AS "NEW CUSTOMER NAME",
    CI.FULL_NAME AS "EXISTING CUSTOMER NAME",
    VECTOR_COSINE_SIMILARITY(
        SNOWFLAKE.CORTEX.EMBED_TEXT_768($VECT_MDL_NM,CI.FULL_NAME)
        ,SNOWFLAKE.CORTEX.EMBED_TEXT_768($VECT_MDL_NM,$NEW_CUST)
        ) as "VECTOR SIMILARITY SCORE"
    ,VECTOR_L2_DISTANCE(
        SNOWFLAKE.CORTEX.EMBED_TEXT_768($VECT_MDL_NM,CI.FULL_NAME)
        ,SNOWFLAKE.CORTEX.EMBED_TEXT_768($VECT_MDL_NM,$NEW_CUST)
        ) AS "VECTOR DISTANCE SCORE"
    ,JAROWINKLER_SIMILARITY(CI.FULL_NAME,$NEW_CUST)/100.0 AS "JAROWINKLER SIMILARITY SCORE"
    ,("VECTOR SIMILARITY SCORE" + (1-"VECTOR DISTANCE SCORE") + "JAROWINKLER SIMILARITY SCORE") / 3 AS "CALCULATED SUMMARY SCORE"
FROM
    CUSTOMER_INFO as CI
WHERE
    "CALCULATED SUMMARY SCORE" >= $TTL_SCORE
QUALIFY
    RANK() OVER(ORDER BY "CALCULATED SUMMARY SCORE" DESC) <= $MAX_MATCH;
