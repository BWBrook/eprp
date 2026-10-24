FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends libgl1 libglib2.0-0 libgomp1 && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir pygplates==1.0.0 numpy pandas scipy pyarrow requests \
 && python -c "import pygplates; print(pygplates.__version__)" \
 && pip freeze > /opt/pip-freeze.txt
WORKDIR /work
