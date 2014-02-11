# -*- coding: utf-8 -*-
"""
processMovesExportJSON.py

Script to process the JSON output of moves-export.com into a 
structured, 2-dimensional table for export in CSV or database tables.

Author: Konstantin Greger
Date:  2014/02/10

"""

import json
import time
from pytz import timezone
import pytz

# initialization
utc = pytz.utc
#targetTimeZone = timezone('Asia/Tokyo') # set this to the timezone you intend to use in your I/O (cf. http://stackoverflow.com/questions/13866926/python-pytz-list-of-timezones for a list of pytz timezones)
inputFileName = "jsonstoryline_20140205.json"
f = open(inputFileName)
data = json.load(f)
json = data[0]['segments']

# parse data from JSON string into CSV format
ID = 1
tripID = 1
for segment in json:
    if segment['type'] == "place":
        # stationarity event
        subtripID = 1 # dummy value
        trackpointID = 1 # dummy value
        stype = segment['type']
        mode = segment['type'] # dummy value
        lon = segment['place']['location']['lon']
        lat = segment['place']['location']['lat']
        timestamp_ = time.strptime(str(segment['startTime']), "%Y%m%dT%H%M%SZ")
        timestamp__ = time.strftime("%Y-%m-%d %H:%M:%S", timestamp_)
        data = (str(ID),str(tripID),str(subtripID),str(trackpointID),str(stype),str(mode),str(lon),str(lat),str(timestamp__))
        print ";".join(data)
        ID += 1
    elif segment['type'] == "move":
        # actual movement
        stype = segment['type']
        subtripID = 1
        for activities in segment['activities']:
            mode = activities['activity']
            trackpointID = 1
            for trackpoints in activities['trackPoints']:
                timestamp_ = time.strptime(str(trackpoints['time']), "%Y%m%dT%H%M%SZ")
                timestamp__ = time.strftime("%Y-%m-%d %H:%M:%S", timestamp_)
                lon = trackpoints['lon']
                lat = trackpoints['lat']
                data = (str(ID),str(tripID),str(subtripID),str(trackpointID),str(stype),str(mode),str(lon),str(lat),str(timestamp__))
                print ";".join(data)
                trackpointID += 1
                ID += 1
            subtripID += 1
    tripID += 1