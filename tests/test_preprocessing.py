import arviz as az
import pandas as pd
import pytest

from eagleeye import preprocessing as pp
from . import TESTDATA_PATH


@pytest.fixture
def models():
    model_path = TESTDATA_PATH.joinpath("models")
    return (az.from_netcdf(item) for item in model_path.glob("*.ndf"))
    
def test_get_confidence(models):
    for item in models:
        res = pp.get_confidence(item)
        assert isinstance(res, list)
        for df in res:
            assert isinstance(df, pd.DataFrame)
