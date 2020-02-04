import sys,os,time,stat,logging
import pandas as pd
import numpy as np
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

from prep_data import *
from plot_helper import *

def main():
    #load data
    #print("prepare data in the city")    
    #prepare_data()
    #select data for given station
    prices=give_me_data()
    plot_over_time(prices)
    
if __name__ == "__main__":
    start = time.time()
    main()
    log.info("Process time: %f" %(time.time() - start))

