import numpy as np
from model_dataprep import *
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import matplotlib.pyplot as plt


histdata = HistoricalData('data/processed/total_test')
histdata.get_data_for_prediction()
df = histdata.data_for_prediction
print("Available data from: ",histdata.startdate," to ",histdata.stopdate)

training_fraction = 0.67
window_size = 10
data = ModelDataPrep(df,training_fraction,window_size)
data.gen_train()
data.gen_test()  
trainX = np.reshape(data.X_train, (data.X_train.shape[0], 1, data.X_train.shape[1]))
testX = np.reshape(data.X_test, (data.X_test.shape[0], 1, data.X_test.shape[1]))

do_train = True
if do_train:
    model = Sequential()
    model.add(LSTM(4, input_shape=(1, window_size)))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(trainX, data.Y_train, epochs=100, batch_size=1, verbose=2)
    
    # make predictions
    trainPredict = model.predict(trainX)
    testPredict = model.predict(testX)
    
    plt.plot(data.Y_train,label='Train Data')
    plt.plot(trainPredict,label='Train Prediction')
    plt.legend()
    plot_name = str(histdata.startdate)+"_"+str(histdata.stopdate)
    plt.savefig("Plots/LSTM_train_"+plot_name+".png", transparent=True)
