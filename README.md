# EagleEye 🦅

Visualization and decision support system for humane endpoint detection in laboratory rodents.

![View with EagleEye](https://github.com/UKEIAM/EagleEye/assets/11088297/0306df34-fd9c-457a-81dd-ad24aef952c7)

## Install

It is recommended to install EagleEye in a virtual environment. Create a fresh
virtual env with `python -m venv {env-name} && source
{env-name}/bin/activate`, or use a tool like 
[pyenv](https://github.com/pyenv/pyenv).

### From PyPi
Then install EagleEye the standard Python way:

```sh
pip install eagleeye
```

### From repository
You can also install EagleEye from the repository directly:

```sh
git clone https://github.com/ukeiam/eagleeye
cd EagleEye
pip install .
```


## Run EagleEye

### Run the server locally
To run EagleEye, use the ```run.sh``` command and provide the path to the
models:

```
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

## Example data
If you want to try EagleEye and have no data, use our [demo dataset](https://www.fdr.uni-hamburg.de/record/16079).
