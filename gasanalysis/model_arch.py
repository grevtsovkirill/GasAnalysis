import numpy as np
import pandas as pd

from gasanalysis import plot_helper
from keras.models import Sequential,load_model
from keras.layers import Dense, LSTM
from keras.optimizers import RMSprop
from keras.callbacks import EarlyStopping, ModelCheckpoint

def create_model(window_size):
    model = Sequential()
    model.add(LSTM(4, input_shape=(1, window_size)))
    model.add(Dense(units = 24,
                    activation='relu', 
                    name='Hidden1'))
    model.add(Dense(units = 12,
                    activation='relu', 
                    name='Hidden2'))
    model.add(Dense(units=1,  
                    name='Output'))
    model.compile(loss='mean_squared_error',
                  #metrics = ['mse'],
                  optimizer='adam'
                  #optimizer=RMSprop(lr=0.01)
    )
    return model

def train_model(model, X,Y,range_name,
                epochs=500, batch_size=10, validation_split=0.2):
    
    earlyStop = EarlyStopping(monitor='val_loss', verbose=True, patience=20)
    nn_mChkPt = ModelCheckpoint('Models/nn_weights.h5',monitor='val_loss', verbose=True,
                                save_best_only=True,
                                save_weights_only=True)
    history = model.fit(x=X, y=Y,
                        batch_size=batch_size,
                        epochs=epochs, shuffle=True, 
                        validation_split=validation_split,
                        callbacks=[earlyStop, nn_mChkPt]
    )
    epochs = history.epoch
    hist = pd.DataFrame(history.history)
    rmse = hist["loss"]
    vrmse = hist["val_loss"]
    
    plot_helper.plot_the_loss_curve(epochs,rmse,vrmse)
    model.save('Models/LSTM_'+range_name+'.h5')
    return model, epochs, hist

def pred_model(X,Y,window_size,range_name):
    model = create_model(window_size)
    model, epochs, hist = train_model(model, X, Y,range_name)
        
    return model
    
