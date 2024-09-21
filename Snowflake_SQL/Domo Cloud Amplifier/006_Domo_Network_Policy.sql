USE ROLE ACCOUNTADMIN;
CREATE OR REPLACE NETWORK POLICY DOMO_INBOUND_NETWORK_POLICY
    ALLOWED_IP_LIST = (
         '3.214.145.64/27'
        ,'54.208.87.122/32'
        ,'54.208.94.194/32'
        ,'54.208.95.167/32'
        ,'54.208.95.237/32'
        ,'34.198.214.100'
        ,'34.202.52.248'
        ,'13.92.125.193/32'
        ,'40.76.8.174/32'
        ,'35.82.136.240/28'
        ,'52.62.103.83/32'
        ,'15.222.16.24/29'
        ,'52.18.90.222/32'
        ,'54.168.46.79/32'
    )
COMMENT = 'Network policy for Domo Service Accounts'