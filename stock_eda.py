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
                ('Comparision',"daily return"))

inds=st.sidebar.selectbox('Choose the Industry',
                ('Oil', 'Agriculture', 'Tech','Index_Bank','Index_oil'))

per=st.sidebar.selectbox('Choose the period',
                ('1y', '3y'))


inter=st.sidebar.selectbox('Choose the interval',
                    ('1d', '1wk','1mo'))

#age = st.sidebar.slider('Choose the period', 1, 5, 3)

names={"Oil":["ONGC.NS","XOM"],
       "Agriculture":["RALLIS.NS","BAYERCROP.NS"],
       "Tech":["TCS.NS","NOW"],
       "Index_Bank":["^NSEBANK","^BKX"],
       "Index_oil":['OIL.NS','CL=F']
       }

#reading the data
selected_stock =names[inds]
data_ind = yf.download(tickers=selected_stock[0], 
                period=per, 
                interval=inter)
data_us = yf.download(tickers=selected_stock[1], 
                period=per, 
                interval=inter)

data=pd.merge(data_ind["Close"], data_us["Close"], left_index=True, right_index=True)
data.columns=["INDIA ","US "]

#visualization
if layout=='Comparision':
        col1, col2 = st.columns(2)
        with col1:
                
                st.markdown(f"<h5 style='text-align: center;'> India </h5>",unsafe_allow_html=True)
                st.line_chart(data_ind.Close,width =500 ,height=250)
                if selected_stock[0]=='ONGC.NS':
                    st.write('The Oil and Natural Gas Corporation is an Indian oil and gas explorer and producer. It is under the ownership of Ministry of Petroleum and Natural Gas and Government of India.')
                elif selected_stock[0]=='RALLIS.NS':
                    st.write("Rallis, a Tata Enterprise, is a subsidiary of Tata Chemicals, with its business presence in the farm essentials vertical. It is one of India's leading crop care companies.")
                elif selected_stock[0]=='TCS.NS':
                    st.write('Tech Mahindra is an Indian multinational information technology services and consulting company. Part of the Mahindra Group, the company is headquartered in Pune')
                elif selected_stock[0]=='^NSEBANK':
                    st.write('Bank Nifty represents the 12 most liquid and large capitalised stocks from the banking sector which trade on the National Stock Exchange (NSE). It provides investors and market intermediaries a benchmark that captures the capital market performance of Indian banking sector.')
                elif selected_stock[0]=='OIL.NS':
                    st.write('India Oil Index represents the 10 most liquid and large capitalised stocks from the oil and gas sector which trade on the National Stock Exchange (NSE). It provides investors and market intermediaries a benchmark that captures the capital market performance of Indian OIl and gas sector.')
        with col2:
                st.markdown(f"<h5 style='text-align: center;'>United States</h5>",unsafe_allow_html=True)
                st.line_chart(data_us.Close,width =500 ,height=250,)
                if selected_stock[1]=='XOM':
                    st.write('Exxon Mobil Corporation, stylized as ExxonMobil, is an American multinational oil and gas corporation headquartered in Irving, Texas.')
                elif selected_stock[1]=='BAYERCROP.NS':
                    st.write("Crop Science Division | Bayer. Bayer's leadership in Crop Science provides tailored solutions for farmers to plant, grow and protect their harvests using less land, water and energ")
                elif selected_stock[1]=='NOW':
                    st.write('International Business Machines Corporation is an American multinational technology corporation headquartered in Armonk, New York, with operations in over 171 countries.')
                elif selected_stock[1]=='^BKX':
                    st.write('The KBW Bank Index is a benchmark stock index of the banking sector. It includes a weighting of 24 banking stocks selected as indicators of this industry group. The stocks represent large U.S. national money center banks, regional banks, and thrift institutions.')
                elif selected_stock[1]=='CL=F':
                    st.write('US Oil Index')                
        from sklearn.preprocessing import MinMaxScaler ,StandardScaler
        mms=MinMaxScaler()
        data=pd.DataFrame(mms.fit_transform(data),columns=["Indian company","US company"],index=data.index)
        st.markdown(f"<h5 style='text-align: center;'>{selected_stock[0]} v/s {selected_stock[1]}</h5>",unsafe_allow_html=True)
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