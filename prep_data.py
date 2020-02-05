import os
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

def month_to_num_str(mon_num=1):
    mon_str=''
    if mon_num<10:
        mon_str='0'+str(mon_num)
    elif mon_num>9 and mon_num<13:
        mon_str=str(mon_num)
    else:
        print("smth went wrong")
        return 0
    return mon_str
        


def prepare_data():
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
    
def give_me_data(mon=1,year=2020,spec_id = "e1a15081-2617-9107-e040-0b0a3dfe563c"):
    data_dir = 'data/processed/'+str(year)+'/'+month_to_num_str(mon)
    merged_data = pd.DataFrame()
    

    for filename in os.listdir(data_dir):
        if "csv" in filename:
            #print(filename)
            dataset=pd.read_csv(os.path.join(data_dir, filename))
            #print("all ",len(dataset))
            dataset_spec=dataset.loc[dataset.station_uuid==spec_id]
            #print("sel ",len(dataset_spec))
            merged_data = merged_data.append(dataset_spec)

    merged_data.loc[:,'date']=pd.to_datetime(merged_data['date'])
    merged_data.sort_values('date', ascending=True, inplace=True)
    return merged_data

