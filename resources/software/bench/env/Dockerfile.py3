FROM python:3.12-slim
RUN pip install --no-cache-dir pygplates==1.0.0 numpy pandas scipy pyarrow requests \
 && pip freeze > /opt/pip-freeze.txt
WORKDIR /work
