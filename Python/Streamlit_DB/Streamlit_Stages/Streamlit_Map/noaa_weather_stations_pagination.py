#IMPORT STREAMLIT LIBRARY
import streamlit as st
#IMPORT SNOWPARK
import snowflake.snowpark as sp
#IMPORT SNOWPARK SESSION
from snowflake.snowpark.context import get_active_session
#IMPORT PANDAS
import pandas as pd

##CREATE NEW FUNCTION TO TRY GET ACTIVE SESSION FROM SNOWPARK
##OTHERWISE BUILD CONNECTION
def open_session():
    snow_session = None

    try:
      snow_session = get_active_session()
    except:
      #READ CREDS INTO DICTIONARY
        creds = {
            "account":"",
            "user":"",
            "password":"",    
            "database":"",
            "schema":"",
            "role":"",
            "warehouse":""
        }        
        #BUILD SESSION
        snow_session = sp.Session.builder.configs(creds).create()

    return snow_session

##DEFINE SNOWFLAKE OFFICES
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


##DATA LOADER
@st.cache_data(show_spinner=False)
def map_data_loader(lat_off,long_off,rad):    

    #GET THE NOAA WEATHER STATIONS WITHIN THE RADIUS SPECIFIED
    station_sql = """
    SELECT LONGITUDE,LATITUDE,
    ID AS STATION_ID,
    ST_DISTANCE(ST_MAKEPOINT(LONGITUDE,LATITUDE),ST_MAKEPOINT({long},{lat}))/1609::NUMBER(8,2) AS DISTANCE_IN_MILES
    FROM ST_DEMO_DB.RAW_DATA.NOAA_STATIONS
    WHERE ST_DWITHIN(ST_MAKEPOINT(LONGITUDE,LATITUDE),ST_MAKEPOINT({long},{lat}),{rad}*1609)
    ORDER BY DISTANCE_IN_MILES
    """

    #FORMAT THE QUERY AND RETURN DATA FRAME AS PANDAS
    df_map = session.sql(station_sql.format(long=long_off,lat=lat_off,rad=radius)).to_pandas()    

    return df_map

##DATA SPLITTER
def split_df(input_df,rows):
    df = [input_df.loc[i : i + rows - 1, :] for i in range(0, len(input_df), rows)]
    return df

#CREATE A SESSION VARIABLE
session = open_session()


#UPDATE THE PAGE CONFIG SETTINGS
st.set_page_config(layout="wide")

#GIVE THE PAGE A TITLE
st.header("NOAA Weather Station Location")


##ADD SOME COLUMNS FOR SELECTION BOXES
col1,col2,col3 = st.columns([1,1,3])
with col1:
    snow_office = st.selectbox(label="Choose a Snowflake Location:",options=sorted(office_locations["offices"]))
with col2:
    radius = st.selectbox(label="Radius (in miles)",options=[10,15,25,50,100,250,500])

#CAPTURE OFFICE LAT/LONG FROM DICT
    lat_off = office_locations["offices"][snow_office]["Latitude"]
    long_off = office_locations["offices"][snow_office]["Longitude"]

#LOAD THE MAPPING DF
df_map = map_data_loader(lat_off,long_off,radius)

#USE LAT/LONG DATA FROM DF TO PLOT WEATHER STATIONS
disp_text = """
Showing NOAA weather stations within {rad} miles of {office} ({lat},{long})
"""
st.write(disp_text.format(rad=radius,office=snow_office,lat=lat_off,long=long_off))

app_cols = st.columns(2)

with app_cols[0]:
    #DISPLAY MAP
    st.map(df_map,use_container_width=True)
with app_cols[1]:
    #ADD PAGINATION CONTROLS
    pg_menu = st.columns([4,1,1])
    #ADD BATCH SIZE PICKER
    with pg_menu[2]:
        pg_size = st.selectbox("Page Size",options=[10,25,50,100])
    #ADD PAGE PICKER
    with pg_menu[1]:
        total_pages = (
        int(len(df_map) / pg_size) if int(len(df_map) / pg_size) > 0 else 1
        )
        current_page = st.number_input(
            "Page", min_value=1, max_value=total_pages, step=1
        )
    with pg_menu[0]:
        #DISPLAY CURRENT PAGE
        st.markdown(f"Page **{current_page}** of **{total_pages}** ")
    #PAGINATE UNDERLYING DATA
    df_chart = split_df(df_map,pg_size)
    #DISPLAY DATA
    st.dataframe(df_chart[current_page-1],use_container_width=True)    
