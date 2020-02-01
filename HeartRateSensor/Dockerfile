# docker build -t heartratesensor:latest SimulatedHeartRateSensor/
# docker run -p 127.0.0.1:9000:9000 --name hr0 -t heartratesensor:latest 9000
FROM arm32v7/python:3.7-alpine

WORKDIR /app

COPY requirements.txt .
COPY HeartRateSensor.py .

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python", "HeartRateSensor.py"]
CMD ["8000", "http://host.docker.internal:7000/logs"]