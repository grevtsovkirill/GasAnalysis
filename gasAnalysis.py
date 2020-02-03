import sys,os,time,stat,logging
import pathlib
import pandas as pd
import numpy as np
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

from prep_data import *

def loop_days(beg, end):
    days_list=[]
    for i in range(beg,end+1):
        if i<10:
            days_list.append("0"+str(i))
        elif i>9 and i<32:
            days_list.append(str(i))
        else:
            print("smth went wrong")
            return 0
    return days_list

def main():
    #load data
    print("load data")
    months=["01"]
    #days=["01"]
    days=loop_days(1,31)
    for mon in months:
        for day in days: 
            name="2020/"+mon+"/2020-"+mon+"-"+day+"-prices.csv"
            my_file = pathlib.Path("data/processed/"+name)
            if not my_file.exists ():
                print("file does NOT exist: require processing (save output to processed folder)")
                prices_raw=pd.read_csv("data/raw/GasPrices/"+name)
                prices = presel_data(prices_raw)
                prices.to_csv(my_file)
            else:
                prices=pd.read_csv(my_file)
                
                print("Read {} entries for {}".format(len(prices),my_file))
            
            
if __name__ == "__main__":
    start = time.time()
    main()
    log.info("Process time: %f" %(time.time() - start))

