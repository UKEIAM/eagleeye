"""
EagleEye - observing mice from the beginning till the end.
"""
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


def main(argv: list[str] | None = None) -> int:
    """Entry point for app execution."""
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
        path = args.models.joinpath(f"{mid}.ndf")

        trace = utils.load_idata(path)
        raw_features = utils.load_features(args.features)
        g = raw_features.groupby("mouse_id")
        feat = g.get_group(int(mid)).reset_index(drop=True)

        fig = charts.render_chart_elements(feat, trace)
        if fig:
            st.altair_chart(fig, use_container_width=True)

    return 0


def _parse_cmd_line(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser("EagleEye")
    parser.add_argument("-m", "--models", type=pathlib.Path, default=pathlib.Path("/data/models"),
            help="Path to data files")
    parser.add_argument("-f", "--features", type=pathlib.Path, default=pathlib.Path("/data/input/features.pkl"),
        help="Path to feature file")
    args = parser.parse_args(argv[1:])
    _check_args(args)
    return args


def _check_args(args: argparse.Namespace) -> None:
    if args.models.is_dir():
        if not list(args.models.glob("*.ndf")):
            raise ValueError("Model directory empty")
    else:
        raise ValueError("Model path not a directory")

    if not args.features.is_file():
        raise ValueError("Feature path not a regular file")


if __name__ == "__main__":
    sys.exit(main())
