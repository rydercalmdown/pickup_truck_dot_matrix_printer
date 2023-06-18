FROM python:3.8
WORKDIR /code
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    tini

COPY src/requirements.txt .
RUN pip install -r requirements.txt
COPY src .

ENTRYPOINT ["/usr/bin/tini", "--"]

CMD [ "python", "app.py" ]
