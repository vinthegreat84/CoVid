import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import date
import plotly.express as px

url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv'
df = pd.read_csv(url) 

today = date.today().strftime("%d %b, %Y")

st.title("Covid Vaccination Analysis - 1.0")
st.write('## Welcome to the Covid Vaccination Analysis')
st.write('### Created by Vinay Babu')
st.write('''Covid Vaccination Analysis is a tool designed using Python and Streamlit to analyse covid vacinnation.''')

st.sidebar.title("Covid Vaccination Analysis")

if st.checkbox('Raw data as on '+today):
    df
    
sub_df=df[["location","date","total_vaccinations"]]
      
if st.checkbox('Total vacinnations'):
    sub_df

if st.checkbox('Total vacinnations (countrywise)'):
    # selection of country from 'location'
    country = st.radio("Select the country: ", sub_df['location'].unique())
    sub_df_country = sub_df.loc[sub_df['location'] == country].sort_values(by='date', ascending=False)
    sub_df_country
    
    # data downloading as 'csv'
    @st.cache
    def convert_df(sub_df_country):
        return sub_df_country.to_csv().encode('utf-8')
    
    csv = convert_df(sub_df_country)
    
    st.download_button(
   "Press to download data",
   csv,
   "file.csv",
   "text/csv",
   key='download-csv'
    )
    
    fig = px.bar(sub_df_country, x='date', y='total_vaccinations',title="Total vacinnations of " +country)
    st.plotly_chart(fig, use_container_width=True)

st.sidebar.write("For vaccination dataset, check out [citation](https://www.nature.com/articles/s41562-021-01122-8)", unsafe_allow_html=True)
    
st.sidebar.write("For source code, check out my [github](https://github.com/vinthegreat84/CoVid)", unsafe_allow_html=True)

st.sidebar.write("If you want to get in touch, you can find me on [linkedin](https://www.linkedin.com/in/vinay-babu-81791015/)", unsafe_allow_html=True)