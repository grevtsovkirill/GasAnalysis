import numpy as np
from model_dataprep import *
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

rawdata = HistoricalData('data/processed/total_test')
df0 = rawdata.read_all_data()
df = rawdata.prep_min_price(df0)
training_fraction = 0.67
window_size = 10
data = ModelDataPrep(df,training_fraction,window_size)
data.gen_train()
data.gen_test()  
trainX = np.reshape(data.X_train, (data.X_train.shape[0], 1, data.X_train.shape[1]))
testX = np.reshape(data.X_test, (data.X_test.shape[0], 1, data.X_test.shape[1]))

model = Sequential()
model.add(LSTM(4, input_shape=(1, window_size)))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(trainX, data.Y_train, epochs=100, batch_size=1, verbose=2)

#print(data.X_test)
#print(data.Y_test)
#print(trainX)

