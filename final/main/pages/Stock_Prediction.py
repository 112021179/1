import streamlit as st
import datetime
import time
import pandas as pd
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

st.title('📊Stock Prediction Application')

# Check if a symbol exists
def check_stock_symbol(symbol):
  if isinstance(symbol, str):
    stock = yf.Ticker(symbol)
    _ = stock.history(period="1d")  
    return True  
  else:
    return False
    
def get_company_name(symbol):
  if isinstance(symbol, str):
    stock = yf.Ticker(symbol)
    info = stock.info
    company_name = info['longName']
    return company_name
  else:
    return None

# Preprocessing the dataset
def cleaning_data(dataset): 
  df = dataset
  df = df.drop("Adj Close", axis = 1)
  df["Target"] = ((df["Close"] - df["Open"]) > 0).astype(int)
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

# Predicting the data
def predict(train, test, predictors, model): 
  model.fit(train[predictors], train["Target"])
  preds = model.predict_proba(test[predictors])[:,1] 
  preds[preds >= .6] = 1
  preds[preds < .6] = 0
  preds = pd.Series(preds, index = test.index, name = "Predictions")
  combined = pd.concat([test["Target"], preds], axis = 1)
  return combined

# Testing the machine learning model
def backtesting(data, model, predictors, start = 1250, step = 250):
  all_preds = [] 

  for i in range(start, data.shape[0], step):
    train = data.iloc[0:i].copy()
    test = data.iloc[i:(i+step)].copy()
    all = predict(train, test, predictors, model)
    all_preds.append(all)

  return pd.concat(all_preds)



# Fetch and clean data
def main():

  button_state = st.button("Load Stock Prediction Model")
  if button_state:
  # Disable the button to prevent multiple clicks
    button_state = st.button("Loading...", disabled=True)

    # Display progress bar while the model is loading
    with st.spinner("Loading Stock Prediction Model..."):
      df, predictors = cleaning_data(data)

      # Machine learning model
      RFC_model = RandomForestClassifier(n_estimators=200, min_samples_split=50, random_state=1)
      predictions = backtesting(df, RFC_model, predictors)

      # Display results
      st.subheader("Classification Report:")
      st.text(classification_report(predictions["Target"], predictions["Predictions"]))
      st.markdown("---")

      # Tomorrow's prediction
      st.subheader("Tomorrow price prediction")
      tomorrow_data = df.iloc[[-1]]
      tomorrow_prediction = RFC_model.predict(tomorrow_data[predictors])
      if tomorrow_prediction == 1:
          st.write(f"Tomorrow's price for {company_name} ({symbol}) is predicted to go up.")
      else:
          st.write(f"Tomorrow's price for {company_name} ({symbol}) is predicted to go down.")

    # Once loading is complete, display the success message
    st.success("Stock prediction model loaded successfully!")

    if st.button("Retry"):
      button_state = st.button("Load Prediction Model")

if __name__ == "__main__":
  st.sidebar.header('Stock Symbol')
  symbol = st.sidebar.text_input("Enter Stock Symbol", value="AAPL", max_chars=5)

  # Download data using yfinance
  if check_stock_symbol(symbol):
    data = yf.download(symbol, start="1971-02-05", end=datetime.datetime.today(), interval='1d')
    company_name = get_company_name(symbol)
    main()
  else:
    st.error("Stock symbol doesn't exist. Please try again")