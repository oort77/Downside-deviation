#!/usr/bin/env python
# coding: utf-8


import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
plt.rcParams["figure.figsize"] = [12, 8]
plt.rcParams["figure.dpi"] = 120
plt.style.use('ggplot')


st.set_page_config(page_title='WHO COVID statistics',
                   page_icon='./lincoln_indy.ico', layout='wide', initial_sidebar_state='auto')

with open('./df.pickle', 'rb') as f:
    df = pickle.load(f)


target = st.sidebar.slider('Target', min_value=-15, max_value=40, value=1)

col1, col2 = st.columns([3, 5])

with col1:
    st.header("Data")
    df['Return-Target'] = df['Return'] - target
    st.dataframe(df)
    # st.image("https://static.streamlit.io/examples/cat.jpg")

with col2:
    st.header("Plot")

    downside_deviation = np.sqrt(
        ((df.loc[df['Return-Target'] < 0, 'Return-Target'])**2).sum()/df.shape[0])
    upside_deviation = np.sqrt(
        ((df.loc[df['Return-Target'] > 0, 'Return-Target'])**2).sum()/df.shape[0])

    st.write(
        f'**Downside deviation** = {downside_deviation:.2f}, **upside deviation** = {upside_deviation:.2f}')

    fig, ax = plt.subplots(figsize=(11, 8))  # ,dpi=1000
    df.plot.bar(x='Year', y='Return', color='b', ax=ax)
    plt.annotate(f'Target: {target:.2f}', (-0.35, target+2))
    plt.annotate(f'Up dev: {upside_deviation:.2f}',
                 (-0.35, target+upside_deviation+2))
    plt.annotate(f'Down dev: {downside_deviation:.2f}',
                 (-0.35, target-downside_deviation-2))
    plt.axhline(y=target, xmin=-10, xmax=100, color='r', label='Target')
    plt.axhline(y=0, xmin=-10, xmax=100,  color='b')
    plt.axhline(y=target - downside_deviation, xmin=-10, xmax=100, color='k')
    plt.axhline(y=target + upside_deviation, xmin=-10, xmax=100, color='g')
    plt.legend()
    st.pyplot(fig)

    # st.image("https://static.streamlit.io/examples/dog.jpg")
