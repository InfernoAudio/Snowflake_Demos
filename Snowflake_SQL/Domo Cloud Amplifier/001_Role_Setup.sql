/*****************************************************
*     001_ROLE_SETUP.SQL
*
*     20240529     EHEILMAN     Initial Setup
*****************************************************/

/*********************************
CREATE NEW ROLES FOR DOMO
--CREATE DOMO ADMIN ROLE
--READ/WRITE ROLES ROLL UP TO ADMIN
*********************************/

USE ROLE SECURITYADMIN;

/*DOMO READ ROLE */
CREATE OR REPLACE ROLE DOMO_READER_ROLE;
/*DOMO WRITE ROLE */
CREATE OR REPLACE ROLE DOMO_WRITER_ROLE;
/*DOMO ADMIN ROLE */
CREATE OR REPLACE ROLE DOMO_ADMIN_ROLE;
/*CREATE HIERARCHY */
GRANT ROLE DOMO_READER_ROLE TO ROLE DOMO_ADMIN_ROLE;
GRANT ROLE DOMO_WRITER_ROLE TO ROLE DOMO_ADMIN_ROLE;
GRANT ROLE DOMO_ADMIN_ROLE TO ROLE SYSADMIN;

/*ASSUME CURRENT USER WILL BE DOMO ADMIN */
SET CURR_USER = CURRENT_USER();
GRANT ROLE DOMO_ADMIN_ROLE TO USER IDENTIFIER($CURR_USER);
UNSET CURR_USER;