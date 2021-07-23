  
import streamlit as st

import pandas_datareader.data as web
import pandas as pd

import datetime as dt
import webbrowser
from time import sleep

import yfinance as yf
import mplfinance as mpf
import plotly.graph_objects as go


def data_extraction(Symbol, Tick, inter):
        # extracting data from Yahoo API
        
        stock = yf.Ticker(Symbol)
        if inter == '1m'or inter == '1m' or inter == '2m' or inter == '5m' or inter == '15m':
            data = stock.history(period = '1d', interval = inter)
        elif inter == '30m'or inter == '60m' or inter == '90m' or inter == '1h' or inter == '1d':
            data = 0
            data = stock.history(period = '1mo', interval = inter)
        else:
            data = 0
            data = stock.history(period = 'max', interval = inter)

        df=pd.DataFrame(data)
        if st.sidebar.checkbox('View Stock Data'):
            st.subheader(Tick + " OHLC Data")
            st.dataframe(df)
        chart(df, Tick, inter)
        
        

def chart(df, Tick, inter):
        #charting the stock data
        graphtype = st.selectbox('Chart Type', ('candle', 'ohlc', 'line', 'renko', 'pnf'))
        #fig = mpf.plot(df, type=graphtype, figratio=(20,9), style='nightclouds')
        #st.set_option('deprecation.showPyplotGlobalUse', False)
        #st.pyplot(fig)

        fig = go.Figure(
        data = [
                        go.Candlestick(
                                x = df.index,
                                open = df['Open'],
                                high = df['High'],
                                low = df['Low'],
                                close = df['Close'],
                                name = Tick,
                                increasing_line_color = 'green',
                                decreasing_line_color = 'red'
                        )
                ]
        )
        fig.update_layout(
                title=Tick+ " " +inter + ' Chart',
                xaxis_title="Date",
                yaxis_title="Price (₹)",
                font=dict(
                    family="Courier New, monospace",
                    size=12,
                    color="black"
                ),
                width=10000,
                height=750
            )
        st.plotly_chart(fig, use_container_width=True)
            
        
def company_data(symbol, Tick):
        # getting company data from ticker
        tick = yf.Ticker(symbol)
        company_name = tick.info['longName']
        year_high = tick.info['fiftyTwoWeekHigh']
        year_low = tick.info['fiftyTwoWeekLow']
        day_high = tick.info['dayHigh']
        day_low = tick.info['dayLow']
        mkcap = tick.info['marketCap']
        st.write(Tick + " : " + company_name)
        st.write("Market Cap :", mkcap)
        st.write("52 Week High:", year_high, "52 Week Low :", year_low)
        st.write("Day High:", day_high, "Day Low :", day_low)


def main():
    st.title('Blue Pheonix v1.1.1')
    Tick = st.sidebar.text_input("Enter Ticker: ", 'MRF')
    Symbol = Tick.upper() + ".NS" 
    inter = st.sidebar.selectbox("Enter TimeFrame", ('1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'))
        
    if st.sidebar.checkbox('View Stock Info'):
        company_data(Symbol , Tick)
    data = data_extraction(Symbol, Tick, inter)
    if st.sidebar.checkbox('Predict Stock Price Movement'):
            price_prediction(Symbol)
    #if st.sidebar.button('Back',help="go back to the dashboard"):
        #url = "http://127.0.0.1:8000/"
        #webbrowser.open(url, new=0, autoraise=True) 
     


if __name__ == "__main__":
        main()


 
