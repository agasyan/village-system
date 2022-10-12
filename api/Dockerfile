FROM python:3.8-slim

RUN apt-get update \
    && apt-get -y install libpq-dev gcc 

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /api/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . /api/

EXPOSE 8000
