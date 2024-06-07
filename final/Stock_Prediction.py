import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report


symbol = str(input("Enter stock symbol"))
period1 = int(time.mktime(datetime.datetime(1971, 2, 5, 23, 59).timetuple())) # Just let this be the starting point for the dataset
period2 = int(time.mktime(datetime.datetime.today().timetuple()))
interval = '1d'

# Scraping the stock data 
data = f'https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'


def cleaning_data(symbol, dataset): # Preprocessing the dataset
    df = pd.read_csv(dataset)
    df.to_csv(f'{symbol}.csv')
    df = pd.read_csv(f"{symbol}.csv")
    df = df.drop(["Unnamed: 0", "Adj Close"], axis = 1)
    df["Target"] = ((df["Close"] - df["Open"]) > 0).astype(int)
    df.set_index('Date', inplace = True)
    df = df.dropna()
    horizons = [2, 5, 60, 250, 1000]
    predictors = []

    for horizon in horizons:
        rolling_averages = df.rolling(horizon).mean()

        ratio = f"Close_Ratio_{horizon}"
        df[ratio] = df["Close"].shift(1) / rolling_averages["Close"]

        trend = f"Trend_Ratio"
        df[trend] = df["Target"].shift(1).rolling(horizon).sum()

        predictors += [ratio, trend]
        
    df = df.dropna()
    
    return df, predictors

def predict(train, test, predictors, model): # Predicting the data
  model.fit(train[predictors], train["Target"])
  preds = model.predict_proba(test[predictors])[:,1] 
  preds[preds >= .6] = 1
  preds[preds < .6] = 0
  preds = pd.Series(preds, index = test.index, name = "Predictions")
  combined = pd.concat([test["Target"], preds], axis = 1)
  return combined


def backtesting(data, model, predictors, start = 1250, step = 250): # Testing the machine learning model
  all_preds = [] 

  for i in range(start, data.shape[0], step):
    train = data.iloc[0:i].copy()
    test = data.iloc[i:(i+step)].copy()
    all = predict(train, test, predictors, model)
    all_preds.append(all)

  return pd.concat(all_preds)

df, predictors = cleaning_data(symbol, data)

RFC_model = RandomForestClassifier(n_estimators = 200, min_samples_split = 50, random_state = 1) # Machine learning model

predictions = backtesting(df, RFC_model, predictors)

print(predictions["Predictions"].value_counts())

print(predictions)

print(classification_report(predictions["Target"], predictions["Predictions"]))

tomorrow_data = df.iloc[[-1]]
tomorrow_prediction = RFC_model.predict(tomorrow_data[predictors])
# Result of the prediction
if tomorrow_prediction == 1:
    print("Tomorrow's price is predicted to go up.")
else:
    print("Tomorrow's price is predicted to go down.")




