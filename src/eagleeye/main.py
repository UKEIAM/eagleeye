import argparse
import pathlib
import logging
import sys

import streamlit as st

from eagleeye import widgets
from eagleeye import charts
from eagleeye import utils


log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    args = _parse_cmd_line(argv)
    widgets.init_ui_controls(args)

    mid = st.session_state.ctrl_id_select

    if mid is None:
        st.title("Welcome to EagelEye")
        st.text("Select mouse ID on the left sidebar.")
    else:
        st.title("Evolution of body weight")
        st.text(f"Mouse ID: {mid}")
        path = args.data_path.joinpath(f"{mid}.ndf")

        trace = utils.load_data(path)
        raw_features = utils.load_features(args.feature_path)
        g = raw_features.groupby("mouse_id")
        feat = g.get_group(int(mid))
        charts.chart(feat, trace, args)




def _parse_cmd_line(argv):
    parser = argparse.ArgumentParser("EagleEye")
    parser.add_argument("data_path", type=pathlib.Path, help="Path to data files")
    parser.add_argument("feature_path", type=pathlib.Path, help="Path to feature file")
    return parser.parse_args(argv[1:])


if __name__ == "__main__":
    sys.exit(main())
