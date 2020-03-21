import pandas as pd
import numpy as np
import os
from selected import *
from plot_helper import * 

st = 'star_home'
spec_id = fav_stations[st]['id']
time_split_array = pd.date_range("06:00", "23:59", freq="30min").time
day_hourly_change = pd.DataFrame(columns=time_split_array)
def match_time_to_index(time_v, t_array=time_split_array):
    for j in range(len(t_array)):
        if time_v > t_array[j]: 
            if time_v < t_array[j+1]:
                return j
            
def create_hourly_array(df,t_array=time_split_array,gas_type='e5'):
    price_hour_array = [None]*len(t_array)
    t_i, p_i = df['date'],df[gas_type]
    for j in range(len(t_array)):
        found = False
        for i in range(len(df)):           
            if j < len(t_array)-1:
                if t_i[i].time() > t_array[j] and t_i[i].time() < t_array[j+1]:
                    price_hour_array[j]=p_i[i]
                    found=True
            else:
                if t_i[i].time() > t_array[j]:
                    price_hour_array[j]=p_i[i]
                    found=True                    
        if not found:
            if j==0:
                price_hour_array[0]=100
            else:
                price_hour_array[j]= price_hour_array[j-1]
    return price_hour_array


data_dir = 'data/processed/total'
filename = '2020-03-11-prices.csv'
dataset = pd.read_csv(os.path.join(data_dir, filename))
dataset_spec = dataset.loc[dataset.station_uuid==spec_id]   
dataset_spec = dataset_spec.loc[dataset.e5change==1]
dataset_spec['date'] = pd.to_datetime(dataset_spec['date'])
dataset_spec = dataset_spec.sort_values('date', ascending=True)
min_val=dataset_spec[gas_type].min()
dataset_spec[gas_type] = dataset_spec[gas_type].apply(lambda x: (x-min_val)/min_val*100 )
dataset_spec.reset_index(inplace=True)
print(len(dataset_spec),dataset_spec[gas_type].min())

#create complete day-hourly map of change - i.e. fill with previous measurement if current time doesn't exist:
day_array = create_hourly_array(dataset_spec)
print(day_array)
#check measurements correspondance to time_split_array
#for i in range(len(dataset_spec)):
#    t_i, p_i = dataset_spec['date'][i],dataset_spec[gas_type][i]
#    print(i,'\t',t_i.time()," (bin=",match_time_to_index(t_i.time()),")",'\t',p_i)
day_hourly_change = day_hourly_change.append(pd.Series(day_array,index=time_split_array),ignore_index=True )
print(day_hourly_change)
