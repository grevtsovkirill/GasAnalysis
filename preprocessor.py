import sys,os,time,stat,logging
import pandas as pd
import numpy as np
import argparse
import datetime

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

from gasanalysis import prep_data

parser = argparse.ArgumentParser(description='Preprocess raw data')
parser.add_argument('-t','--type', required=True, type=str, choices=['date', 'range'], help='Choose processing type: date or range ')
parser.add_argument('--d0', required=True, type=prep_data.valid_date, help='Date in format DD-MM-YYYY')
parser.add_argument('--d1', required=False, type=prep_data.valid_date, help='End date in format DD-MM-YYYY')
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
    if process_type=='date':
        prep_data.prepare_data(initial_date)
    else:
        delta = final_date - initial_date        
        for i in range(delta.days + 1):
            day_to_proc = initial_date + datetime.timedelta(days=i)
            print(day_to_proc)
            prep_data.prepare_data(day_to_proc)
    
if __name__ == "__main__":
    start = time.time()
    main()
    log.info("Process time: %f" %(time.time() - start))

