import argparse
import functools
import operator

import altair as alt
import arviz as az
import pandas as pd
import streamlit as st
import logging

from . import preprocessing as pp
from . import utils

X_LABEL = "Visit"
Y_LABEL = "Body weight [g]"

FigContainer = list[alt.Chart]


def append_measurements(fig: FigContainer, feat: pd.DataFrame) -> None:
    """Append the original measured data to the final chart.

    Args:
        fig:    Final chart container
        feat:   Original weight dataframe
    """
    df = feat.dropna().reset_index()
    chart = alt.Chart(df
            ).mark_point(
                color='grey'
            ).encode(
                alt.X('index'),
                alt.Y('weight').scale(zero=False)
            )
    fig.append(chart)


def append_prediction(fig: FigContainer, idata: az.InferenceData) -> None:
    """Append the models mean prediction to the final chart.

    Args:
        fig:    Final chart container
        idata:  Model inference data
    """
    chart = alt.Chart(pp.get_predictions(idata)
            ).mark_line(
            ).encode(
                alt.X('index').title(X_LABEL),
                alt.Y('prediction').title(Y_LABEL).scale(zero=False)
            )
    fig.append(chart)


def append_forecast(fig: FigContainer, idata: az.InferenceData) -> None:
    """Append the models forecast to the final chart.

    Args:
        fig:    Final chart container
        idata:  Model inference data
    """
    chart = alt.Chart(pp.get_forecast(idata)
            ).mark_circle(
                color="red"
            ).encode(
                alt.X('index'),
                alt.Y('forecast').scale(zero=False)
            )
    fig.append(chart)


def append_credible_interval(fig: FigContainer, idata: az.InferenceData) -> None:
    """Append the credible interval of the model fit  to the final chart.

    Args:
        fig:    Final chart container
        idata:  Model inference data
    """
    charts = []

    data_pred = pp.get_confidence(idata, mode="predictions")
    for df in data_pred:
        chart = _cred_int_chart(df, color="blue")
        charts.append(chart)

    if st.session_state.ctrl_forecast:
        data_forecast = pp.get_confidence(idata, mode="forecast")
        for df in data_forecast:
            chart = _cred_int_chart(df, color="red")
            charts.append(chart)

    fig.append(utils.combine_charts(charts))


def append_threshold(fig: FigContainer, thdf: pd.DataFrame) -> None:
    """Append the weight threshold to the final chart.

    Args:
        fig:    Final chart container
        thdf:   Dataframe
    """
    chart = alt.Chart(thdf
            ).mark_line(
                color='white'
            ).encode(
                alt.X('index'),
                alt.Y('val')
            )
    fig.append(chart)


def annotate_treatment(fig: FigContainer, indicator: pd.DataFrame) -> None:
    """Append the weight threshold to the final chart.

    Args:
        fig:        Final chart container
        indicator:  Tratment indicator variable
    """
    base = alt.Chart(indicator
            ).mark_rule(
                color='green'
            ).encode(
                x='index'
            ).transform_filter(
                alt.FieldGTPredicate(field=indicator.columns[-1], gt=0)
            )
    fig.append(base)


def render_chart_elements(
        feat: pd.DataFrame,
        idata: az.InferenceData,
    ) -> alt.Chart | None:
    """Render the final chart.

    Args:
        feat:   Original weight dataframe
        idata:  Model inference data

    Returns:
        Final chart
    """

    chart_elements: list[alt.Chart] = []

    if st.session_state.ctrl_measurement:
        append_measurements(chart_elements, feat)

    if st.session_state.ctrl_prediction:
        append_prediction(chart_elements, idata)

    if st.session_state.ctrl_confidence:
        append_credible_interval(chart_elements, idata)

    if st.session_state.ctrl_forecast:
        append_forecast(chart_elements, idata)

    if st.session_state.ctrl_threshold:
        append_threshold(chart_elements, _compute_threshold(feat))

    if st.session_state.ctrl_chemo:
        annotate_treatment(chart_elements, _get_indicator(feat, "chemo"))

    if st.session_state.ctrl_radiation:
        annotate_treatment(chart_elements, _get_indicator(feat, "radiation"))

    if st.session_state.ctrl_operation:
        annotate_treatment(chart_elements, _get_indicator(feat, "operation"))

    if chart_elements:
        return utils.combine_charts(chart_elements)
    return None


def _cred_int_chart(df: pd.DataFrame, color: str) -> alt.Chart:
    chart = alt.Chart(df
            ).mark_area(opacity=0.1, color=color
            ).encode(
                alt.X('index').title(X_LABEL),
                alt.Y('upper').scale(zero=False).title(Y_LABEL),
                alt.Y2('lower')
            )
    return chart


def _compute_threshold(feat: pd.DataFrame) -> pd.DataFrame:
    cond = feat[['chemo', 'radiation', 'operation']].sum(axis=1) > 0
    th = feat[cond].iloc[0].weight * (4/5)
    df = pd.DataFrame({'index': feat.index, 'val': th})
    return df


def _get_indicator(df: pd.DataFrame, treatment: str) -> pd.DataFrame:
    return df.reset_index()[['index', treatment]]
