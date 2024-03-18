# Eageleye

## Observing mice from the beginning till the end 🦅

## Run the container
Foward a port from your port range to Docker host:
```
ssh username@iam-docker -NL {your-port}:localhost:{your-port}
```

Run the following command to start EagelEye on Docker host:
```
docker run -it --rm -v {my-volume}:/data -p {your-port}:8501 eagleeye
```

Navigate your browser to `localhost:{your-port}`.
