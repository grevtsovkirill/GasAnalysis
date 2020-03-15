import pandas as pd
import numpy as np
import os
from selected import *

st = 'star_home'
spec_id = fav_stations[st]['id']

data_dir = 'data/processed/total'
filename = '2020-03-10-prices.csv'
dataset = pd.read_csv(os.path.join(data_dir, filename))
dataset_spec = dataset.loc[dataset.station_uuid==spec_id]   
dataset_spec = dataset_spec.sort_values('date', ascending=True)
dataset_spec = dataset_spec.loc[dataset_spec[gas_type]<=dataset_spec[gas_type].min()][:1]
print(dataset_spec)
