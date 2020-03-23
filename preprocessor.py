import sys,os,time,stat,logging
import pandas as pd
import numpy as np
import argparse

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

from prep_data import *
from plot_helper import *

parser = argparse.ArgumentParser(description='Upload data from sensor')
parser.add_argument('-t','--type', required=True, type=str, choices=['date', 'range'], help='Choose processing type: date or range ')
parser.add_argument('--d0', required=True, type=str, help='Date in format DD-MM-YYYY')
parser.add_argument('--d1', required=False, type=str, help='Date in format DD-MM-YYYY')
args = parser.parse_args()

process_type = vars(args)["type"]
initial_date = vars(args)["d0"]
final_date = vars(args)["d1"]

if (process_type=='range' and  not final_date ):
    parser.error('The type range requires the --d1 argument')
    


def main():
    #load data
    #years = ['2015','2016','2017','2018','2019','2020']
    #for j in years:
    #    for i in range(1,13):
    #        month=month_to_num_str(i)
    #        prepare_data(month,j)
    #print(process_type,initial_date)
    if process_type=='date':
        dd, mm, yy = initial_date.split("-")
        #print(type(dd))
        prepare_data(dd, mm, yy)
    #prepare_data("02","2020")
    
if __name__ == "__main__":
    start = time.time()
    main()
    log.info("Process time: %f" %(time.time() - start))

