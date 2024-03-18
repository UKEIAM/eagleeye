import functools
import operator
import pathlib


import arviz as az
import pandas as pd
import streamlit as st


@st.cache_data
def load_data(path):
    return az.from_netcdf(path)

@st.cache_data
def load_features(path):
    return pd.read_pickle(path)

def combine_charts(charts: list):
    return functools.reduce(operator.add, charts)
