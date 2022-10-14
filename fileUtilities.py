#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

def readConfigFile(configFilePath):
    # Opening JSON file
    f = open(configFilePath)

    jsonContent = json.load(f)

    return (jsonContent["K2400_gpibAddress"],
            jsonContent["HVSource_gpibAddress"],
            jsonContent["initialVoltage"],
            jsonContent["finalVoltage"],
            jsonContent["pointsVoltage"],
            jsonContent["measureDelay_ms"],
            jsonContent["rampVoltage"],
            jsonContent["outputCurrentLimit"],
            jsonContent["enableKill"],
            jsonContent["ammeterRange"],
            jsonContent["ammeterCompliance"],
            jsonContent["ammeterNPLCs"],
            jsonContent["resultsFilePath"],
            jsonContent["resultsFilePathExtension"])