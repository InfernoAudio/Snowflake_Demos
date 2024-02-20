#IMPORT STREAMLIT LIBRARY
import streamlit as st
#IMPORT SNOWPARK
import snowflake.snowpark as sp
#IMPORT SNOWPARK SESSION
from snowflake.snowpark.context import get_active_session

##CREATE NEW FUNCTION TO TRY GET ACTIVE SESSION FROM SNOWPARK
##OTHERWISE BUILD CONNECTION
def open_session():
    snow_session = None

    try:
      snow_session = get_active_session()
    except:
      #READ CREDS INTO DICTIONARY
        creds = {
            "account":"YOUR ACCOUNT",
            "user":"YOUR USERNAME",
            "password":"YOUR PASSWORD",    
            "database":"YOUR DATABASE",
            "schema":"YOUR SCHEMA",
            "role":"YOUR ROLE",
            "warehouse":"YOUR WAREHOUSE"
        }        
        #BUILD SESSION
        snow_session = sp.Session.builder.configs(creds).create()

    return snow_session


#CREATE A SESSION VARIABLE
session = open_session()

office_locations = {
    "offices":{
        "Bozeman, MT":{
            "Latitude":"45.6779796",
            "Longitude":"-111.0348163"
        },
        "San Mateo, CA":{
            "Latitude":"37.553252",
            "Longitude":"-122.3062339"
        },
        "Bellevue, WA":{
            "Latitude":"47.6183091",
            "Longitude":"-122.1969603"
        },
        "New York, NY":{
            "Latitude":"40.7544099",
            "Longitude":"-73.9856036"
        },
        "Atlanta, GA":{
            "Latitude":"33.8460342",
            "Longitude":"-84.37203"
        }
    }
}

#UPDATE THE PAGE CONFIG SETTINGS
st.set_page_config(layout="wide")

#GIVE THE PAGE A TITLE
st.header("NOAA Weather Station Location")


##ADD SOME COLUMNS FOR SELECTION BOXES
col1,col2,col3 = st.columns([1,1,3])
with col1:
    snow_office = st.selectbox(label="Choose a Snowflake Location:",options=sorted(office_locations["offices"]))
with col2:
    radius = st.selectbox(label="Radius (in miles)",options=[10,15,25,50,100])

#CAPTURE OFFICE LAT/LONG FROM DICT
lat_off = office_locations["offices"][snow_office]["Latitude"]
long_off = office_locations["offices"][snow_office]["Longitude"]

 #GET THE NOAA WEATHER STATIONS WITHIN THE RADIUS SPECIFIED
station_sql = """
SELECT LONGITUDE,LATITUDE FROM ST_DEMO_DB.RAW_DATA.NOAA_STATIONS
WHERE ST_DWITHIN(ST_MAKEPOINT(LONGITUDE,LATITUDE),ST_MAKEPOINT({long},{lat}),{rad}*1609)
"""

#FORMAT THE QUERY AND RETURN DATA FRAME
df_map = session.sql(station_sql.format(long=long_off,lat=lat_off,rad=radius))

#USE LAT/LONG DATA FROM DF TO PLOT WEATHER STATIONS
disp_text = """
Showing NOAA weather stations within {rad} miles of {office} ({lat},{long})
"""
st.write(disp_text.format(rad=radius,office=snow_office,lat=lat_off,long=long_off))
#PLOT STATIONS ON MAP
st.map(df_map)
