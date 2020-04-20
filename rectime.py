import pandas as pd
import numpy as np
import os
import pathlib
from selected import *
from plot_helper import * 

import argparse
from prep_data import *


parser = argparse.ArgumentParser(description='Hisorical data:')
parser.add_argument('-t','--type', required=True, type=str, choices=['hourly', 'daily'], help='Choose type: per hour during day or per day in week')
parser.add_argument('--d0', required=True, type=valid_date, help='Date in format DD-MM-YYYY')
parser.add_argument('-s','--station', required=True, type=str, choices=['star_home','aral_home','hem_home'], help='Choose station ')
parser.add_argument('--debug', required=False, default=False, type=bool, help='For local checks ')
parser.add_argument('--delta', type=int, default=41, help="Number of days to step back for weekly estimations") 
parser.add_argument('--inpath', type=str, default='data/processed/total', help="Path of input data") 
args = parser.parse_args()

process_type = vars(args)["type"]
debug = vars(args)["debug"]
st = vars(args)["station"]
delta = vars(args)["delta"]
selected_date = vars(args)["d0"].date()
data_path = vars(args)["inpath"]


spec_id = fav_stations[st]['id']
def prepare_hour_day_output():
    time_split_array = pd.date_range("06:00", "23:59", freq="30min").time
    for i in range(len(time_split_array)):
        time_split_array[i]=time_split_array[i].strftime("%H:%M")
    
    dayinfocols=np.append('min_val',time_split_array)
    dayinfocols=np.append('date',dayinfocols)
    day_hourly_change = pd.DataFrame(columns=dayinfocols)
    return day_hourly_change

def create_hourly_array(df,gas_type='e5'):
    tt_array = prepare_hour_day_output()
    tt_array.drop(['date', 'min_val'], axis=1,inplace = True)
    t_array=tt_array.columns.values
    price_hour_array = [None]*len(t_array)
    t_i, p_i = df['date'],df[gas_type]
    for j in range(len(t_array)):
        found = False
        for i in range(len(df)):           
            if j < len(t_array)-1:
                if t_i[i].time().strftime("%H:%M") > t_array[j] and t_i[i].time().strftime("%H:%M") < t_array[j+1]:
                    price_hour_array[j]=p_i[i]
                    found=True
            else:
                if t_i[i].time().strftime("%H:%M") > t_array[j]:
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


def plot_maker(df):
    #day_hourly_change.to_csv("data/Tableau/per_hour/test_03_1014.csv")
    df = df.drop('min_val',axis=1)
    plot = df.T.plot(kind='bar',legend=False)
    plot.set_title("Relative increase of price wrt minimal value")
    plot.set_xlabel("Time of the day")
    plot.set_ylabel("Price increase, %")
    fig = plot.get_figure()
    fig.tight_layout()
    fig.savefig("Plots/relative_hourly_change.png")

def get_list_of_files(t_delta):
    delta = datetime.timedelta(t_delta)
    filenames = []
    for i in range(delta.days + 1):
        day_to_proc = selected_date - datetime.timedelta(days=i)
        fname=str(day_to_proc)+'-prices.csv'
        filenames.insert(0,fname)
    return filenames

if process_type == 'hourly':
    day_hourly_change = prepare_hour_day_output()
    dayinfocols = day_hourly_change.columns.values
    filenames = get_list_of_files(delta)
    for filename in filenames:
        if pathlib.Path(data_path+"/"+filename).is_file():
            day_info = get_relative_hourly_price(data_path,filename)
            day_hourly_change = day_hourly_change.append(pd.Series(day_info,index=dayinfocols),ignore_index=True )
        else:
            print("file does NOT exist")
        
    day_hourly_change = day_hourly_change.set_index('date')
    plot_maker(day_hourly_change)
    print(day_hourly_change)
elif process_type == 'daily':
    filenames = get_list_of_files(delta) 
    #print(selected_date,'\n',filenames)
    for filename in filenames:
        if pathlib.Path(data_path+"/"+filename).is_file():
            print(filename)
        else:
            print("file does NOT exist")
        
