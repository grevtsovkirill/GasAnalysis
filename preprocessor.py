import sys,os,time,stat,logging
import pandas as pd
import numpy as np
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

from prep_data import *
from plot_helper import *

def main():
    #load data
    #years = ['2015','2016','2017','2018','2019','2020']
    #for j in years:
    #    for i in range(1,13):
    #        month=month_to_num_str(i)
    #        prepare_data(month,j)
    prepare_data("03","2020")
    
if __name__ == "__main__":
    start = time.time()
    main()
    log.info("Process time: %f" %(time.time() - start))

