# GasAnalysis
Extract information on gas prices close to my route. 

## Historical data
Check evolution of the prices, variance over time for stations along the route from work.
Build interactive dashbord with hisorical data ["Tableau dash"](https://public.tableau.com/profile/kirill.grevtsov#!/vizhome/GasPriceAnalysis_15826513372120/Dashboard1?publish=yes):

![alt text](https://github.com/grevtsovkirill/GasAnalysis/blob/master/Plots/tableau_dash.png)


## Predictive models

### Price
Train LSTM model to predict "next-day-price":

![alt text](https://github.com/grevtsovkirill/GasAnalysis/blob/master/Plots/LSTM_train_2017-01-01_2020-02-12load.png)

### Time
Predict the right time to refill. Estimate the time ranges during the day where relative increase of the price wrt to day's minimum was lowest (i.e. 0% means minimal price):

X: time of the day;
Y: increase of the price wrt to day's minimum in %

![alt text](https://github.com/grevtsovkirill/GasAnalysis/blob/master/Plots/relative_hourly_change.png)
