FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /kafka-producer
WORKDIR /kafka-producer
COPY requirements.txt /kafka-producer/
RUN pip install -r requirements.txt
COPY producer.py /kafka-producer/producer.py
CMD ["python", "./producer.py"]
