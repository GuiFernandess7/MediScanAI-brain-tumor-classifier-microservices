FROM python:3.8-slim-buster

LABEL maintainer="guilhermesampaio"

ENV TF_ENABLE_ONEDNN_OPTS=0

WORKDIR /app

COPY requirements.txt /app/requirements.txt

COPY ./package/tensorflow-2.7.0-cp38-cp38-linux_x86_64 /app/tensorflow-2.7.0-cp38-cp38-linux_x86_64

RUN pip install --no-cache-dir -r /app/requirements.txt && \
    pip install --no-cache-dir /app/tensorflow-2.7.0-cp38-cp38-linux_x86_64

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
