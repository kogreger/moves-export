# -*- coding: utf-8 -*-
"""
processMovesExportJSON.py

Script to process the JSON output of moves-export.com into a 
structured, 2-dimensional table for export in CSV or database tables.

Author: Konstantin Greger
Date:  2014/02/10

"""

import json

f = open("/Users/konstantingreger/Downloads/jsonstoryline_20140205.json")
data = json.load(f)

json = data[0]['segments']
ID = 1
tripID = 1
for segment in json:
    if segment['type'] == "place":
        # stationarity event
        #print "ID: " + str(ID)
        #print "tripID: " + str(tripID)
        subtripID = 1 # dummy value
        #print "subtripID: " + str(subtripID)
        trackpointID = 1 # dummy value
        #print "trackpointID: " + str(trackpointID)
        stype = segment['type']
        #print "type: " + str(stype)
        mode = segment['type'] # dummy value
        #print "mode: " + str(mode)
        #print "lon: " + str(segment['place']['location']['lon'])
        #print "lat: " + str(segment['place']['location']['lat'])
        #print "timestamp: " + str(segment['startTime'])
        data = (str(ID),str(tripID),str(subtripID),str(trackpointID),str(stype),str(mode),str(segment['place']['location']['lon']),str(segment['place']['location']['lat']),str(segment['startTime']))
        print ";".join(data)
        ID += 1
    elif segment['type'] == "move":
        # actual movement
        #print "ID: " + str(ID)
        #print "tripID: " + str(tripID)
        stype = segment['type']
        #print "type: " + str(stype)
        subtripID = 1
        for activities in segment['activities']:
            #print "subtripID: " + str(subtripID)
            mode = activities['activity']
            #print "mode: " + str(mode)
            trackpointID = 1
            for trackpoints in activities['trackPoints']:
                #print "trackpointID: " + str(trackpointID)
                #print "lon: " + str(trackpoints['lon'])
                #print "lat: " + str(trackpoints['lat'])
                #print "timestamp: " + str(trackpoints['time'])
                data = (str(ID),str(tripID),str(subtripID),str(trackpointID),str(stype),str(mode),str(trackpoints['lon']),str(trackpoints['lat']),str(trackpoints['time']))
                print ";".join(data)
                trackpointID += 1
                ID += 1
            subtripID += 1
    tripID += 1