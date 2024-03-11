import functools
import operator

import altair as alt
import pandas as pd
import streamlit as st
import logging

from . import preprocessing as pp
from . import utils

X_LABEL = "Visit"
Y_LABEL = "Body weight [g]"


def prediction(fig, data: pd.DataFrame):
    chart = alt.Chart(pp.get_predictions(data)
                ).mark_line(
                ).encode(
                    alt.X('index').title(X_LABEL),
                    alt.Y('prediction').title(Y_LABEL).scale(zero=False)
                )
    fig.append(chart)


def forecast(fig, data: pd.DataFrame):
    chart = alt.Chart(pp.get_forecast(data)
            ).mark_circle(
                color="red"
            ).encode(
                alt.X('index'),
                alt.Y('forecast').scale(zero=False)
            )
    fig.append(chart)


def _conf_int(df, color):
    crt = alt.Chart(df
            ).mark_area(opacity=0.1, color=color
            ).encode(
                alt.X('index').title(X_LABEL),
                alt.Y('upper').scale(zero=False).title(Y_LABEL),
                alt.Y2('lower'))
    return crt


def confidence(fig, data: list[pd.DataFrame]) -> None:
    charts = []

    data_pred = pp.get_confidence(data, mode="predictions")
    for df in data_pred:
        chart = _conf_int(df, color="blue")
        charts.append(chart)

    if st.session_state.ctrl_forecast:
        data_forecast = pp.get_confidence(data, mode="forecast")
        for df in data_forecast:
            chart = _conf_int(df, color="red")
            charts.append(chart)

    fig.append(utils.combine_charts(charts))



def chart(mid: int | None) -> None:
    if mid is None:
        return

    df = utils.load_data(mid)
    chart_elements: list[alt.Chart] = []

    if st.session_state.ctrl_prediction:
        prediction(chart_elements, df)

    if st.session_state.ctrl_confidence:
        confidence(chart_elements, df)

    if st.session_state.ctrl_forecast:
        forecast(chart_elements, df)

    if chart_elements:
        out = functools.reduce(operator.add, chart_elements)
        st.altair_chart(out, use_container_width=True)
