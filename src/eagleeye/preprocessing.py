"""
Preprocess idata for chart functions.
"""
from typing import Any, cast

import arviz as az
import numpy as np
import pandas as pd


FloatArray = np.ndarray[Any, np.dtype[np.float64]]


def get_predictions(idata: az.InferenceData) -> pd.DataFrame:
    df = idata.predictions.llh.mean(["chain", "draw"]).to_dataframe()
    df = df.reset_index(drop=True).reset_index()
    df.columns = ["index", "prediction"]
    return cast(pd.DataFrame, df)


def get_forecast(idata: az.InferenceData) -> pd.DataFrame:
    x = idata.predictions.obs_id_future.to_dataframe()
    y = idata.predictions.yhat_fut.mean(["chain", "draw"]).to_dataframe()
    df = pd.concat((x, y), axis=1)
    df.index.name = None
    df.columns = pd.Index(["index", "forecast"])
    return df


def get_confidence(idata: az.InferenceData, *,
                   qnt: FloatArray = np.linspace(51, 99, 10),
                   mode: str = "predictions"
                   ) -> list[pd.DataFrame]:
    if mode == "predictions":
        index = np.arange(idata.predictions.obs_idx.data.size, dtype=np.int32)
        weight = az.extract(idata, group="predictions").llh
    elif mode == "forecast":
        index = idata.predictions.obs_id_future
        weight = az.extract(idata, group="predictions").yhat_fut
    else:
        raise ValueError(f"Unknown mode '{mode}'.")

    out = []
    for p in qnt[::-1]:
        upper, lower = np.percentile(weight, [p, 100-p], axis=1)
        df = pd.DataFrame(
                {'upper': upper, 'lower': lower},
                index=index).reset_index()
        out.append(df)

    return out
