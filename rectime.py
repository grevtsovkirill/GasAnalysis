import pandas as pd
import numpy as np
import os
from selected import *
from plot_helper import * 

st = 'star_home'
spec_id = fav_stations[st]['id']
time_split_array = pd.date_range("06:00", "23:59", freq="30min").time
dayinfocols=np.append('min_val',time_split_array)
dayinfocols=np.append('date',dayinfocols)
day_hourly_change = pd.DataFrame(columns=dayinfocols)
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


def get_relative_hourly_price(data_dir,filename):
    dataset = pd.read_csv(os.path.join(data_dir, filename))
    dataset_spec = dataset.loc[dataset.station_uuid==spec_id]   
    dataset_spec = dataset_spec.loc[dataset.e5change==1]
    dataset_spec['date'] = pd.to_datetime(dataset_spec['date'])
    dataset_spec = dataset_spec.sort_values('date', ascending=True)
    min_val=dataset_spec[gas_type].min()
    dataset_spec[gas_type] = dataset_spec[gas_type].apply(lambda x: (x-min_val)/min_val*100 )
    dataset_spec.reset_index(inplace=True)
    #create complete day-hourly map of change - i.e. fill with previous measurement if current time doesn't exist:
    day_array = create_hourly_array(dataset_spec)
    t_i= dataset_spec['date'][0].date()
    day_info = []
    day_info=np.append(min_val,day_array)
    day_info=np.append(t_i,day_info)
    return day_info

data_dir = 'data/processed/total'
filename = '2020-03-11-prices.csv'
filenames = ['2020-03-01-prices.csv']
#filenames = ['2020-03-01-prices.csv','2020-03-02-prices.csv','2020-03-03-prices.csv','2020-03-04-prices.csv','2020-03-05-prices.csv','2020-03-06-prices.csv','2020-03-07-prices.csv','2020-03-08-prices.csv','2020-03-09-prices.csv','2020-03-10-prices.csv','2020-03-11-prices.csv','2020-03-12-prices.csv','2020-03-13-prices.csv','2020-03-14-prices.csv']
#,'2020-03-15-prices.csv','2020-03-16-prices.csv','2020-03-17-prices.csv','2020-03-18-prices.csv','2020-03-19-prices.csv'
for filename in filenames:
    day_info = get_relative_hourly_price(data_dir,filename)
    day_hourly_change = day_hourly_change.append(pd.Series(day_info,index=dayinfocols),ignore_index=True )

day_hourly_change = day_hourly_change.set_index('date')
print(day_hourly_change)
day_hourly_change.to_csv("data/Tableau/per_hour/test_03_1014.csv")
#plot = day_hourly_change.T.plot(kind='bar',legend=False)
#fig = plot.get_figure()
#fig.savefig("Plots/relative_hourly_change.png")
