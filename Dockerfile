FROM python:3.10-slim-bullseye
ENV PYTHON=python3.10

ADD . /opt/eda-demo
ADD https://bootstrap.pypa.io/get-pip.py /
RUN $PYTHON /get-pip.py
WORKDIR /opt/eda-demo
RUN pip install -e .
