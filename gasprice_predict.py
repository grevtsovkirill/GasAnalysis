import numpy as np
import matplotlib.pyplot as plt

from model_dataprep import *
from plot_helper import *

histdata = HistoricalData('data/processed/total_test')
histdata.get_data_for_prediction()
df = histdata.data_for_prediction
print("Available data from: ",histdata.startdate," to ",histdata.stopdate)
range_name = str(histdata.startdate)+"_"+str(histdata.stopdate)

plot_over_time(df,True,'e5_variation_'+range_name,'Price evolution of ')

training_fraction = 0.67
window_size = 10
data = ModelDataPrep(df,training_fraction,window_size)
data.gen_train()
data.gen_test()  
trainX = np.reshape(data.X_train, (data.X_train.shape[0], 1, data.X_train.shape[1]))
testX = np.reshape(data.X_test, (data.X_test.shape[0], 1, data.X_test.shape[1]))

debug = True
do_train = False
do_load = False
model_suf = ''

if not debug:
    from keras.models import Sequential
    from keras.layers import Dense
    from keras.layers import LSTM
    from keras.models import load_model
    
    if do_train and not do_load:
        model = Sequential()
        model.add(LSTM(4, input_shape=(1, window_size)))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(trainX, data.Y_train, epochs=100, batch_size=1, verbose=2)
        model.save('Models/LSTM_'+range_name+'.h5')
        model_suf = 'train'
    if do_load:
        model = load_model('Models/LSTM_'+range_name+'.h5')
        model_suf = 'load'

    # make predictions using trained/loaded model:
    trainPredict = model.predict(trainX)
    testPredict = model.predict(testX)
    
    plt.plot(data.Y_train,label='Train Data')
    plt.plot(trainPredict,label='Train Prediction')
    plt.legend()
    plt.savefig("Plots/LSTM_train_"+range_name+model_suf+".png", transparent=True)

