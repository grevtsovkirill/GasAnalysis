import pandas as pd
import numpy as np

#define geographical constraints
minlat=53.553444
maxlat=53.667341
minlon=9.851884
maxlon=9.995315

stations=pd.read_csv("data/stations.csv")

def get_stations(stations=stations):    
    stations_on_route=stations.loc[
             (stations.latitude>minlat)&(stations.latitude<maxlat)&
            (stations.longitude>minlon)&(stations.longitude<maxlon)]
    return stations_on_route

def extend_station_info(df):
    df.loc[:,'station_name']=df.station_uuid.map(get_stations().set_index('uuid')['brand'].to_dict())
    df.loc[:,'station_address']=df.station_uuid.map(get_stations().set_index('uuid')['street'].to_dict())
    df.loc[:,'station_latitude']=df.station_uuid.map(get_stations().set_index('uuid')['latitude'].to_dict())
    df.loc[:,'station_longitude']=df.station_uuid.map(get_stations().set_index('uuid')['longitude'].to_dict())
    return df

    
def presel_data(df):
    df_presel = df.loc[df.station_uuid.isin(get_stations().uuid)]
    df_addinfo = extend_station_info(df_presel)
    #df_presel.loc[:,'station_name']=df_presel.station_uuid
    return df_addinfo 
    
