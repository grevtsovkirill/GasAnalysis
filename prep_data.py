import pandas as pd
import numpy as np
import pathlib

#define geographical constraints
minlat=53.567181
maxlat=53.648408
minlon=9.876232
maxlon=9.941601

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

def loop_days(beg, end):
    days_list=[]
    for i in range(beg,end+1):
        if i<10:
            days_list.append("0"+str(i))
        elif i>9 and i<32:
            days_list.append(str(i))
        else:
            print("smth went wrong")
            return 0
    return days_list


def give_me_data():
    months=["01"]
    #days=["01"] day=1,month=1,year=2020
    days=loop_days(1,31)
    for mon in months:
        for day in days: 
            name="2020/"+mon+"/2020-"+mon+"-"+day+"-prices.csv"
            my_file = pathlib.Path("data/processed/"+name)
            if not my_file.exists ():
                print("file does NOT exist: require processing (save output to processed folder)")
                prices_raw=pd.read_csv("data/raw/GasPrices/"+name)
                prices = presel_data(prices_raw)
                prices.to_csv(my_file)
            else:
                prices=pd.read_csv(my_file)
                
                print("Read {} entries for {}".format(len(prices),my_file))
    return prices

