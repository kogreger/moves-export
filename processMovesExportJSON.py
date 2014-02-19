# -*- coding: utf-8 -*-
"""
processMovesExportJSON.py

Script to process the JSON output of moves-export.com into a structured, 
2-dimensional table for export in CSV or database tables.

Author: Konstantin Greger
"""

import json
import datetime

# initialization
UTCadjust = 9                                   # local timezone of data (e.g.: UTC+9 for JST)
csvSeparator = ";"                              # separator to use in output
inputFileName = "jsonstoryline_20140206.json"   # path and filename of the input JSON string
outputFileName = "storyline_20140206.csv"       # path and filename of the CSV output file

inputFile = open(inputFileName)
data = json.load(inputFile)
json = data[0]['segments']
inputFile.close()

outputFile = open(outputFileName, "w")
outputString = ("ID","tripID","subtripID","trackpointID","type","mode","lon","lat","timestamp","origin")
outputFile.write(csvSeparator.join(outputString) + "\n")

# parse data from JSON string into CSV format
ID = 1
tripID = 1
for segment in json:
    if segment['type'] == "place":
        # stationarity event
        subtripID = 1           # dummy value
        trackpointID = 1
        stype = segment['type']
        mode = segment['type']  # dummy value
        lon = segment['place']['location']['lon']
        lat = segment['place']['location']['lat']
        timestamp = datetime.datetime.strptime(str(segment['startTime']), "%Y%m%dT%H%M%SZ")
        # adjust UTC timestamp by timezone offset
        timestamp += datetime.timedelta(hours = UTCadjust)
        if ID == 1:
            # special treatment for a day's first dataset
            timestamp = datetime.datetime.strptime(data[0]['date'], "%Y%m%d")
        timestamps = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        outputString = (str(ID),str(tripID),str(subtripID),str(trackpointID),str(stype),str(mode),str(lon),str(lat),str(timestamps),"d")
        outputFile.write(csvSeparator.join(outputString) + "\n")
        ID += 1
        trackpointID += 1
        # synthesize intermediate stationary timesteps
        endtimestamp = datetime.datetime.strptime(str(segment['endTime']), "%Y%m%dT%H%M%SZ")
        endtimestamp += datetime.timedelta(hours = UTCadjust)
        while timestamp < endtimestamp:
            timestamp += datetime.timedelta(seconds = 1)
            if timestamp >= datetime.datetime.strptime(data[0]['date'], "%Y%m%d") + datetime.timedelta(days = 1):
                break               # stop at 23:59:59
            timestamps = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            outputString = (str(ID),str(tripID),str(subtripID),str(trackpointID),str(stype),str(mode),str(lon),str(lat),str(timestamps),"s")
            outputFile.write(csvSeparator.join(outputString) + "\n")
            ID += 1
            trackpointID += 1
    elif segment['type'] == "move":
        # actual movement
        stype = segment['type']
        subtripID = 1
        for activities in segment['activities']:
            mode = activities['activity']
            trackpointID = 1
            for trackpoints in activities['trackPoints']:
                lon = trackpoints['lon']
                lat = trackpoints['lat']
                timestamp = datetime.datetime.strptime(str(trackpoints['time']), "%Y%m%dT%H%M%SZ")
                # adjust UTC timestamp by timezone offset
                timestamp += datetime.timedelta(hours = UTCadjust)
                if timestamp >= datetime.datetime.strptime(data[0]['date'], "%Y%m%d") + datetime.timedelta(days = 1):
                    break               # stop at 23:59:59
                if trackpointID == 1:
                    prevTimestamp = timestamp
                    prevLon = lon
                    prevLat = lat
                if ID == 1:
                    # special treatment for a day's first dataset
                    timestamp = datetime.datetime.strptime(data[0]['date'], "%Y%m%d")                    
                else:
                    if timestamp > prevTimestamp + datetime.timedelta(seconds = 1):
                        # save data for next timestep
                        nextLon = lon
                        nextLat = lat
                        nextTimestamp = timestamp
                        # synthesize intermediate movement timesteps
                        secsDiff = (nextTimestamp - prevTimestamp).seconds
                        lonDiff = nextLon - prevLon
                        latDiff = nextLat - prevLat
                        for i in range(1, secsDiff):
                            lon = prevLon + ((lonDiff / secsDiff) * i)
                            lat = prevLat + ((latDiff / secsDiff) * i)
                            timestamp = prevTimestamp + datetime.timedelta(seconds = i)
                            if timestamp >= datetime.datetime.strptime(data[0]['date'], "%Y%m%d") + datetime.timedelta(days = 1):
                                break               # stop at 23:59:59
                            timestamps = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                            outputString = (str(ID),str(tripID),str(subtripID),str(trackpointID),str(stype),str(mode),str(lon),str(lat),str(timestamps),"s")
                            outputFile.write(csvSeparator.join(outputString) + "\n")
                            ID += 1
                            trackpointID += 1
                        # restore data for next timestep
                        lon = nextLon
                        lat = nextLat
                        timestamp = nextTimestamp
                if timestamp >= datetime.datetime.strptime(data[0]['date'], "%Y%m%d") + datetime.timedelta(days = 1):
                    break               # stop at 23:59:59
                timestamps = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                outputString = (str(ID),str(tripID),str(subtripID),str(trackpointID),str(stype),str(mode),str(lon),str(lat),str(timestamps),"d")
                outputFile.write(csvSeparator.join(outputString) + "\n")
                trackpointID += 1
                ID += 1
                prevLon = lon
                prevLat = lat
                prevTimestamp = timestamp
            subtripID += 1
    tripID += 1
    if timestamp >= datetime.datetime.strptime(data[0]['date'], "%Y%m%d") + datetime.timedelta(days = 1):
        break               # stop at 23:59:59