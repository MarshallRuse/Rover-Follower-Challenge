import socket
import commands as comm
import os
import subprocess

controlSock = 0
obsSock = 0
host = '127.0.0.1'

def readFile(fileName):
    f = open(fileName)
    lines = f.read().splitlines()
    f.close()
    return lines

def findPorts(lines):
    conPort = 0
    obsPort = 0
    # probably the first 2 lines, but function scans the whole
    # config text in case settings are rearranged
    for line in lines:
        setting = line.split("=")
        if setting[0].lower() == "controlport":
            conPort = int(setting[1])
        if setting[0].lower() == "observationport":
            obsPort = int(setting[1])

    return conPort, obsPort

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


configSettings = readFile("../Settings/config.txt")
conPort, obsPort = findPorts(configSettings)

