# uncomment below lines of code to install required packages
# !pip install streamlit
# !pip install pandas
# !pip install numpy
# !pip install datetime
# !pip install plotly_express

import streamlit as st
import pandas as pd
import numpy as np
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

if st.sidebar.checkbox('Raw vacinnation data as on '+today):
    df
    
sub_df=df[["location","date","total_vaccinations", "total_vaccinations_per_hundred"]]
      
if st.sidebar.checkbox('Vacinnations progress'):
    sub_df

if st.sidebar.checkbox('Vacinnations progress (countrywise)'):
    # selection of country from 'location'
    country = st.selectbox("Select the country: ", sub_df['location'].unique())
    sub_df_country = sub_df.loc[sub_df['location'] == country].sort_values(by='date', ascending=False)
    sub_df_country
    
    # display of latest figure of vacinnation
    total_vaccinations = sub_df_country['total_vaccinations'].iloc[0]
    total_vaccinations_per_hundred = sub_df_country['total_vaccinations_per_hundred'].iloc[0]
    st.write('Total vacinnations in '+country, 'as on '+today, 'is', total_vaccinations)
    st.write('Total vacinnations per hundred in '+country, 'as on '+today, 'is', total_vaccinations_per_hundred)
    
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
    
    if st.checkbox('Show/Hide graph of total vacinnation'):
        fig = px.line(sub_df_country, x='date', y='total_vaccinations', hover_name="location",title="Total vacinnations of " +country)
        st.plotly_chart(fig, use_container_width=True)

    if st.checkbox('Show/Hide graph of total vacinnation per hundred'):
        fig = px.line(sub_df_country, x='date', y='total_vaccinations_per_hundred', hover_name="location",title="Total vacinnations of " +country)
        st.plotly_chart(fig, use_container_width=True)

st.sidebar.write("For vaccination dataset (updated each morning, London time), check out the [citation](https://www.nature.com/articles/s41562-021-01122-8)", unsafe_allow_html=True)
    
st.sidebar.write("For source code, check out my [github](https://github.com/vinthegreat84/CoVid)", unsafe_allow_html=True)

st.sidebar.write("If you want to get in touch, you can find me on [linkedin](https://www.linkedin.com/in/vinay-babu-81791015/)", unsafe_allow_html=True)