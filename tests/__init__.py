import os
from pathlib import Path

env = os.getenv("EAGLEEYE_TESTDATA_PATH")
if env is None:
    raise ValueError("Env var EAGLEEYE_TESTDATA_PATH not set")
TESTDATA_PATH = Path(env)
