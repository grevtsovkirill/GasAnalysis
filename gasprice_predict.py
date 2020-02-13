import numpy as np
from model_dataprep import *

rawdata = HistoricalData('data/processed/total_test')
df0 = rawdata.read_all_data()
df = rawdata.prep_min_price(df0)
print(df.head())
data = ModelDataPrep(df,1)
