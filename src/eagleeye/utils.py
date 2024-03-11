import functools
import operator
import pathlib


import arviz as az
import streamlit as st


@st.cache_data
def load_data(path):
    return az.from_netcdf(path)


def combine_charts(charts: list):
    return functools.reduce(operator.add, charts)
