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


def measurements(fig, feat):
    x = feat.dropna().reset_index()
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


def confidence(fig, data: pd.DataFrame) -> None:
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


def _compute_threshold(feat) -> pd.DataFrame:
    cond = feat[['chemo', 'radiation', 'operation']].sum(axis=1) > 0
    th = feat[cond].iloc[0].weight * (4/5)
    df = pd.DataFrame({'index': feat.index, 'val': th})
    return df

def threshold(fig, thdf) -> None:
    c = alt.Chart(thdf
          ).mark_line(
                  color='white'
          ).encode(
                  alt.X('index'),
                  alt.Y('val'))
    fig.append(c)


def _get_indicator(df, var):
    g = df.groupby("mouse_id")
    out = g.get_group(3).dropna().reset_index()
    return out[['index', var]]


def annotate_treatment(fig, indicator):
    base = alt.Chart(indicator
            ).mark_rule(
                color='green'
            ).encode(
                x='index'
            ).transform_filter(
                alt.FieldGTPredicate(field=indicator.columns[-1], gt=0)
            )
    fig.append(base)


def chart(feat, trace, args) -> None:

    chart_elements: list[alt.Chart] = []

    if st.session_state.ctrl_prediction:
        prediction(chart_elements, trace)

    if st.session_state.ctrl_confidence:
        confidence(chart_elements, trace)

    if st.session_state.ctrl_forecast:
        forecast(chart_elements, trace)

    if st.session_state.ctrl_threshold:
        threshold(chart_elements, _compute_threshold(feat))

    if st.session_state.ctrl_measurement:
        measurements(chart_elements, feat)

    if st.session_state.ctrl_chemo:
        annotate_treatment(chart_elements, _get_indicator(feat, "chemo"))

    if st.session_state.ctrl_radi:
        annotate_treatment(chart_elements, _get_indicator(feat, "radiation"))

    if st.session_state.ctrl_op:
        annotate_treatment(chart_elements, _get_indicator(feat, "operation"))

    if chart_elements:
        out = functools.reduce(operator.add, chart_elements)
        st.altair_chart(out, use_container_width=True)
