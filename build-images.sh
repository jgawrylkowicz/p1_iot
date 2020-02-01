#!/bin/sh
docker build -t heartratesensor:latest HeartRateSensor/
docker build -t activitytracker:latest ActivitySensor/
docker build -t energyexpenditure:latest EnergyExpenditure/