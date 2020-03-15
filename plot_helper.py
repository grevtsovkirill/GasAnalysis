import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()
        
def plot_over_time(data,to_save=False,name='',lab_str='',gas_type='e5'):
    df1 = data.sort_values('date', ascending=True)
    lab_str = lab_str+' '+gas_type
    fig, ax = plt.subplots()
    ax.plot(pd.to_datetime(df1['date']), df1[gas_type],label=lab_str)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%D'))
    ax.grid(True)
    ax.set_title(lab_str)
    fig.autofmt_xdate()
    if to_save:
        plt.savefig("Plots/"+name+".png", transparent=True)

def plot_over_day(data,to_save=False,name='',lab_str='',gas_type='e5'):
    df1 = data.sort_values('date', ascending=True)
    nbins=len(df1)
    lab_str = lab_str+' '+gas_type
    fig, ax = plt.subplots()
    #ax.plot(pd.to_datetime(df1['date']), df1[gas_type],label=lab_str)
    ax.bar(pd.to_datetime(df1['date']), df1[gas_type],label=lab_str)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H'))
    
    #ax.xticks(index, pd.to_datetime(df1['date'])) 
    ax.grid(True)
    #ax.set_title(lab_str)
    #fig.autofmt_xdate()
    if to_save:
        plt.savefig("Plots/"+name+".png", transparent=True)
        
