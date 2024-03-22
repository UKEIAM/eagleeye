FROM python:3.12 AS basis

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y vim && rm -rf /var/lib/lists/*
RUN pip install -U build


FROM basis AS trainer

WORKDIR /app/repo
COPY . .
RUN python -m build
RUN pip install $(ls dist/*.whl)

CMD ["streamlit", "run", "src/eagleeye/main.py", "--server.fileWatcherType", "none", "--", "/data/models", "/data/input/features-with-indicators.pkl"]
