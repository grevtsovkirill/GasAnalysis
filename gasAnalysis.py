import sys,os,time,stat,logging
import pathlib
import pandas as pd
import numpy as np
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

from prep_data import *

def main():
    #load data
    print("load data")
    name="2020/01/2020-01-01-prices.csv"
    my_file = pathlib.Path("data/processed/"+name)
    if not my_file.exists ():
        print("file does NOT exist: require processing")
    else:
        prices=pd.read_csv(my_file)
        print("Read {} entries for {}".format(len(prices),my_file))
    
if __name__ == "__main__":
    start = time.time()
    main()
    log.info("Process time: %f" %(time.time() - start))

