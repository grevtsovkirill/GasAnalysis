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
    prices=give_me_data()
    
if __name__ == "__main__":
    start = time.time()
    main()
    log.info("Process time: %f" %(time.time() - start))

