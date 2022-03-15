import streamlit as st

st.text('Welcome')
st.text('Please upload your Amazon data')
st.sidebar.subheader("yan kol")
uploaded_file = st.sidebar.file_uploader(label = 'upload your file', type = ['csv', 'xlsx'])


class calculation:      
    def csv_calculation(uploaded_file):
        import pandas as pd
        import numpy as np
        sessions_limit = 10
        impression_limit = 100
        df = pd.read_csv(uploaded_file)
        df['Sessions'] = pd.to_numeric(df['Sessions'], errors='coerce')
        df['Total Order Items'] = pd.to_numeric(df['Total Order Items'], errors='coerce')
        df['impression'] = pd.to_numeric(df['impression'], errors='coerce')
        df['des_not_disc'] = (df['Total Order Items'] / df['Sessions'] / df['impression'] * 1000)
        df['disc_not_des'] = (1 / df['des_not_disc'])
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df = df.dropna()
        df = df[df.Sessions > sessions_limit]
        df = df.sort_values(by=['des_not_disc'], ascending = False)[:5]
        return df['(Child) ASIN'][:5]

st.text(calculation.csv_calculation(uploaded_file))

