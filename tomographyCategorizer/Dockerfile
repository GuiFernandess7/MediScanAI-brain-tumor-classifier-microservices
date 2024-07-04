FROM python:3.8-slim-buster

LABEL maintainer="guilhermesampaio"

ENV TF_ENABLE_ONEDNN_OPTS=0

WORKDIR /app

RUN useradd -m app
RUN chown -R app:app /app

USER app

ENV PATH="/home/app/.local/bin:${PATH}"

COPY requirements.txt /app/requirements.txt

COPY package/tensorflow-2.7.0-cp38-cp38-linux_x86_64.whl /app/tensorflow-2.7.0-cp38-cp38-linux_x86_64.whl

RUN pip install --upgrade pip && \
    pip install --user --no-cache-dir -r /app/requirements.txt && \
    pip install --user --no-cache-dir /app/tensorflow-2.7.0-cp38-cp38-linux_x86_64.whl

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
