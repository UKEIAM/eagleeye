"""
Common utilities
"""
import functools
import operator
import pathlib
from typing import cast

import altair as alt
import arviz as az
import pandas as pd
import streamlit as st


@st.cache_data
def load_idata(path: pathlib.Path | str) -> az.InferenceData:
    """Load model inference data.

    Args:
        path: Path to inference data file
    """
    return cast(az.InferenceData, az.from_netcdf(path))


@st.cache_data
def load_features(path: pathlib.Path | str) -> pd.DataFrame:
    """Load original training data.

    Args:
            path: Path to training data file
    """
    data = pd.read_pickle(path)
    if isinstance(data, pd.Series):
        data = pd.DataFrame(data)
    return cast(pd.DataFrame, data)


def combine_charts(charts: list[alt.Chart]) -> alt.Chart:
    """Combine multiple altair charts.

    Args:
        charts: list of altair charts

    Returns:
        Combined chart
    """
    return functools.reduce(operator.add, charts)
