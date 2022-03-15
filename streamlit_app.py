import streamlit as st
import pandas as pd
import numpy as np

st.text('Welcome')
st.text('Please upload your Amazon data')
#st.sidebar.subheader("yan kol")

try:
    uploaded_file = st.file_uploader(label = 'Upload Your File', type = ['csv', 'xlsx'])
    df = pd.read_csv(uploaded_file)    
    limit = int(st.number_input('minimum limit for views', min_value=1, value=10, step=1))
    result_number = int(st.slider('Product_number', 1, 100))
        
    class calculation:
        def csv_correction(df):
            #df = pd.read_csv(uploaded_file)
            df['Sessions'] = df['Sessions'].replace("," , "", regex=True)
            df['Total Order Items'] = df['Total Order Items'].replace("," , "", regex=True)
            df['Page Views'] = df['Page Views'].replace("," , "", regex=True)                  
            df['Sessions'] = pd.to_numeric(df['Sessions'], errors='coerce')
            df['Total Order Items'] = pd.to_numeric(df['Total Order Items'], errors='coerce')
            df['Page Views'] = pd.to_numeric(df['Page Views'], errors='coerce')
            return df    
        def csv_calculation(uploaded_file):
            df = calculation.csv_correction(uploaded_file)
            df['des_not_disc'] = ((df['Total Order Items'] / df['Sessions']) / df['Page Views'])
            df.replace([np.inf, -np.inf], np.nan, inplace=True)       
            df = df.dropna()
            return df        
        def desirable_but_not_discoverable_items(uploaded_file, sessions_limit, result_count):
            df = calculation.csv_calculation(uploaded_file)
            df = df[df.Sessions > sessions_limit]
            df = df.sort_values(by=['des_not_disc'], ascending = False)
            return df['(Child) ASIN'][:result_count].to_string(index=False)
        def discoverable_but_not_desirable_items(uploaded_file, sessions_limit, result_count):
            df = calculation.csv_calculation(uploaded_file)
            df = df[df.Sessions > sessions_limit]
            df = df.sort_values(by=['des_not_disc'], ascending = False)
            return df['(Child) ASIN'][-result_count:].to_string(index=False)
    
    st.text('Discoverable but not desirable items')
    st.text(calculation.discoverable_but_not_desirable_items(df, limit, result_number))
    
    st.text('Desirable but not discoverable items')
    st.text(calculation.desirable_but_not_discoverable_items(df, limit, result_number))
except:
    st.text('NO DATA NO BUSINESS  :))')
