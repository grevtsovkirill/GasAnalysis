import numpy as np
import pandas as pd

from gasanalysis import prep_data
from gasanalysis import selected
from gasanalysis import plot_helper
from gasanalysis import model_dataprep
import argparse

parser = argparse.ArgumentParser(description='Hisorical data:')
parser.add_argument('-t','--type', required=True, type=str, choices=['model_train','model_apply', 'tableau'], help='Choose type: do model training or application; get tableau data ')
parser.add_argument('-s','--station', required=True, type=str, choices=['star_home','aral_home','hem_home'], help='Choose station ')
parser.add_argument('--debug', required=False, default=False, type=bool, help='For local checks ')
parser.add_argument('--tf', required=False, type=float, default=0.69, help="Fraction of used data for training")
parser.add_argument('--win_size', required=False, type=int, default=10, help="Size of training window") 
parser.add_argument('--inpath', type=str, default='data/processed/total_test', help="Path of input data") 
args = parser.parse_args()

process_type = vars(args)["type"]
debug = vars(args)["debug"]
st = vars(args)["station"]
training_fraction = vars(args)["tf"]
window_size = vars(args)["win_size"]
data_path = vars(args)["inpath"]


###
def hist_data_tableau(df,range_name):
    plot_helper.plot_over_time(df,True,'e5_variation_'+range_name,'Price evolution of ')
    file_name = 'data/Tableau/'+range_name+'.csv'
    df.to_csv(file_name, sep=',')


def get_predictions(df,range_name):
    data = model_dataprep.ModelDataPrep(df,training_fraction,window_size)
    data.gen_train()
    data.gen_test()  
    trainX = np.reshape(data.X_train, (data.X_train.shape[0], 1, data.X_train.shape[1]))
    testX = np.reshape(data.X_test, (data.X_test.shape[0], 1, data.X_test.shape[1]))

    from keras.models import Sequential,load_model
    from keras.layers import Dense, LSTM
    from keras.optimizers import RMSprop

    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    
    if process_type=='model_train':
        model = Sequential()
        model.add(LSTM(4, input_shape=(1, window_size)))
        model.add(Dense(units = 1,
                        activation='relu', 
                        name='Hidden1'))
        # Define the output layer.
        model.add(Dense(units=1,  
                        name='Output'))
        model.compile(loss='mean_squared_error',
                      metrics = ['mean_squared_error'],
                      #optimizer='adam'
                      optimizer=RMSprop(lr=0.01)
        )

        history = model.fit(trainX, data.Y_train,
                            epochs=100, batch_size=1000, verbose=2,
                            validation_split=0.2
        )

        epochs = history.epoch
        hist = pd.DataFrame(history.history)
        print(history.history.keys())
        rmse = hist["loss"]
        vrmse = hist["val_loss"]

        plot_helper.plot_the_loss_curve(epochs,rmse,vrmse)
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


    
def main():
    spec_id = selected.fav_stations[st]['id']
    print(selected.fav_stations[st]['name'])
    histdata = model_dataprep.HistoricalData(data_path,spec_id)
    histdata.get_data_for_prediction()
    df = histdata.data_for_prediction
    print("Available data from: ",histdata.startdate," to ",histdata.stopdate)
    range_name = st+"_"+str(histdata.startdate)+"_"+str(histdata.stopdate)
    model_suf = ''

    if process_type=='tableau':
        hist_data_tableau(df,range_name)

    if 'model' in process_type:
        get_predictions(df,range_name)

if __name__ == "__main__":
    main()

