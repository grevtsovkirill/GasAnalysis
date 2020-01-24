import pandas as pd
import numpy as np

#define geographical constraints
minlat=53.553444
maxlat=53.667341
minlon=9.851884
maxlon=9.995315

stations=pd.read_csv("data/stations.csv")

def get_stations(stations):    
    stations_on_route=stations.loc[
             (stations.latitude>minlat)&(stations.latitude<maxlat)&
            (stations.longitude>minlon)&(stations.longitude<maxlon)]
    return stations_on_route.uuid
