import sys,os,time,stat,logging
import pandas as pd
import numpy as np
import argparse
import datetime

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

from prep_data import *
from plot_helper import *

def valid_date(s):
    try:
        return datetime.datetime.strptime(s, "%d-%m-%Y")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

parser = argparse.ArgumentParser(description='Upload data from sensor')
parser.add_argument('-t','--type', required=True, type=str, choices=['date', 'range'], help='Choose processing type: date or range ')
#parser.add_argument('--d0', required=True, type=str, help='Date in format DD-MM-YYYY')
parser.add_argument('--d0', required=True, type=valid_date, help='Date in format DD-MM-YYYY')
parser.add_argument('--d1', required=False, type=valid_date, help='End date in format DD-MM-YYYY')
#parser.add_argument('--d1', required=False, type=str, help='Date in format DD-MM-YYYY')
args = parser.parse_args()

    
process_type = vars(args)["type"]
initial_date = vars(args)["d0"].date()
final_date = vars(args)["d1"]
if final_date:
    final_date=final_date.date()
    
if (process_type=='range'):
    if( not final_date ):
        parser.error('The type range requires the --d1 argument')
    elif( final_date< initial_date):
        parser.error('End date of the range earlier then start. Check dates')


def main():
    #load data
    #years = ['2015','2016','2017','2018','2019','2020']
    #for j in years:
    #    for i in range(1,13):
    #        month=month_to_num_str(i)
    #        prepare_data(month,j)
    #print(process_type,initial_date)
    if process_type=='date':
        prepare_data(initial_date)
    else:
        print(initial_date,final_date)
    #prepare_data("02","2020")
    
if __name__ == "__main__":
    start = time.time()
    main()
    log.info("Process time: %f" %(time.time() - start))

