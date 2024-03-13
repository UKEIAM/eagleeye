FROM python:3.12 AS basis

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y liblapack3 && rm -rf /var/lib/lists/*
RUN apt install -y vim
RUN pip install -U build

COPY . ./repo

FROM basis AS trainer

WORKDIR /home
#COPY ./data/features-with-indicators.pkl /home/data/features-with-indicators.pkl
