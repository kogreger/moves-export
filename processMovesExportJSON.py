# -*- coding: utf-8 -*-
"""
processMovesExportJSON.py

Script to process the JSON output of moves-export.com into a structured, 2-dimensional table for export in CSV or database tables.

Author: Konstantin Greger
"""

import json
import time
import datetime

# initialization
UTCadjust = datetime.timedelta(hours=9)         # set this to the local timezone of data collection (e.g.: UTC+9 for JST)
csvSeparator = ";"                              # set this to the separator you need in the output
inputFileName = "jsonstoryline_20140205.json"   # set this to the path and filename of the JSON string to process

f = open(inputFileName)
data = json.load(f)
json = data[0]['segments']

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
        if tripID == 1:
            # special treatment for a day's first dataset
            timestamp = datetime.datetime.strptime(data[0]['date'], "%Y%m%d")
        else:
            # adjust UTC timestamp by timezone offset
            timestamp = timestamp + UTCadjust
        timestamps = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        data = (str(ID),str(tripID),str(subtripID),str(trackpointID),str(stype),str(mode),str(lon),str(lat),str(timestamps))
        print csvSeparator.join(data)
        ID += 1
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
                if tripID == 1:
                    # special treatment for a day's first dataset
                    timestamp = datetime.datetime.strptime(data[0]['date'], "%Y%m%d")                    
                else:
                    # adjust UTC timestamp by timezone offset
                    timestamp = timestamp + UTCadjust
                timestamps = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                data = (str(ID),str(tripID),str(subtripID),str(trackpointID),str(stype),str(mode),str(lon),str(lat),str(timestamps))
                print csvSeparator.join(data)
                trackpointID += 1
                ID += 1
            subtripID += 1
    tripID += 1