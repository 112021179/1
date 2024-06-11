import streamlit as st
import datetime
import pandas as pd
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

st.title('📊Stock Prediction Application')

# Predefined list of valid symbols with company names
valid_symbols = {
    'AAPL': 'Apple Inc.',
    'MSFT': 'Microsoft Corporation',
    'AMZN': 'Amazon.com Inc.',
    'TSLA': 'Tesla Inc.',
    'GOOGL': 'Alphabet Inc. (Google)',
    'META': 'Meta Platforms Inc.',
    'NFLX': 'Netflix Inc.',
    'NVDA': 'NVIDIA Corporation',
    'ADBE': 'Adobe Inc.',
    'CRM': 'Salesforce Inc.',
    'ORCL': 'Oracle Corporation',
    'CSCO': 'Cisco Systems Inc.',
    'INTC': 'Intel Corporation',
    'IBM': 'International Business Machines Corporation',
    'VZ': 'Verizon Communications Inc.',
    'T': 'AT&T Inc.',
    'JPM': 'JPMorgan Chase & Co.',
    'BAC': 'Bank of America Corporation',
    'WFC': 'Wells Fargo & Company',
    'C': 'Citigroup Inc.',
    'GS': 'Goldman Sachs Group Inc.',
    'MS': 'Morgan Stanley',
    'UNH': 'UnitedHealth Group Incorporated',
    'JNJ': 'Johnson & Johnson',
    'PFE': 'Pfizer Inc.',
    'ABT': 'Abbott Laboratories',
    'XOM': 'ExxonMobil Corporation',
    'CVX': 'Chevron Corporation',
    'COP': 'ConocoPhillips',
    'HD': 'The Home Depot Inc.',
    'LOW': 'Lowe\'s Companies Inc.',
    'WMT': 'Walmart Inc.',
    'TGT': 'Target Corporation',
    'COST': 'Costco Wholesale Corporation',
    'NKE': 'Nike Inc.',
    'MCD': 'McDonald\'s Corporation',
    'SBUX': 'Starbucks Corporation',
    'DIS': 'The Walt Disney Company',
    'CMCSA': 'Comcast Corporation',
    'F': 'Ford Motor Company',
    'GM': 'General Motors Company',
    'BA': 'The Boeing Company',
    'UAL': 'United Airlines Holdings Inc.',
    'DAL': 'Delta Air Lines Inc.',
    'LUV': 'Southwest Airlines Co.',
    'AAL': 'American Airlines Group Inc.'
}

# Display symbol and company name in the selectbox
symbol_options = [f"{symbol} ({company_name})" for symbol, company_name in valid_symbols.items()]

st.sidebar.header('Stock Symbol')
symbol = st.sidebar.selectbox("Select a stock symbol:", symbol_options)

# Extract the symbol from the selected option
symbol = symbol.split(" (")[0]

# Download data using yfinance
data = yf.download(symbol, start="1971-02-05", end=datetime.datetime.today(), interval='1d')

# Preprocessing the dataset
def cleaning_data(dataset): 
    df = dataset
    # df.to_csv(f'{symbol}.csv')
    # df = pd.read_csv(f"{symbol}.csv")
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
try:
    company_name = valid_symbols[symbol]
    df, predictors = cleaning_data(data)

    # Machine learning model
    RFC_model = RandomForestClassifier(n_estimators=200, min_samples_split=50, random_state=1)
    predictions = backtesting(df, RFC_model, predictors)

    # Display results
    st.write(predictions)
    st.write("Classification Report:")
    st.text(classification_report(predictions["Target"], predictions["Predictions"]))

    # Tomorrow's prediction
    tomorrow_data = df.iloc[[-1]]
    tomorrow_prediction = RFC_model.predict(tomorrow_data[predictors])
    if tomorrow_prediction == 1:
        st.write(f"Tomorrow's price for {company_name} ({symbol}) is predicted to go up.")
    else:
        st.write(f"Tomorrow's price for {company_name} ({symbol}) is predicted to go down.")
except Exception as e:
    st.write("Error fetching data. Please check the stock symbol and try again.")
    st.write(str(e))
