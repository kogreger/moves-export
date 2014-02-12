# -*- coding: utf-8 -*-
"""
processMovesExportJSON.py

Script to process the JSON output of moves-export.com into a structured, 2-dimensional table for export in CSV or database tables.

Author: Konstantin Greger
"""

import sys
import json
import datetime

# initialization
UTCadjust = 9                                   # set this to the local timezone of data collection (e.g.: UTC+9 for JST)
csvSeparator = ";"                              # set this to the separator you need in the output
inputFileName = "jsonstoryline_20140205.json"   # set this to the path and filename of the JSON string to process
outputFileName = "storyline_20140205.csv"       # set this to the path and filename of the CSV output file

inputFile = open(inputFileName)
data = json.load(inputFile)
json = data[0]['segments']
inputFile.close()

outputFile = open(outputFileName, "w")

# parse data from JSON string into CSV format
ID = 1
tripID = 1
for segment in json:
    if segment['type'] == "place":
        # stationarity event
        subtripID = 1           # dummy value
        trackpointID = 1        # dummy value
        stype = segment['type']
        mode = segment['type']  # dummy value
        lon = segment['place']['location']['lon']
        lat = segment['place']['location']['lat']
        timestamp = datetime.datetime.strptime(str(segment['startTime']), "%Y%m%dT%H%M%SZ")
        if ID == 1:
            # special treatment for a day's first dataset
            timestamp = datetime.datetime.strptime(data[0]['date'], "%Y%m%d")
        else:
            # adjust UTC timestamp by timezone offset
            timestamp += datetime.timedelta(hours = UTCadjust)
        timestamps = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        data = (str(ID),str(tripID),str(subtripID),str(trackpointID),str(stype),str(mode),str(lon),str(lat),str(timestamps),"d")
        outputFile.write(csvSeparator.join(data) + "\n")
        ID += 1
        # synthesize intermediate stationary timesteps
        endtimestamp = datetime.datetime.strptime(str(segment['endTime']), "%Y%m%dT%H%M%SZ")
        endtimestamp += datetime.timedelta(hours = UTCadjust)
        while timestamp < endtimestamp:
            timestamp += datetime.timedelta(seconds = 1)
            timestamps = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            data = (str(ID),str(tripID),str(subtripID),str(trackpointID),str(stype),str(mode),str(lon),str(lat),str(timestamps),"s")
            outputFile.write(csvSeparator.join(data) + "\n")
            ID += 1
            #if ID == 10: sys.exit("Done for now... - Restart Python interpreter!")
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
                if trackpointID == 1: prevTimestamp = timestamp
                if ID == 1:
                    # special treatment for a day's first dataset
                    timestamp = datetime.datetime.strptime(data[0]['date'], "%Y%m%d")                    
                else:
                    # adjust UTC timestamp by timezone offset
                    timestamp += datetime.timedelta(hours = UTCadjust)
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
                            timestamps = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                            data = (str(ID),str(tripID),str(subtripID),str(trackpointID),str(stype),str(mode),str(lon),str(lat),str(timestamps),"s")
                            outputFile.write(csvSeparator.join(data) + "\n")
                            ID += 1
                            trackpointID += 1
                        # restore data for next timestep
                        lon = nextLon
                        lat = nextLat
                        timestamp = nextTimestamp
                timestamps = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                data = (str(ID),str(tripID),str(subtripID),str(trackpointID),str(stype),str(mode),str(lon),str(lat),str(timestamps),"d")
                outputFile.write(csvSeparator.join(data) + "\n")
                trackpointID += 1
                ID += 1
                prevLon = lon
                prevLat = lat
                prevTimestamp = timestamp
            subtripID += 1
    tripID += 1