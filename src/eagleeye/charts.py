from typing import cast

import altair as alt
import arviz as az
import pandas as pd
import streamlit as st
from xarray import DataArray

from . import preprocessing as pp
from . import utils

X_LABEL = "Visit"
Y_LABEL = "Body weight [g]"

FigContainer = list[alt.Chart]


def append_measurements(fig: FigContainer, weight: pd.DataFrame) -> None:
    """Append the original measured data to the final chart.

    Args:
        fig:    Final chart container
        feat:   Original weight dataframe
    """
    chart = alt.Chart(weight
            ).mark_point(
                color='grey'
            ).encode(
                alt.X('visit').title(X_LABEL),
                alt.Y('weight').title(Y_LABEL).scale(zero=False)
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


def append_threshold(fig: FigContainer, obs: pd.DataFrame) -> None:
    """Append the weight threshold to the final chart.

    Args:
        fig:    Final chart container
        thdf:   Dataframe
    """
    chart = alt.Chart(obs
            ).mark_rule(
                color='white'
            ).encode(
                alt.Y("threshold")
            )
    fig.append(chart)


def annotate_treatment(fig: FigContainer, indicator: pd.DataFrame) -> None:
    """Append the weight threshold to the final chart.

    Args:
        fig:        Final chart container
        indicator:  Tratment indicator variable
    """
    colormap = {
        'chemo': "green",
        'radiation': "yellow",
        'operation': "red"
    }
    color = colormap[indicator.columns[-1]]
    base = alt.Chart(indicator.reset_index()
            ).mark_rule(
                color=color
            ).encode(
                x='Visit'
            ).transform_filter(
                alt.FieldGTPredicate(field=indicator.columns[-1], gt=0)
            )
    fig.append(base)


def render_chart_elements(
        idata: az.InferenceData,
    ) -> alt.Chart | None:
    """Render the final chart.

    Args:
        idata:  Model inference data

    Returns:
        Final chart
    """

    chart_elements: list[alt.Chart] = []
    obs_weight = pd.DataFrame({
            'visit': idata['constant_data']['visits'].to_numpy(),
            'weight': idata['observed_data']['llh']})

    if st.session_state.ctrl_measurement:
        append_measurements(chart_elements, obs_weight)

    if st.session_state.ctrl_prediction:
        append_prediction(chart_elements, idata)

    if st.session_state.ctrl_confidence:
        append_credible_interval(chart_elements, idata)

    if st.session_state.ctrl_forecast:
        append_forecast(chart_elements, idata)

    if st.session_state.ctrl_threshold:
        append_threshold(chart_elements, _get_threshold(obs_weight))

    if st.session_state.ctrl_chemo:
        annotate_treatment(chart_elements, _get_indicator(idata, "chemo"))

    if st.session_state.ctrl_radiation:
        annotate_treatment(chart_elements, _get_indicator(idata, "radiation"))

    if st.session_state.ctrl_operation:
        annotate_treatment(chart_elements, _get_indicator(idata, "operation"))

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
    return cast(alt.Chart, chart)


def _get_threshold(obs: pd.DataFrame) -> pd.DataFrame:
    th = obs.weight.iloc[0] * (4/5)
    df = pd.DataFrame({'index': [0, obs.index[-1]], 'threshold': [th, th]})
    return df


def _get_indicator(idata: az.InferenceData, treatment: str) -> pd.DataFrame:
    df = idata['constant_data']['treatments'].sel(treatment_type=treatment).to_dataframe(name=treatment)
    df = df.drop(columns='treatment_type')
    df.index.name = "Visit"
    return df
