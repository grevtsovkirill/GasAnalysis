import pandas as pd
import numpy as np
import os
from selected import *

st = 'star_home'
spec_id = fav_stations[st]['id']

data_dir='data/processed/total'
filename='2020-03-10-prices.csv'
dataset=pd.read_csv(os.path.join(data_dir, filename))
print(len(dataset))
