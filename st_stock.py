import numpy as np
import pandas as pd
import yfinance as yf
import streamlit as st
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import plotly.express as px


#page layout

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>Stock price</h1>",
             unsafe_allow_html=True)

layout=st.sidebar.selectbox('Choose the Industry',
                ( 'Comparision',"daily return"))

inds=st.sidebar.selectbox('Choose the Industry',
                ('Oil Index','Oil Companies', 'Agriculture', 'Tech','Banking'))

per=st.sidebar.selectbox('Choose the period',
                ('1y', '3y'))


inter=st.sidebar.selectbox('Choose the interval',
                    ('1d','1mo'))


#age = st.sidebar.slider('Choose the period', 1, 5, 3)

names={"Oil":["ONGC.NS","DE"],
       "Agriculture":["GODREJAGRO.NS","XOM"],
       "Tech":["TCS.NS","NOW"],
       "Banking":["^NSEBANK","^BKX"]}

#reading the data
selected_stock =names[inds]
data_ind = yf.download(tickers=selected_stock[0], 
                period=per, 
                interval=inter)
data_us = yf.download(tickers=selected_stock[1], 
                period=per, 
                interval=inter)

data=pd.merge(data_ind["Close"], data_us["Close"], left_index=True, right_index=True)
data.columns=["Indian compnay","US compnay"]

#visualization 
if layout=='Seprate':
        col1, col2 = st.columns(2)
        with col1:
                st.markdown(f"<h5 style='text-align: center;'> {selected_stock[0]} </h5>",unsafe_allow_html=True) #labelling
                st.line_chart(data_ind.Close,width =500 ,height=250)
        with col2:
                st.markdown(f"<h5 style='text-align: center;'>{selected_stock[1]}</h5>",unsafe_allow_html=True) #labelling
                st.line_chart(data_us.Close,width =500 ,height=250,)
        from sklearn.preprocessing import MinMaxScaler ,StandardScaler
        mms=MinMaxScaler()
        data=pd.DataFrame(mms.fit_transform(data),columns=["Inidan compnay","US compnay"],index=data.index)
        st.markdown(f"<h5 style='text-align: center;'>{selected_stock[0]} v/s {selected_stock[1]}</h5>",unsafe_allow_html=True) #labelling 
        st.line_chart(data,)



elif layout=='daily return':
        data_ind['Day_Perc_Change']= data_ind['Close'].pct_change()*100
        data_us['Day_Perc_Change'] = data_us['Close'].pct_change()*100

        col1, col2 = st.columns(2)
        with col1:
                st.line_chart(data_ind.Day_Perc_Change,width =500 ,height=350)
                st.markdown("<h6 style='text-align: left;'>It can be observed that for most of the days, the returns are between -2% to 2% with few spikes in between crossing 6% mark on both the sides.</h1>", unsafe_allow_html=True)
        with col2:
                st.line_chart(data_us.Day_Perc_Change,width =500 ,height=350,)
                st.markdown("<h6 style='text-align: left;'>It can be observed that for most of the days, the returns are between -2% to 2% with few spikes in between crossing 6% mark on both the sides.</h1>", unsafe_allow_html=True)


     



#st.line_chart(data_us.Close)

#plt.plot(data.index,data["Close_x"])
#plt.plot(data.index,data["Close_y"])
#st.pyplot(plt)
#st.line_chart(sd,width =1500 ,height=350,)
#st.line_chart(data.set_index(data.Date)[data])
