import pandas as pd
import numpy as np
import os

def read_all_data(data_dir = 'data/processed/total_test', spec_id = 'e1a15081-2617-9107-e040-0b0a3dfe563c', gas_type = 'e5'):
    '''
    Read all available data
    '''
    min_price_data = pd.DataFrame()
    for filename in os.listdir(data_dir):
        if "csv" in filename:
            print(filename)
            dataset=pd.read_csv(os.path.join(data_dir, filename))
            dataset_spec = dataset.loc[dataset.station_uuid==spec_id]
            dataset_spec = dataset_spec.sort_values('date', ascending=True)
            dataset_spec = dataset_spec.loc[dataset_spec[gas_type]<=dataset_spec[gas_type].min()][:1]
            min_price_data = min_price_data.append(dataset_spec)

    min_price_data = min_price_data.sort_values('date', ascending=True)
    return min_price_data
        
class ModelDataPrep:
    def __init__(self, df, train):
        self.data = df
