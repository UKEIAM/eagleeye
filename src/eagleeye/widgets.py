"""
Define UI controls
"""
import pathlib

import streamlit as st


def mouse_id_selector(data_path: pathlib.Path) -> None:
    ids = [None]
    ids.extend(p.stem for p in sorted(data_path.glob("*.ndf"), key=lambda x: int(x.stem)))
    st.sidebar.selectbox("Select mouse ID", ids, key="ctrl_id_select")


def data_elements() -> None:
    _widget_def = {
        'Measurement': {
            'value': True,
            'key': "ctrl_measurement",
            'help': "Original measurements from the lab"},

        'Mean Prediction': {
            'value': True,
            'key': "ctrl_prediction",
            'help': ("Mean prediction of the body weight according to the "
                     "underlying auto-regressive model.")},

        'Confidence Interval' : {
             'value': False,
             'key': "ctrl_confidence",
             'help': "Confidence intervall of the mean prediction."},


        'Threshold': {
            'value': False,
            'key': "ctrl_threshold",
            'help': ("20 % drop-off of the body weight at the first "
                     "recorded treatment.")},

        'Forecast': {
            'value': False,
            'key': "ctrl_forecast",
            'help': "Mean future development of the body weight."},
    }

    st.sidebar.caption("Data elements")
    for label, kwargs in _widget_def.items():
        st.sidebar.toggle(label, **kwargs)


def annotations():
    _widget_def = {
        '\U0001F9ea Chemo therapie': {
            'value': False,
            'key': "ctrl_chemo"},

        '\U00002622 Radioation': {
            'value': False,
            'key': "ctrl_radi"},

        '\U0001FAC0 OP': {
            'value': False,
            'key': "ctrl_op"},
    }

    st.sidebar.caption("Treatment annotations")
    for label, kwargs in _widget_def.items():
        st.sidebar.toggle(label, **kwargs)


def init_ui_controls(args):
    mouse_id_selector(args.data_path)
    data_elements()
    annotations()
