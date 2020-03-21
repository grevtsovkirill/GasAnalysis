import pandas as pd
import numpy as np
import os
from selected import *
from plot_helper import * 

st = 'star_home'
spec_id = fav_stations[st]['id']

data_dir = 'data/processed/total'
filename = '2020-03-11-prices.csv'
dataset = pd.read_csv(os.path.join(data_dir, filename))
dataset_spec = dataset.loc[dataset.station_uuid==spec_id]   
dataset_spec = dataset_spec.loc[dataset.e5change==1]
dataset_spec['date'] = pd.to_datetime(dataset_spec['date'])
dataset_spec = dataset_spec.sort_values('date', ascending=True)
#dataset_spec = dataset_spec.loc[dataset_spec[gas_type]<=dataset_spec[gas_type].min()][:1]
min_val=dataset_spec[gas_type].min()
dataset_spec[gas_type] = dataset_spec[gas_type].apply(lambda x: (x-min_val)/min_val*100 )
dataset_spec.reset_index(inplace=True)
print(len(dataset_spec),dataset_spec[gas_type].min())
for i in range(len(dataset_spec)):
    t_i, p_i = dataset_spec['date'][i],dataset_spec[gas_type][i]
    print(i,'\t',t_i.time(),'\t',p_i)
#print(dataset_spec[['date',gas_type]])
#plot_over_day(dataset_spec,True,'test','day 1 ') 
#plot_over_time(dataset_spec,True,'test','day 1 ') 
