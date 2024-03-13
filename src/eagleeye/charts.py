import functools
import operator

import altair as alt
from altair import datum
import pandas as pd
import streamlit as st
import logging

from . import preprocessing as pp
from . import utils

X_LABEL = "Visit"
Y_LABEL = "Body weight [g]"


def measurements(fig, data: pd.DataFrame):
    df = pd.read_pickle("../de.uke.iam.mouse/data/features-with-indicators.pkl")
    g = df.groupby("mouse_id")
    x = g.get_group(3).dropna().reset_index()

    c = alt.Chart(x).mark_point(color='grey').encode(alt.X('index'),
                                                     alt.Y('weight').scale(zero=False))
    fig.append(c)


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


def threshold(fig, data) -> None:
    cond = x[['chemo', 'radiation', 'operation']].sum(axis=1) > 0
    th = x[cond].iloc[0].weight * (4/5)
    v = pd.DataFrame({'index': x['index'], 'val': th})
    c = alt.Chart(v
                  ).mark_line(
                          color='white'
                  ).encode(
                          alt.X('index'),
                          alt.Y('val'))
    fig.append(c)


def _get_indicator(var):
    raw = pd.read_pickle("../de.uke.iam.mouse/data/features-with-indicators.pkl")
    g = raw.groupby("mouse_id")
    df = g.get_group(3).dropna().reset_index()
    return df[['index', var]]


def annotate_treatment(fig, ttype: str):
    indi = _get_indicator(ttype)
    base = alt.Chart(indi
            ).mark_rule(
                color='green'
            ).encode(
                x='index'
            ).transform_filter(
                alt.FieldGTPredicate(field=ttype, gt=0)
            )
    fig.append(base)


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

    if st.session_state.ctrl_threshold:
        threshold(chart_elements, df)

    if st.session_state.ctrl_measurement:
        measurements(chart_elements, None)

    if st.session_state.ctrl_chemo:
        annotate_treatment(chart_elements, "chemo")

    if st.session_state.ctrl_radi:
        annotate_treatment(chart_elements, "radiation")

    if st.session_state.ctrl_op:
        annotate_treatment(chart_elements, "operation")

    if chart_elements:
        out = functools.reduce(operator.add, chart_elements)
        st.altair_chart(out, use_container_width=True)
