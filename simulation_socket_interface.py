import socket
import os
import subprocess

import commands as comm
from configuration_settings import *
from simulation_socket import *

class SimulationSocketInterface:

    def __init__(self):
        self.host = '127.0.0.1'
        self.configSettings = ConfigurationSettings()
        self.controlPort = int(self.configSettings.settings["controlPort"])
        self.observationPort = int(self.configSettings.settings["observationPort"])
        self.controlSocket = SimulationSocket(self.host, self.controlPort)
        self.observationSocket = SimulationSocket(self.host, self.observationPort)


