# docker build -t ee:0.0.1 EnergyExpenditure/
# docker run -p 127.0.0.1:8991:8991 --name ee0 -t ee:0.0.1 8991 2 http://127.0.0.1:9000/heartrate
FROM arm32v7/python:3.8.1-alpine

WORKDIR /app

COPY requirements.txt .
COPY Server.py .
COPY SensorListener.py .
COPY main.py .

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python", "main.py"]
CMD ["9000", "1"]