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
#dataset_spec = dataset_spec.loc[dataset.e5change==1]   
dataset_spec = dataset_spec.sort_values('date', ascending=True)
#dataset_spec = dataset_spec.loc[dataset_spec[gas_type]<=dataset_spec[gas_type].min()][:1]
min_val=dataset_spec[gas_type].min()
dataset_spec[gas_type] = dataset_spec[gas_type].apply(lambda x: (x-min_val)/min_val*100 )

print(len(dataset_spec),dataset_spec[gas_type].min())
print(dataset_spec)
plot_over_day(dataset_spec,True,'test','day 1 ') 
#plot_over_time(dataset_spec,True,'test','day 1 ') 
