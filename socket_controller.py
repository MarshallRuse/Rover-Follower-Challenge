import socket
import commands as comm
import os
import subprocess

controlSock = 0
obsSock = 0
host = '127.0.0.1'

# Generic function for reading a file and splitting by newline
def readFile(fileName):
    f = open(fileName)
    lines = f.read().splitlines()
    f.close()
    return lines

# Takes a newline delimited list of config settings, turns them into
# a string dictionary of {configName : configSetting}
def configDictionary(configLines):
    configDict = {}
    for line in configLines:
        setting = line.split("=")
        configDict[setting[0]] = setting[1]

    return configDict


def connectControlSock():
    global controlSock
    global host
    global conPort

    controlSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    controlSock.connect((host, conPort))

def connectObserverSock():
    global obsSock
    global host
    global obsPort

    obsSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    obsSock.connect((host, obsPort))


configSettings = configDictionary(readFile("../Settings/config.txt"))
conPort = int(configSettings["controlPort"])
obsPort = int(configSettings["observationPort"])

