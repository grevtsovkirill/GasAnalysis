import numpy as np

from model_dataprep import *
from plot_helper import *
from selected import *
import argparse

parser = argparse.ArgumentParser(description='Upload data from sensor')
parser.add_argument('-t','--type', required=True, type=str, choices=['model_train','model_apply', 'tableau'], help='Choose type: do model training or application; get tableau data ')
parser.add_argument('-s','--station', required=True, type=str, choices=['star_home','aral_home','hem_home'], help='Choose station ')
parser.add_argument('--debug', required=False, default=False, type=bool, help='For local checks ')
parser.add_argument('--tf', required=False, type=float, default=0.69, help="Fraction of used data for training")
parser.add_argument('--win_size', required=False, type=int, default=10, help="Size of training window") 
args = parser.parse_args()

process_type = vars(args)["type"]
debug = vars(args)["debug"]
st = vars(args)["station"]
training_fraction = vars(args)["tf"]
window_size = vars(args)["win_size"]



###
spec_id = fav_stations[st]['id']
print(fav_stations[st]['name'])
histdata = HistoricalData('data/processed/total',spec_id)
histdata.get_data_for_prediction()
df = histdata.data_for_prediction
print("Available data from: ",histdata.startdate," to ",histdata.stopdate)
range_name = st+"_"+str(histdata.startdate)+"_"+str(histdata.stopdate)

if process_type=='tableau':
    plot_over_time(df,True,'e5_variation_'+range_name,'Price evolution of ')
    file_name = 'data/Tableau/'+range_name+'.csv'
    df.to_csv(file_name, sep=',')

data = ModelDataPrep(df,training_fraction,window_size)
data.gen_train()
data.gen_test()  
trainX = np.reshape(data.X_train, (data.X_train.shape[0], 1, data.X_train.shape[1]))
testX = np.reshape(data.X_test, (data.X_test.shape[0], 1, data.X_test.shape[1]))


model_suf = ''

if 'model' in process_type:
    from keras.models import Sequential
    from keras.layers import Dense
    from keras.layers import LSTM
    from keras.models import load_model

    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    
    if process_type=='model_train':
        model = Sequential()
        model.add(LSTM(4, input_shape=(1, window_size)))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(trainX, data.Y_train, epochs=100, batch_size=1, verbose=2)
        model.save('Models/LSTM_'+range_name+'.h5')
        model_suf = 'train'
    elif process_type=='model_apply':
        model = load_model('Models/LSTM_'+range_name+'.h5')
        model_suf = 'load'

    # make predictions using trained/loaded model:
    trainPredict = model.predict(trainX)
    testPredict = model.predict(testX)
    
    fig, (ax1, ax2) = plt.subplots(1,2)
    ax1.plot(data.Y_train,label='Train Data')
    ax1.plot(trainPredict,label='Train Prediction')
    ax1.legend()

    ax2.plot(data.Y_test,label='Test Data')
    ax2.plot(testPredict,label='Test Prediction')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig("Plots/LSTM_train_"+range_name+model_suf+".png", transparent=True)
    #plt.savefig("Plots/LSTM_test_"+range_name+model_suf+".png", transparent=True)

