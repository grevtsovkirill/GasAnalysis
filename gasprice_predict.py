import numpy as np
from model_dataprep import *

rawdata = HistoricalData('data/processed/total_test')
df0 = rawdata.read_all_data()
df = rawdata.prep_min_price(df0)
training_fraction = 0.67
window_size = 10
data = ModelDataPrep(df,training_fraction,window_size)
data.gen_train()
data.gen_test()  
