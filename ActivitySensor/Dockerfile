# docker build -t activitysensor:0.0.1 SimulatedHeartRateSensor/
# e.g.: docker run --name hr0 -t activitysensor:0.0.1 http://127.0.0.1:7000/device0 0.0.0.0 9000 activity
FROM amd64/python:3.7-slim-buster

WORKDIR /app

COPY requirements.txt .
COPY ActivityTracker.py .

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python", "ActivityTracker.py"]
CMD ["8000", "http//127.0.0.1:7000/edge1"]