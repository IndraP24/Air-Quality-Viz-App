FROM python:3.8

WORKDIR /app

RUN apt-get -y update  && apt-get install -y \
    python3-dev \
    apt-utils \
    python-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade setuptools

RUN pip install --upgrade pip
RUN pip install \
    cython==0.29.24 \
    pystan==2.19.1.1

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD gunicorn -w 3 -k uvicorn.workers.UvicornWorker api.app:app --bind 0.0.0.0:$PORT