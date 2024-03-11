import arviz as az
import pandas as pd
import pytest

from eagleeye import preprocessing as pp


@pytest.fixture
def data():
    return az.from_netcdf("../de.uke.iam.mouse/data/bar-v1/3.ndf")

def test_get_confidence(data):
    res = pp.get_confidence(data)
    assert isinstance(res, list)
    for df in res:
        assert isinstance(df, pd.DataFrame)
