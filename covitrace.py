# uncomment below lines of code to install required packages
# !pip install streamlit
# !pip install pandas
# !pip install numpy
# !pip install datetime
# !pip install plotly_express

import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta
import plotly.express as px

@st.cache
def fetch_data():
    url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv'
    df = pd.read_csv(url)
    df['date'] = pd.to_datetime(df['date']).dt.date
    return df
    
df = fetch_data()

# url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv'
# df = pd.read_csv(url)
# df['date'] = pd.to_datetime(df['date']).dt.date

today = date.today().strftime("%d %b, %Y")

st.title("Covid Vaccination Analysis - 1.0")
st.write('## Welcome to the Covid Vaccination Analysis')
st.write('### Created by Vinay Babu')
st.write('''The covitrace is a tool designed using Python and Streamlit to analyse covid vacinnation.''')

st.sidebar.title("Covid Vaccination Analysis")

if st.sidebar.checkbox('Raw data as on '+today):
    df
        
    # data downloading as 'csv'
    @st.cache
    def convert_df(df):
        return df.to_csv().encode('utf-8')
    
    csv = convert_df(df)
    
    st.download_button(
   "Press to download data",
   csv,
   "file.csv",
   "text/csv",
   key='download1-csv'
    )

if st.sidebar.checkbox('Date filter'):
    N_DAYS = 30 # set for '30' days; may be changed for the default view
#     today = datetime.now()
    start = datetime.now() - timedelta(days=N_DAYS)
    end = datetime.now()
    
    start_date = st.sidebar.date_input('Start date (default set for 30 days back)', start)
    end_date = st.sidebar.date_input('End date (default set for today)', end) 
    if start_date < end_date:
        pass
        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        df = df.loc[mask]
    else:
        st.error('Error: End date should be chosen after the start day.')
    
sub_df=df[["location","date","total_vaccinations", "total_vaccinations_per_hundred"]]

if st.sidebar.checkbox('Vacinnations progress (global)'):
    sub_df    
        
    # data downloading as 'csv'
    @st.cache
    def convert_df(sub_df):
        return sub_df.to_csv().encode('utf-8')
    
    csv = convert_df(sub_df)
    
    st.download_button(
   "Press to download data",
   csv,
   "file.csv",
   "text/csv",
   key='download2-csv'
    )

# Vacinnations progress (countrywise)     
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
   key='download3-csv'
    )
    
    if st.checkbox('Show/Hide graph of total vacinnations'):
        fig = px.line(sub_df_country, x='date', y='total_vaccinations', hover_name="location",title="Total vacinnations of " +country)
        st.plotly_chart(fig, use_container_width=True)

    if st.checkbox('Show/Hide graph of total vacinnation per hundreds'):
        fig = px.line(sub_df_country, x='date', y='total_vaccinations_per_hundred', hover_name="location",title="Total vacinnations per hundred of " +country)
        st.plotly_chart(fig, use_container_width=True)
        
# Vacinnations progress (countrywise comparison)     
if st.sidebar.checkbox('Vacinnations progress (comparison)'):
    # selection of country from 'location'
    country = st.multiselect("Select the countries: ", sub_df['location'].unique())
    sub_df_country_comparison = sub_df[sub_df['location'].isin(country)].sort_values(by='date', ascending=False)
    sub_df_country_comparison
    
    # data downloading as 'csv'
    @st.cache
    def convert_df(sub_df_country_comparison):
        return sub_df_country_comparison.to_csv().encode('utf-8')
    
    csv = convert_df(sub_df_country_comparison)
    
    st.download_button(
   "Press to download data",
   csv,
   "file.csv",
   "text/csv",
   key='download4-csv'
    )
    
    if st.checkbox('Show/Hide graph of total vacinnations for countrywise comparison'):
        fig = px.line(sub_df_country_comparison, x='date', y='total_vaccinations', color="location", hover_name="location",title="Total vacinnations")
        st.plotly_chart(fig, use_container_width=True)

    if st.checkbox('Show/Hide graph of total vacinnations per hundred for countrywise comparison'):
        fig = px.line(sub_df_country_comparison, x='date', y='total_vaccinations_per_hundred', color="location", hover_name="location",title="Total vacinnations_per_hundred")
        st.plotly_chart(fig, use_container_width=True)
        
st.sidebar.write("For vaccination dataset (updated each morning, London time), check out the [citation](https://www.nature.com/articles/s41562-021-01122-8)", unsafe_allow_html=True)
    
st.sidebar.write("For source code, check out my [github](https://github.com/vinthegreat84/CoVid)", unsafe_allow_html=True)

st.sidebar.write("If you want to get in touch, you can find me on [linkedin](https://www.linkedin.com/in/vinay-babu-81791015/)", unsafe_allow_html=True)
