import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_over_time(data,gas_type='e5'):
    df1 = data.sort_values('date', ascending=True)
    lab_str = gas_type+"_"+df1['station_name'].values[0]+"_"+df1['station_address'].values[0]
    lab_str = lab_str.replace(" ", "")
    print(lab_str)
    fig, ax = plt.subplots()
    ax.plot(pd.to_datetime(df1['date']), df1[gas_type],label=lab_str)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%D'))
    ax.grid(True)
    ax.set_title(lab_str)
    fig.autofmt_xdate()
    plt.savefig("Plots/overal_"+lab_str+".png", transparent=True)
