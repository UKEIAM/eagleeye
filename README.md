# Eageleye

Observing mice from the beginning till the end 🦅

![View with EagleEye](https://github.com/UKEIAM/eagleeye/assets/11088297/0306df34-fd9c-457a-81dd-ad24aef952c7)

## Run the container
### Prerequisites
To supply the app with data you have to provide a docker volume with the following layout:

* the root path must contain the directories "models" and "input".
* there is a file "/input/features-with-indicators.pkl" that contains the original training data.
* "/models" contains a set of NetCDF files. The names of the these files will appear in the mouse ID drop down menu.
* you can use the volume "bar-output" for testing. Please make sure to not overwrite any data on it!

### Start the app
Foward a port from your port range to Docker host:
```
ssh username@iam-docker -NL {your-port}:localhost:{your-port}
```

Run the following command to start EagelEye on Docker host:
```
docker run -it --rm -v {my-volume}:/data -p {your-port}:8501 eagleeye
```

Navigate your browser to `localhost:{your-port}`.
