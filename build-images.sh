#!/bin/sh
version=$(git describe)

if ( "$version" == "" ) then 
    version="latest"
fi

docker build -t heartratesensor:${version} HeartRateSensor/
docker build -t activitytracker:${version} ActivitySensor/
docker build -t energyexpenditure:${version} EnergyExpenditure/