/*****************************************************
*     003_Service_Account_Setup.sql
*
*     20240529     EHEILMAN     Initial Setup
*****************************************************/

/*************************************
* CREATE TWO SERVICE ACCOUNTS
* --ONE FOR READ/ONE FOR WRITE
* --GRANT APPROPRIATE DOMO ROLES TO ACCOUNTS
**************************************/


/*DOMO READ SERVICE ACCOUNT */
USE ROLE SECURITYADMIN;
CREATE USER DOMO_READER_SVC_01
    PASSWORD = 'STRONG PASSWORD'
    DISPLAY_NAME = 'DOMO READER SERVICE ACCOUNT'
    FIRST_NAME = 'DOMO READER'
    LAST_NAME = 'SERVICE ACCOUNT'
    DEFAULT_ROLE = 'DOMO_READER_ROLE'
    DEFAULT_WAREHOUSE = 'DOMO_READ_XS_WH';
GRANT ROLE DOMO_READER_ROLE TO USER DOMO_READER_SVC_01;

/*DOMO READ WRITE ACCOUNT */
USE ROLE SECURITYADMIN;
CREATE USER DOMO_WRITER_SVC_01
    PASSWORD = 'STRONG PASSWORD'
    DISPLAY_NAME = 'DOMO WRITER SERVICE ACCOUNT'
    FIRST_NAME = 'DOMO WRITER'
    LAST_NAME = 'SERVICE ACCOUNT'
    DEFAULT_ROLE = 'DOMO_WRITER_ROLE'
    DEFAULT_WAREHOUSE = 'DOMO_WRITE_XS_WH';
GRANT ROLE DOMO_WRITER_ROLE TO USER DOMO_WRITER_SVC_01;