import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import date
import plotly.express as px

url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv'
df = pd.read_csv(url) 

today = date.today().strftime("%d %b, %Y")

st.title("Covid Vaccination Analysis")

if st.checkbox('Raw data as on '+today):
    df
    
sub_df=df[["location","date","total_vaccinations"]]
      
if st.checkbox('Total vacinnations'):
    sub_df

if st.checkbox('Total vacinnations (countrywise)'):
    location = st.radio("Select the country: ", sub_df['location'].unique())
    sub_df_location=sub_df.loc[sub_df['location']==location].sort_values(by='date', ascending=False)
    sub_df_location
    fig = px.bar(sub_df_location, x='date', y='total_vaccinations',title="Total vacinnations of " +location)
    st.plotly_chart(fig, use_container_width=True)