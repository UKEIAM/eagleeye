# EagleEye 🦅

Visualization and decision support system for humane endpoint detection in laboratory rodents.

![View with EagleEye](https://github.com/UKEIAM/EagleEye/assets/11088297/0306df34-fd9c-457a-81dd-ad24aef952c7)

## Install

We recommend to install EagleEye in a virtual environment. Create a fresh
virtual env and activate it with 

```sh
python -m venv {env-name}
source {env-name}/bin/activate
```

or use a tool like [pyenv](https://github.com/pyenv/pyenv).

### From PyPi
Then install EagleEye the standard Python way:

```sh
pip install eagleeye
```

### From repository
You can also install EagleEye from the repository directly:

```sh
git clone https://github.com/ukeiam/eagleeye
cd eagleeye
pip install .
```

## Run EagleEye

### Run the server locally
To run EagleEye, use the ```run.sh``` command and provide the path to the
models:

```sh
./run.sh /path/to/model/directory
```

### Run as a Docker container
You can also start EagleEye as Docker container. To do so, set the path to your
models in the environment variable `EAGLEEYE_MODEL_PATH`:

```sh
cd path/to/eagleeye/repo
export EAGLEEYE_MODEL_PATH=/path/to/your/models
docker-compose up
```

## Run test suite
The test suite requires a dataset to run. EagelEye reads the path to the root
directory of the test data from the environment variable
`EAGLEEYE_TESTDATA_PATH`. The [demo
dataset](https://www.fdr.uni-hamburg.de/record/16079) is suitable for testing
EagleEye. Additionally, [pytest](https://pytest.org) is required as test
runner. Once all requirements have been met, execute the following commands to
start the test run

```sh
export EAGLEEYE_TESTDATA_PATH=</path/to/test/data/>
pytest
``` 

## Example data
If you want to try EagleEye and have no data, use our [demo dataset](https://www.fdr.uni-hamburg.de/record/16079).
