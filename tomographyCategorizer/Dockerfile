FROM python:3.8-slim-buster

LABEL maintainer="guilhermesampaio"

ENV TF_CPP_MIN_LOG_LEVEL=2

COPY ./requirements.txt /app/requirements.txt
COPY . /app

WORKDIR /app

RUN python3 -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /app/requirements.txt && \
    #/py/bin/pip install ./package/tensorflow-2.7.0-cp38-cp38-linux_x86_64.whl && \
    /py/bin/pip install uvicorn

RUN adduser --disabled-password --no-create-home app && \
    chown -R app:app /app

USER app


EXPOSE 8000
CMD ["/py/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

#https://stackoverflow.com/questions/72235848/starting-container-process-caused-exec-uvicorn-executable-file-not-found-in