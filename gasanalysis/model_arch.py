import numpy as np
import pandas as pd

from gasanalysis import plot_helper
from keras.models import Sequential,load_model
from keras.layers import Dense, LSTM
from keras.optimizers import RMSprop

def pred_model(X,Y,window_size,range_name):
        model = Sequential()
        model.add(LSTM(4, input_shape=(1, window_size)))
        model.add(Dense(units = 32,
                        activation='relu', 
                        name='Hidden1'))
        # model.add(Dense(units = 12,
        #                 activation='relu', 
        #                 name='Hidden2'))
        # Define the output layer.
        model.add(Dense(units=1,  
                        name='Output'))
        model.compile(loss='mean_squared_error',
                      #metrics = ['mse'],
                      optimizer='adam'
                      #optimizer=RMSprop(lr=0.01)
        )

        history = model.fit(X,Y,
                            epochs=300, batch_size=1000, verbose=2,
                            validation_split=0.2
        )

        epochs = history.epoch
        hist = pd.DataFrame(history.history)
        print(history.history.keys())
        rmse = hist["loss"]
        vrmse = hist["val_loss"]

        plot_helper.plot_the_loss_curve(epochs,rmse,vrmse)
        model.save('Models/LSTM_'+range_name+'.h5')
        

        return model
