USE ROLE ACCOUNTADMIN;
USE WAREHOUSE COMPUTE_WH;

/*CREATE TEMP TABLE TO HOLD ROLE HIERARCHY*/
CREATE OR REPLACE TEMPORARY TABLE ROLE_HIER(CHILD_ROLE STRING,PARENT_ROLE STRING);
INSERT INTO ROLE_HIER(CHILD_ROLE,PARENT_ROLE)
VALUES
('ST_DEV_MGR','ST_MGR'),
('ST_ANLY_MGR','ST_MGR'),
('ST_DEV','ST_DEV_MGR'),
('ST_ANLY','ST_ANLY_MGR'),
('ST_MGR','SYSADMIN'),
('ST_CORTEX_USERS','ST_DEV'),
('ST_CORTEX_USERS','ST_ANLY');

/*CREATE ROLES IF NOT ALREADY IN THE ACCOUNT*/
DECLARE
    DYN_SQL STRING;
BEGIN
    LET rsRoles RESULTSET :=(
        SELECT ROLE_NAME FROM(
            SELECT CHILD_ROLE AS ROLE_NAME FROM ROLE_HIER
            UNION SELECT PARENT_ROLE FROM ROLE_HIER
            ) GROUP BY ROLE_NAME
        );
    LET cRoles CURSOR for rsRoles;
    FOR r IN cRoles DO
        DYN_SQL := 'CREATE ROLE IF NOT EXISTS '|| r.ROLE_NAME;
        EXECUTE IMMEDIATE(:DYN_SQL);
    END FOR;
END;

/*GRANT CHILD ROLES TO PARENT ROLES*/
DECLARE
    DYN_SQL STRING;
BEGIN
    LET rsRoles RESULTSET :=(
        SELECT CHILD_ROLE,PARENT_ROLE FROM ROLE_HIER
        GROUP BY ALL
        );
    LET cRoles CURSOR for rsRoles;
    FOR r IN cRoles DO
        DYN_SQL := CONCAT('GRANT ROLE ',r.CHILD_ROLE, ' TO ROLE ',r.PARENT_ROLE);        
        EXECUTE IMMEDIATE(:DYN_SQL);
    END FOR;
END;