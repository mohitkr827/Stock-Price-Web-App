import streamlit as st
import yfinance as yf
import pandas as pd
import cufflinks as cf
import datetime
import plotly.graph_objects as go

# App title
st.set_page_config(page_title="Stock Price App")
st.markdown('''
# Stock Price App
Select company and date range

*Powered by YFinance*
''')
st.write('---')

# Sidebar
st.sidebar.subheader('Query parameters')
start_date = st.sidebar.date_input("Start date", datetime.date(2022, 10, 1))
end_date = st.sidebar.date_input("End date", datetime.date(2022, 10, 31))

# Retrieving tickers data
ticker_list = pd.read_csv('ticker_list.txt')
tickerSymbol = st.sidebar.selectbox('Stock ticker', ticker_list) # Select ticker symbol
tickerData = yf.Ticker(tickerSymbol) # Get ticker data
tickerDf = tickerData.history(period='1d', start=start_date, end=end_date) #get the historical prices for this ticker

# Ticker information
string_logo = '<img src=%s>' % tickerData.info['logo_url']
st.markdown(string_logo, unsafe_allow_html=True)

string_name = tickerData.info['longName']
st.header('**%s**' % string_name)

string_summary = tickerData.info['longBusinessSummary']
st.info(string_summary)

# Ticker data
st.header('**Ticker data**')
st.write(tickerDf)

# Plots
st.header('**Plot**')

plots_av=('Candlestick (OHLC)','Line Chart')
graph_select=st.selectbox('Select type of plot',plots_av)

#Candlestick Graph
if graph_select=='Candlestick (OHLC)':
    fig = go.Figure()
    fig.add_trace(go.Candlestick( 
    open=tickerDf['Open'], 
    high=tickerDf['High'], 
    low=tickerDf['Low'], 
    close=tickerDf['Close'] ))
    st.plotly_chart(fig)

#Line Chart
if graph_select=='Line Chart':
    vals=('Open','Close','High','Low','Volume')

    selec=st.selectbox('Select plot parameter',vals)
    if selec=='Open':
        st.line_chart(tickerDf.Open)
    if selec=='Close':
        st.line_chart(tickerDf.Close)
    if selec=='High':
        st.line_chart(tickerDf.High)
    if selec=='Low':
        st.line_chart(tickerDf.Low)
    if selec=='Volume':
        st.line_chart(tickerDf.Volume)        
