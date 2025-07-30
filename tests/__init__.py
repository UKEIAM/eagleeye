import os
from pathlib import Path

env = os.getenv("EE_TESTDATA_PATH")
if env is None:
    raise ValueError("Env var EE_TEST_DATAPATH not set")
TESTDATA_PATH = Path(env)
