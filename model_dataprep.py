import pandas as pd
import numpy as np
import os

class HistoricalData:
    spec_id = 'e1a15081-2617-9107-e040-0b0a3dfe563c'
    gas_type = 'e5'
    def __init__(self, data_dir):
        self.data_dir=data_dir
        
    def read_all_data(self):
        '''
        Read all available data
        '''
        min_price_data = pd.DataFrame()
        for filename in os.listdir(self.data_dir):
            if "csv" in filename:
                print(filename)
                dataset=pd.read_csv(os.path.join(self.data_dir, filename))
                dataset_spec = dataset.loc[dataset.station_uuid==self.spec_id]
                dataset_spec = dataset_spec.sort_values('date', ascending=True)
                dataset_spec = dataset_spec.loc[dataset_spec[self.gas_type]<=dataset_spec[self.gas_type].min()][:1]
                min_price_data = min_price_data.append(dataset_spec)
                
        min_price_data = min_price_data.sort_values('date', ascending=True)
        return min_price_data
    
    def prep_min_price(self,df):
        df = df[['date', self.gas_type]].copy()
        df.loc[:,'date']=pd.to_datetime(df['date'],utc=True).dt.date
        df = df.reset_index(drop=True)
        print("Available data from: ",df.date.iloc[0]," to ",df.date.iloc[-1])
        return df
        
class ModelDataPrep:
    def __init__(self, df, train):
        self.data = df
